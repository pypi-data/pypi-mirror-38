from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import has_focus, Condition
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

def create_key_bindings(trex_layout):

    @Condition
    def output_window_focused():
        _, split = trex_layout.active_split()
        return bool(split and trex_layout.layout.has_focus(split.content_window))

    redis_prompt = trex_layout.redis_prompt
    kb = KeyBindings()

    kb.add('tab')(focus_next)
    kb.add('s-tab')(focus_previous)

    @kb.add('c-d', filter=has_focus(redis_prompt))
    def _(event):
        if redis_prompt.text.strip() == '':
            event.app.exit()

    @kb.add('down', filter=has_focus(redis_prompt))
    @kb.add('c-j', filter=has_focus(redis_prompt))
    def _(event):
        output_splits = trex_layout.splits
        if output_splits:
            trex_layout.layout.focus(output_splits[-1])

    @kb.add('c-k', filter=output_window_focused)
    def _(event):
        trex_layout.layout.focus(redis_prompt)

    @kb.add('right', filter=output_window_focused)
    @kb.add('l', filter=output_window_focused)
    @kb.add('c-l', filter=output_window_focused)
    def _(event):
        output_splits = trex_layout.splits
        i, split = trex_layout.active_split()
        if (i + 1) < len(output_splits):
            trex_layout.layout.focus(output_splits[i+1])

    @kb.add('left', filter=output_window_focused)
    @kb.add('h', filter=output_window_focused)
    @kb.add('c-h', filter=output_window_focused)
    def _(event):
        output_splits = trex_layout.splits
        i, split = trex_layout.active_split()
        if i > 0:
            trex_layout.layout.focus(output_splits[i-1])

    @kb.add(':', filter=output_window_focused)
    def enter_command_mode(event):
        """
        Entering command mode.
        """
        cmd_buffer = trex_layout.commandline
        trex_layout.layout.focus(cmd_buffer.content)

    return kb
