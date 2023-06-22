from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QStackedWidget
from PyQt5 import uic
from GUI.Screens.GeneratorScreen import GeneratorWidget
from GUI.Screens.TesterScreen import TesterWidget
from GUI.Screens.VisualizerScreen import VisualizerWidget
import sys


class StartWidget(QWidget):

    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)

        # load ui file:
        uic.loadUi("GUI/UI/StartUI.ui", self)


class UI(QMainWindow):
    def __init__(self, parent=None):
        super(UI, self).__init__()
        self.setWindowTitle('BMC Via Simulation')
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        # set up secondary widgets
        self.start_screen = StartWidget(self)
        self.generator_screen = GeneratorWidget(self)
        self.visualizer_screen = VisualizerWidget(self)
        self.tester_screen = TesterWidget(self)
        # add widgets to stack widget:
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.generator_screen)
        self.central_widget.addWidget(self.visualizer_screen)
        self.central_widget.addWidget(self.tester_screen)
        self.central_widget.setCurrentWidget(self.start_screen)
        # fix central widget visuals:
        self.setStyleSheet("background-color: rgb(160, 210, 235)")

        # setup signal connections:
        self.start_screen.BtnGenerator.clicked.connect(self.setGeneratorScreen)
        self.start_screen.BtnVisual.clicked.connect(self.setVisualizerScreen)
        self.start_screen.BtnTester.clicked.connect(self.setTesterScreen)
        self.generator_screen.BtnBack.clicked.connect(self.setStartScreen)
        self.visualizer_screen.BtnBack.clicked.connect(self.setStartScreen)
        self.tester_screen.BtnBack.clicked.connect(self.setStartScreen)

    def setGeneratorScreen(self):
        self.central_widget.setCurrentWidget(self.generator_screen)

    def setVisualizerScreen(self):
        self.central_widget.setCurrentWidget(self.visualizer_screen)

    def setStartScreen(self):
        self.central_widget.setCurrentWidget(self.start_screen)

    def setTesterScreen(self):
        self.tester_screen.populateComboBox()
        self.central_widget.setCurrentWidget(self.tester_screen)


# Initializing the app
app = QApplication(sys.argv)
UIWindow = UI()
# 670,150 = x,y for startup location, 800x500 = app resolution
UIWindow.setGeometry(670, 150, 800, 500)
UIWindow.show()
app.exec_()
