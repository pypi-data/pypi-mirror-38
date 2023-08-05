import inspect
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, SearchToolbar, VerticalLine, HorizontalLine
from prompt_toolkit.widgets.toolbars import SystemToolbar, FormattedTextToolbar
from prompt_toolkit.filters import has_focus, is_searching
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import (VSplit,
        HSplit,
        FloatContainer,
        ConditionalContainer,
        Float)
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.application import get_app

from .completer import redis_completer
import t_rex.postprocessors as postprocessors

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter()
        yield x

available_processors = dict(inspect.getmembers(postprocessors, inspect.isfunction))

class TrexLayout:
    def __init__(self, redis_executor):
        self.redis_exec = redis_executor
        self.default_processor = [postprocessors.default_processor]
        self.additional_processors = []
        self.redis_prompt = TextArea(height=1, prompt='> ',
                completer=redis_completer,
                style='class:input-field',
                multiline=False,
                accept_handler=self.redis_handler,
                focus_on_click=True
                )
        self.commandline = CommandLine(self.cmd_handler)
        self.errorbar = ErrorToolbar(has_focus(self.commandline))
        self.statusbar = StatusBar(self.processors)
        self.splits = []
        self._add_split(None, '')

    def processors(self):
        return self.additional_processors

    def create(self, focused_element=None):
        focused_element = focused_element or self.redis_prompt
        output_w = VSplit(list(intersperse(self.splits, VerticalLine)))
        root_container = FloatContainer(
                content=HSplit([
                    self.redis_prompt,
                    HorizontalLine(),
                    output_w,
                    self.statusbar,
                    self.commandline,
                    self.errorbar,
                    ]),
                floats=[
                    Float(xcursor=True,
                        ycursor=True,
                        content=CompletionsMenu(max_height=4, scroll_offset=1),
                        transparent=True,
                        )]
                )
        self.layout = Layout(root_container, focused_element=focused_element)
        return self.layout

    def _add_split(self, cmd, contents):
        i, _ = self.active_split()
        # discard remaining splits after the current active_split.
        self.splits = self.splits[:i+1]
        self.splits.append(OutputSplit(
                                contents,
                                self.enter_handler,
                                self.default_processor + self.additional_processors,
                                cmd,
                                self.errorbar.set_error_message,
                                ))

    def active_split(self):
        for i, split in enumerate(self.splits):
            if self.layout.has_focus(split):
                return i, split
        return -1, None

    def redis_handler(self, buf):
        text = buf.text
        if not text:
            return
        self.splits = []
        cmd, results = self.redis_exec(text)
        self.display(cmd, results)

    def enter_handler(self, buf):
        _, split = self.active_split()
        text = buf.document.current_line
        cmd, results = self.redis_exec(text, scoped=True, prev_cmd=split.cmd)
        metadata = self.redis_exec(text, metadata=True)
        self.display(cmd, results)
        return True

    def display(self, cmd, results):
        if results is None:
            return
        current_window = self.layout.current_window

        self._add_split(cmd, results)
        self.create(focused_element=current_window)
        # Force a redraw of the app.
        app = get_app()
        app.layout = self.layout
        app.invalidate()

    def cmd_handler(self, buf):
        self.layout.focus_last()
        name = buf.text.strip()
        processor = available_processors.get(name)
        if processor:
            self.additional_processors.append(processor)
            last_split = self.splits[-1]
            last_split.postprocessors.append(processor)
            last_split.apply_processor(processor)


class OutputSplit(HSplit):
    def __init__(self, content, enter_handler, processors, cmd, err_handler):
        self.raw_content = content
        self.postprocessors = processors
        self.err_handler = err_handler
        self.search = SearchToolbar()
        self.cmd = cmd
        err, self.processed_content = self.process(self.raw_content)
        self.err_handler(err)
        self.content_window = TextArea(search_field=self.search,
                read_only=True,
                text=self.processed_content,
                focus_on_click=True,
                accept_handler=enter_handler,
                style='class:output-field',
                wrap_lines=False,
                )
        self.content_window.window.cursorline = has_focus(self)
        super(OutputSplit, self).__init__(
                [self.content_window, self.search]
                )

    def process(self, contents):
        for postprocessor in self.postprocessors:
            err, contents = postprocessor(contents)
            if err:
                break
        return err, contents

    def apply_processor(self, processor):
        err, self.processed_content = processor(self.processed_content)
        self.err_handler(err)
        self.content_window.buffer.set_document(
            Document(text=self.processed_content,
                     cursor_position=len(self.processed_content)),
            bypass_readonly=True)


class ErrorToolbar(ConditionalContainer):
    def __init__(self, hide_error):
        super(ErrorToolbar, self).__init__(
                FormattedTextToolbar(self.get_error_message),
                filter=(~hide_error & ~is_searching))

    def get_error_message(self):
        return self.message

    def set_error_message(self, message):
        self.message = message

class StatusBar(FormattedTextToolbar):
    """
    The status bar, shown below the window.
    """
    def __init__(self, processors):
        def get_text():
            tokens = '>'.join([x.__name__ for x in processors()])
            return tokens or 'default'

        super(StatusBar, self).__init__(
            get_text,
            style='class:toolbar.status')


class CommandLine(ConditionalContainer):
    """
    The command line. (For at the bottom of the screen.)
    """
    def __init__(self, handler):
        super(CommandLine, self).__init__(
                TextArea(height=1, prompt=':',
                    # completer=redis_completer,
                    style='class:input-field',
                    multiline=False,
                    accept_handler=handler,
                    focus_on_click=True,
                    ),
                filter=has_focus(self))
