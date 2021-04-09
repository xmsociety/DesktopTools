import time
from pynput import keyboard, mouse
from sqlalchemy import create_engine
from PySide2.QtCore import QThread, Signal

from logger import logger, slogger
from data_alchemy.models import WorkInfo
from data_alchemy.inputs import add_count_keymouse
from data_alchemy.worktimes import write_work_info
from args import KEYBOARD_DeviceNo, MOUSE_DeviceNo, TICKER_DeviceNo


class WorkDict:
    start_time = time.time()
    work_by_len = 10
    work_by = []
    work_all = 0
    rest_time = 0
    now_status = [None, None]
    status_continued = {}

    def fill_work_by(self, device_no):
        if len(self.work_by) >= self.work_by_len:
            self.work_by.pop(0)
        self.work_by.append(device_no)

    def count_work(self):
        self.work_all += 1
        return self.work_all

    def count_rest(self):
        self.rest_time += 1
        return self.rest_time

    def count_status_continued(self):
        nstatus = self.now_status[-1]
        lstatus = self.now_status[0]
        last_continued = self.status_continued.get(lstatus, 0)
        continued = self.status_continued.get(nstatus, 0)
        continued += 1
        to_dict = {nstatus: continued}
        slogger.debug(
            f"change status_continued from **{self.status_continued}** to **{to_dict}**"
        )
        self.status_continued = to_dict
        return last_continued

    def count_now_status(self) -> (int, bool):
        from collections import Counter
        dict_by = Counter(self.work_by)
        num_work = dict_by.get(KEYBOARD_DeviceNo, 0) + dict_by.get(
            MOUSE_DeviceNo, 0)
        num_rest = dict_by.get(TICKER_DeviceNo, 0)
        slogger.debug(
            f"work status num| num_work: {num_work}, num_rest: {num_rest}")
        continued = 0
        if num_work:
            self.now_status[-1] = WorkInfo.type_map_reverse["工作"]
            self.count_work()
        else:
            self.now_status[-1] = WorkInfo.type_map_reverse["小憩"]
            self.count_rest()

        continued = self.count_status_continued()
        if self.now_status[0] != self.now_status[-1]:
            write_work_info(self.now_status[0], continued=continued)
            slogger.info(
                f"work status changed: **{self.now_status[0]}_{continued}** -> **{self.now_status[-1]}**"
            )

            self.now_status[0] = self.now_status[-1]
        else:
            slogger.debug("work status no changed")

    def summarize(self):
        self.fill_work_by(TICKER_DeviceNo)
        self.count_now_status()


class ThreadSimple(QThread):
    # 简易线程
    def __init__(self):
        super().__init__()

    def run(self):
        values = [1, 2, 3, 4, 5]
        for i in values:
            print(i)
            time.sleep(0.5)    # 休眠


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
        listener = keyboard.Listener(on_press=self.on_press,
                                     on_release=self.on_release)
        listener.start()

    def log_event(self, name, key, save=0):
        try:
            char_name = key.__dict__.get("char")
            if char_name:
                char_name = key.char
                event_name = name
            else:
                char_name = key._name_
                event_name = name
            if save:
                save = add_count_keymouse(char_name, KEYBOARD_DeviceNo)
            logger.info(f"{char_name}&{event_name}&save_{save}")
        except AttributeError as err:
            logger.error(f"keyboard event catch error: {err} => {key}")

    def on_press(self, key):
        self.log_event("pressed", key, save=1)

    def on_release(self, key):
        self.log_event("released", key)
        self._signal.emit()


class SignalMouse(QThread):
    _signal = Signal()

    def __init__(self):
        self.x, self.y = 0, 0
        super().__init__()

    def listen(self):
        listener = mouse.Listener(on_move=self.on_move,
                                  on_click=self.on_click,
                                  on_scroll=self.on_scroll)
        listener.start()

    def on_move(self, x, y):
        logger.debug(f"move&({x},{y})")
        self._signal.emit()

    def on_click(self, x, y, button, pressed):
        action = 'Pressed' if pressed else 'Released'
        sign = 0
        if pressed:
            sign = add_count_keymouse(button._name_, MOUSE_DeviceNo)
        logger.info(f"{button._name_}&{action}&({x},{y})&save_{sign}")
        self._signal.emit()

    def on_scroll(self, x, y, dx, dy):
        direction = f"({dx},{dy})"
        sign = add_count_keymouse(f"scroll_{direction}", MOUSE_DeviceNo)
        logger.info(f"scroll&({dx},{dy})&({x},{y})&save_{sign}")
        self._signal.emit()
