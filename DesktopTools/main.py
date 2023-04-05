import sys

from PySide6.QtWidgets import QApplication

from .windows_main import WinMain

app = QApplication(sys.argv)


def main():
    screen = app.primaryScreen().geometry()
    _ = WinMain(screen, app=app)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
