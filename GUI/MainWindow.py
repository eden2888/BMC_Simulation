from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMenuBar, QStatusBar, QWidget
from PyQt5 import uic
import sys

generatorWidget = None


class GeneratorUI(QWidget):
    def __init__(self, mainWidget):
        super(GeneratorUI, self).__init__()
        # load ui file:
        uic.loadUi("GeneratorUI.ui", self)

        # connect back button logic:
        self.BtnBack.clicked.connect(self.backToMain)

    def backToMain(self):
        self.setCentralWidget(self.mainWidget)


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # load ui file:
        self.mainWidget = None
        uic.loadUi("MainUI.ui", self)

        # load generator widget:
        self.mainWidget = self.centralWidget()
        self.generatorWidget = GeneratorUI(self.mainWidget)
        # link button clicks to relevant methods:
        self.BtnGenerator.clicked.connect(self.generatorButtonClicked)
        self.BtnTester.clicked.connect(self.testerButtonClicked)
        self.BtnVisual.clicked.connect(self.vusializeButtonClicked)

        # Show the app
        self.show()

    def generatorButtonClicked(self):
        print('generator button clicked')
        self.mainWidget = self.takeCentralWidget()
        self.setCentralWidget(self.generatorWidget)

    def testerButtonClicked(self):
        print('tester button clicked')

    def vusializeButtonClicked(self):
        print('visualize button clicked')


# Initializing the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
