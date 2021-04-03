import time
from pynput import keyboard, mouse
from PySide2.QtCore import QThread, Signal

from logger import logger

class WorkDict:
    start_time = time.time()
    last_time = time.time()
    work_all = 0
    rest_time = 0
    noinput_time = 0
    buffer_time = 10
    def count_all(self):
        self.work_all = int(self.last_time - self.start_time)
        self.noinput_time = 0
        self.buffer_time = 10

    def count_rest(self):
        self.buffer_time -= 1
        if self.buffer_time <= 0:
            self.rest_time += 1

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

class SignalKeyboard(QThread):
    # 有信号发出的线程,接受者可根据信号执行任务
    _signal = Signal()
    def __init__(self):
        super().__init__()

    def listen(self):
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
        self._signal.emit()


class SignalMouse(QThread):
    _signal = Signal()
    def __init__(self):
        self.x, self.y = 0, 0
        super().__init__()

    def listen(self):
        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        listener.start()

    def on_move(self, x, y):
        logger.debug(f"move&({x},{y})")
        self._signal.emit()

    def on_click(self, x, y, button, pressed):
        action = 'Pressed' if pressed else 'Released'
        logger.debug(f"{button._name_}&{action}&({x},{y})")
        self._signal.emit()

    def on_scroll(self, x, y, dx, dy):
        logger.debug(f"scroll&({dx},{dy})&({x},{y})")
        self._signal.emit()

