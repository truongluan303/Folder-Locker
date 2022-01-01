#!/usr/bin/env python

from folder_locker_ui import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
