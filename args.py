import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", type=int, choices=[0, 1], help="debug? 0/1")

args = parser.parse_args()
