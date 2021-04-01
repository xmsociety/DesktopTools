import time
from PySide2.QtCore import QThread, Signal

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

from pynput import keyboard
class SignalKeyboard(QThread):
    # 有信号发出的线程,接受者可根据信号执行任务
    _signal = Signal()
    def __init__(self):
        super().__init__()
        # with keyboard.Listener(
        #     on_press=on_press,
        #     on_release=self.on_release
        # ) as listener:
        #     listener.join()
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        listener.start()

    def on_press(self, key):
        try:
            print(f"{key.char} pressed.")
        except AttributeError:
            print(f"{key} not have char")
    def on_release(self, key):
        try:
            print(f"{key.char} pressed.")
        except AttributeError:
            print(f"{key} not have char")

    def run(self):
        self._signal.emit()
