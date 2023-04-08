from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMenuBar, QStatusBar, QWidget, \
    QStackedWidget, QSizePolicy
from PyQt5 import uic
import sys


class GeneratorWidget(QWidget):
    def __init__(self, parent=None):
        super(GeneratorWidget, self).__init__(parent)
        # load ui file:
        uic.loadUi("GeneratorUI.ui", self)


class StartWidget(QWidget):

    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)

        # load ui file:
        uic.loadUi("StartUI.ui", self)


class UI(QMainWindow):
    def __init__(self, parent=None):
        super(UI, self).__init__()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        # set up secondary widgets
        self.start_screen = StartWidget(self)
        self.generator_screen = GeneratorWidget(self)
        # add widgets to stack widget:
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.generator_screen)
        self.central_widget.setCurrentWidget(self.start_screen)
        # fix central widget visuals:
        self.setStyleSheet("background-color: rgb(160, 210, 235)")

        # setup signal connections:
        self.start_screen.BtnGenerator.clicked.connect(self.setGeneratorScreen)
        self.generator_screen.BtnBack.clicked.connect(self.setStartScreen)

    def setGeneratorScreen(self):
        self.central_widget.setCurrentWidget(self.generator_screen)

    def setStartScreen(self):
        self.central_widget.setCurrentWidget(self.start_screen)


# Initializing the app
app = QApplication(sys.argv)
UIWindow = UI()
# 670,150 = x,y for startup location, 800x500 = app resolution
UIWindow.setGeometry(670, 150, 800, 500)
UIWindow.show()
app.exec_()
