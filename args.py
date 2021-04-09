import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug",
                    type=int,
                    default=0,
                    choices=[0, 1],
                    help="debug? 0/1")
parser.add_argument("--localtime",
                    default=True,
                    type=bool,
                    choices=[True, False],
                    help="use localtime? True/False")

args = parser.parse_args()

KEYBOARD, MOUSE = "keyboard", "mouse"

KEYBOARD_DeviceNo = 1
MOUSE_DeviceNo = 0
TICKER_DeviceNo = -1
