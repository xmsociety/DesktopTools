from pynput import keyboard
from PySide6.QtCore import QThread, Signal


class SignalHotKey(QThread):
    _signal = Signal()

    def __init__(self):
        super().__init__()

    def listen(self):
        hotkey = keyboard.GlobalHotKeys(
            {
                "<ctrl>+<alt>+c": self.on_activate,
                "<ctrl>+<alt>+g": lambda: print("Goodbye"),
            }
        )
        hotkey.start()

    def on_activate(self):
        self._signal.emit()
