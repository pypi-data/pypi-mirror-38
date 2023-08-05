from prompt_toolkit.application import Application
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.styles import Style
from .layout import TrexLayout
from .keybindings import create_key_bindings
from .executor import Executor


# Create a class called Trex() and do the config, logging and application
# initialization.

class Trex(object):
    def __init__(self):
        self.executor = Executor()
        self.layout = TrexLayout(self.__executor)
        kb = create_key_bindings(self.layout)
        style = Style.from_dict({
            'cursor-line': 'nounderline reverse',
            'toolbar.status': '#ffffff bg:#444444',
            })
        self.app = Application(
                layout=self.layout.create(),
                key_bindings=kb,
                mouse_support=True,
                style=style,
                full_screen=True)
        self.app.key_processor.before_key_press += self.choose_keybinding

    def __executor(self, text, metadata=False, scoped=False, prev_cmd=None):
        if not text:
            return
        if scoped:
            result = self.executor.scoped_run(text, prev_cmd)
        elif metadata:
            result = self.executor.get_metadata(text)
        else:
            result = self.executor.run(text, True)

        self.result = result
        return result

    def choose_keybinding(self, *_):
        if self.app.layout.has_focus(self.layout.redis_prompt):
            self.app.editing_mode = EditingMode.EMACS
        else:
            self.app.editing_mode = EditingMode.VI

def run():
    Trex().app.run()


if __name__ == '__main__':
    run()
