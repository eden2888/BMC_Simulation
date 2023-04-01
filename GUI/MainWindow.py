from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMenuBar, QStatusBar
from PyQt5 import uic
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #load ui file:
        uic.loadUi("MainUI.ui", self)

        # Show the app
        self.show()


# Initializing the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()