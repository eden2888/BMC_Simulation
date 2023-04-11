from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMenuBar, QStatusBar, QWidget, \
    QStackedWidget, QSizePolicy, QFileDialog
from PyQt5 import uic
import sys

from Utils.SystemFactory import SystemFactory
from Utils.SystemUtils import SystemUtils


class GeneratorWidget(QWidget):
    def __init__(self, parent=None):
        super(GeneratorWidget, self).__init__(parent)
        self.generated_system = None
        self.system_name = None
        # load ui file:
        uic.loadUi("GeneratorUI.ui", self)

        # hide irrelevant button
        self.BtnPreview.setVisible(False)
        self.BtnSave.setVisible(False)

        self.BtnGenerate.clicked.connect(self.generateBtnHandler)
        self.BtnSave.clicked.connect(self.saveBtnHandler)

    def generateBtnHandler(self):
        # get input parameters
        self.system_name = self.LineSysName.text()
        system_size = int(self.LineSysSize.text())
        system_relation_density = int(self.LineSysDensity.text())
        initials_density = int(self.LineInitDensity.text())
        attributes = self.LineSysAttributes.text()
        attribute_prob = int(self.LineAttProb.text())

        print('generated btn clicked !')
        # input validation - later

        # generate system using system factory
        ks = SystemFactory.create_system(density=system_relation_density, size=system_size, attribute=attributes,
                                         initials_density=initials_density, attribute_probability=attribute_prob)
        # store generated system object
        self.generated_system = ks

    def saveBtnHandler(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save generated system", self.system_name, "json (*.json)")
        if fileName:
            SystemUtils.save_system(self.generated_system, fileName)
            print('Stored successfully')


class VisualizerWidget(QWidget):

    def __init__(self, parent=None):
        super(VisualizerWidget, self).__init__(parent)

        # load ui file:
        uic.loadUi("VisualizerUI.ui", self)


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
        self.visualizer_screen = VisualizerWidget(self)
        # add widgets to stack widget:
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.generator_screen)
        self.central_widget.addWidget(self.visualizer_screen)
        self.central_widget.setCurrentWidget(self.start_screen)
        # fix central widget visuals:
        self.setStyleSheet("background-color: rgb(160, 210, 235)")

        # setup signal connections:
        self.start_screen.BtnGenerator.clicked.connect(self.setGeneratorScreen)
        self.start_screen.BtnVisual.clicked.connect(self.setVisualizerScreen)
        self.generator_screen.BtnBack.clicked.connect(self.setStartScreen)

    def setGeneratorScreen(self):
        self.central_widget.setCurrentWidget(self.generator_screen)

    def setVisualizerScreen(self):
        self.central_widget.setCurrentWidget(self.visualizer_screen)

    def setStartScreen(self):
        self.central_widget.setCurrentWidget(self.start_screen)


# Initializing the app
app = QApplication(sys.argv)
UIWindow = UI()
# 670,150 = x,y for startup location, 800x500 = app resolution
UIWindow.setGeometry(670, 150, 800, 500)
UIWindow.show()
app.exec_()
