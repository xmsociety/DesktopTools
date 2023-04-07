import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", type=int, default=0, choices=[0, 1], help="debug? 0/1")
parser.add_argument(
    "--localtime",
    default=True,
    type=bool,
    choices=[True, False],
    help="use localtime? True/False",
)
parser.add_argument(
    "--threshold", type=float, default=30, help="rest threshold? n /min"
)
parser.add_argument(
    "--work_buffer_len", type=int, default=60, help="work T rest buffer lenth. n /s"
)

args = parser.parse_args(args=[])

KEYBOARD, MOUSE = "keyboard", "mouse"

KEYBOARD_DeviceNo = 1
MOUSE_DeviceNo = 0
TICKER_DeviceNo = -1

ERROR_CATCH_NAME = -1

Alert_REST_MSG = "你该休息了."
Alert_REST_MUST_MSG = "您必须休息了！！！！"
Alert_REST_KEEP_MSG = "GoodJob, 继续保持."
Alert_LockWorkStation_MSG = "即将锁屏"

NUM_REST_KEEP_Alert = 3
