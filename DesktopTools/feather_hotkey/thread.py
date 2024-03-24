import sys
from pynput import keyboard
from PySide6.QtCore import QByteArray, QThread, Signal, QAbstractNativeEventFilter
from ..logger import logger

if sys.platform == "win32":
    import ctypes
    import win32con
    user32 = ctypes.windll.user32

class NativeEvent(QAbstractNativeEventFilter):
    def __init__(self, hotkey) -> None:
        super().__init__()
        self.hotkey = hotkey

    def nativeEventFilter(self, eventType: QByteArray | bytes, message: int) -> object:
        if sys.platform == "win32":
            from ctypes import wintypes
            import win32con
            msg = wintypes.MSG.from_address(message.__init__())
            if eventType == "windows_generic_MSG" and msg.message == win32con.WM_HOTKEY:
                self.hotkey.on_activate()
        return super().nativeEventFilter(eventType, message)


class SignalHotKey(QThread):
    _signal = Signal()

    def __init__(self):
        super().__init__()
        self.hotkey_id = 1
        self.hotkey_vk = 0x31
        # win: https://learn.microsoft.com/zh-cn/windows/win32/inputdev/virtual-key-codes

    def register(self):
        if sys.platform == "win32":
            sign = user32.RegisterHotKey(None, self.hotkey_id, win32con.MOD_ALT, self.hotkey_vk)
            # https://learn.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-registerhotkey
            logger.info(f"Hotkey Registration {sign}")
            self.parent().installEventFilter(NativeEvent(hotkey=self))
        else:
            # sys.platform in ("linux", "darwin"):
            # 还没原生的方法,只能用`pynput`啦
            hotkey = keyboard.GlobalHotKeys(
                {
                    "<ctrl>+1": self.on_activate,
                    # "<ctrl>+<alt>+g": lambda: print("Goodbye"),
                }
            )
            hotkey.start()

    def unregister(self):
        if sys.platform == "win32" and self.hotkey_id:
            sign = user32.UnregisterHotKey(None, self.hotkey_id)
            logger.info(f"Hotkey unregistration {sign}")
        else:
            pass

    def on_activate(self):
        self._signal.emit()
