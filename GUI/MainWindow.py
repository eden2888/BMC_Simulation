from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMenuBar, QStatusBar
from PyQt5 import uic
import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #load ui file:
        uic.loadUi("MainUI.ui", self)

        #link button clicks to relevant methods:
        self.BtnGenerator.clicked.connect(self.generatorButtonClicked)
        self.BtnTester.clicked.connect(self.testerButtonClicked)
        self.BtnVisual.clicked.connect(self.vusializeButtonClicked)

        # Show the app
        self.show()

    def generatorButtonClicked(self):
        print('generator button clicked')
    def testerButtonClicked(self):
        print('tester button clicked')
    def vusializeButtonClicked(self):
        print('visualize button clicked')

# Initializing the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()