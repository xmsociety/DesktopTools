import time
from pynput import keyboard, mouse
from PySide2.QtCore import QThread, Signal

from logger import logger

class ThreadSimple(QThread):
    # 简易线程
    def __init__(self):
        super().__init__()

    def run(self):
        values = [1, 2, 3, 4, 5]
        for i in values:
            print(i)
            time.sleep(0.5)  # 休眠

class ThreadSignal(QThread):
    # 有信号发出的线程,接受者可根据信号执行任务
    _signal = Signal()
    def __init__(self):
        super().__init__()

    def run(self):
        values = ["a", "b", "c", "d", "e"]
        for i in values:
            print(i)
            time.sleep(0.5)
        self._signal.emit()

class LogCache:
    pass

class SignalKeyboard(QThread):
    # 有信号发出的线程,接受者可根据信号执行任务
    # _signal = Signal()
    # self._signal.emit()
    def __init__(self):
        super().__init__()
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()

    def log_event(self, name, key):
        try:
            logger.debug(f"{key.char}&{name}")
        except AttributeError:
            logger.debug(f"{key._name_}&{name}")

    def on_press(self, key):
        self.log_event("pressed", key)

    def on_release(self, key):
        self.log_event("released", key)


class SignalMouse(QThread):
    def __init__(self):
        super().__init__()
        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        listener.start()

    def on_move(self, x, y):
        logger.debug(f"move&({x},{y})")

    def on_click(self, x, y, button, pressed):
        action = 'Pressed' if pressed else 'Released'
        logger.debug(f"{button._name_}&{action}&({x},{y})")

    def on_scroll(self, x, y, dx, dy):
        logger.debug(f"scroll&({dx},{dy})&({x},{y})")

