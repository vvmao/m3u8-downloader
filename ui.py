# !/usr/bin/env python36

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFrame
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPalette


class Launcher(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(Sider())
        hbox.addWidget(Content())
        self.setGeometry(300, 300, 300, 220)
        self.setStyleSheet("background-color:#333;")
        self.setWindowTitle("下载")
        self.show()

    def siderFrame(self):
        pass

def Sider(QFrame):
    def __init(self, *__args):
        super().__init__(*__args)
        self.setGeometry(0, 0, 60, 1000)


def Content(QFrame):
    def __init(self, *__args):
        super().__init__(*__args)
        self.initUI()


class SiderButton(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.initUI()

    def initUI(self):
        self.setFlat(True)
        self.setStyleSheet("color:#fff")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Launcher()
    sys.exit(app.exec())
