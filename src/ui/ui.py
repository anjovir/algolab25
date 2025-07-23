from ui.midi_app import MidiApp


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._handle_midi_app()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _handle_midi_app(self):
        self._show_midi_app()

    def _show_midi_app(self):
        self._hide_current_view()

        self._current_view = MidiApp(
            self._root
        )

        self._current_view.pack()