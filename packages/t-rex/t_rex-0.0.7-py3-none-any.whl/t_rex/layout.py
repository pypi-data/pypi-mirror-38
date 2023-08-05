from functools import partial
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea, SearchToolbar, VerticalLine, HorizontalLine
from prompt_toolkit.widgets.toolbars import SystemToolbar, FormattedTextToolbar
from prompt_toolkit.filters import has_focus, is_searching
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import (
    VSplit,
    HSplit,
    FloatContainer,
    ConditionalContainer,
    Float,
)
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.application import get_app

from .completer import redis_completer
from t_rex.postprocessors import shell_processor, default_processor


def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter()
        yield x


class TrexLayout:
    def __init__(self, redis_executor):
        self.redis_exec = redis_executor
        self.redis_prompt = TextArea(
            height=1,
            prompt="> ",
            completer=redis_completer,
            style="class:input-field",
            multiline=False,
            accept_handler=self.redis_handler,
            focus_on_click=True,
        )
        self.splits = []
        # self._add_split(None, "")

    def create(self, focused_element=None):
        focused_element = focused_element or self.redis_prompt
        output_w = VSplit(self.splits and list(intersperse(self.splits, VerticalLine)))
        if self.splits:
            hsplits = [self.redis_prompt, HorizontalLine(), output_w]
        else:
            hsplits = [self.redis_prompt, HorizontalLine()]
        root_container = FloatContainer(
            content=HSplit(hsplits),
            floats=[
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=4, scroll_offset=1),
                    transparent=True,
                )
            ],
        )
        self.layout = Layout(root_container, focused_element=focused_element)
        return self.layout

    def _add_split(self, redis_cmd, contents):
        i, _ = self.active_split()
        # discard remaining splits after the current active_split.
        self.splits = self.splits[: i + 1]
        self.splits.append(
            OutputSplit(contents, self.enter_handler, redis_cmd, self.get_layout)
        )

    def get_layout(self):
        return self.layout

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
        redis_cmd, results = self.redis_exec(text)
        self.display(redis_cmd, results)

    def enter_handler(self, buf):
        _, split = self.active_split()
        text = buf.document.current_line
        redis_cmd, results = self.redis_exec(
            text, scoped=True, prev_cmd=split.redis_cmd
        )
        metadata = self.redis_exec(text, metadata=True)
        self.display(redis_cmd, results)
        return True

    def display(self, redis_cmd, results):
        if results is None:
            return
        current_window = self.layout.current_window

        self._add_split(redis_cmd, results)
        self.create(focused_element=current_window)
        # Force a redraw of the app.
        app = get_app()
        app.layout = self.layout
        app.invalidate()


class OutputSplit(HSplit):
    def __init__(self, content, enter_handler, redis_cmd, root_layout):
        self.get_layout = root_layout
        self.raw_content = content
        self.postprocessors = [default_processor]
        self.search = SearchToolbar()
        self.statusbar = StatusBar(self.processors)
        self.redis_cmd = redis_cmd
        self.commandline = CommandLine(self.cmd_handler)
        self.errorbar = ErrorToolbar(has_focus(self.commandline))
        err, self.processed_content = self.process(self.raw_content)
        self.errorbar.set_error_message(err)
        self.content_window = TextArea(
            search_field=self.search,
            read_only=True,
            text=self.processed_content,
            focus_on_click=True,
            accept_handler=enter_handler,
            style="class:output-field",
            wrap_lines=False,
        )
        self.content_window.window.cursorline = has_focus(self)
        super(OutputSplit, self).__init__(
            [
                self.content_window,
                self.search,
                self.statusbar,
                self.commandline,
                self.errorbar,
            ]
        )

    def cmd_handler(self, buf):
        self.get_layout().focus(self.content_window)
        user_cmd = buf.text.strip()
        err = ""
        if user_cmd == "undo":
            if len(self.postprocessors) > 1:
                self.postprocessors.pop()
                err, self.processed_content = self.process(self.raw_content)
            else:
                return
        elif user_cmd == "reset":
            if len(self.postprocessors) > 1:
                self.postprocessors = [default_processor]
                err, self.processed_content = self.process(self.raw_content)
            else:
                return
        else:
            processor = partial(shell_processor, user_cmd)
            processor.__name__ = user_cmd
            err, self.processed_content = processor(self.processed_content)
            if err is None:
                self.postprocessors.append(processor)
        self.errorbar.set_error_message(err)
        self.content_window.buffer.set_document(
            Document(
                text=self.processed_content, cursor_position=len(self.processed_content)
            ),
            bypass_readonly=True,
        )

    def processors(self):
        return self.postprocessors

    def process(self, contents):
        for postprocessor in self.postprocessors:
            err, contents = postprocessor(contents)
            if err:
                break
        return err, contents


class ErrorToolbar(ConditionalContainer):
    def __init__(self, hide_error):
        super(ErrorToolbar, self).__init__(
            FormattedTextToolbar(self.get_error_message),
            filter=(~hide_error & ~is_searching),
        )

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
            tokens = ">".join([x.__name__ for x in processors()])
            return tokens or "default"

        super(StatusBar, self).__init__(get_text, style="class:toolbar.status")


class CommandLine(ConditionalContainer):
    """
    The command line. (For at the bottom of the screen.)
    """

    def __init__(self, handler):
        super(CommandLine, self).__init__(
            TextArea(
                height=1,
                prompt=":",
                # completer=redis_completer,
                style="class:input-field",
                multiline=False,
                accept_handler=handler,
                focus_on_click=True,
            ),
            filter=has_focus(self),
        )
