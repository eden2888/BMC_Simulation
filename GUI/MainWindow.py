import random
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMenuBar, QStatusBar, QWidget, \
    QStackedWidget, QSizePolicy, QFileDialog, QGridLayout, QGroupBox, QDesktopWidget, QHBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import uic
from PyQt5.QtCore import Qt
import matplotlib
from PyQt5.uic.properties import QtWidgets, QtCore
from Utils.VisualUtils import preview_system_test, preview_system
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
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
        self.verticalGroupBox = None
        self.canvas = None
        self.toolbar = None
        self.figure = None
        uic.loadUi("VisualizerUI.ui", self)
        # Buttons setup:
        self.BtnBack = QPushButton('< Back')
        self.BtnBack.setFixedSize(120, 30)
        font = QFont('Arial', 12)
        font.setBold(True)
        self.BtnBack.setFont(font)
        self.BtnSelect = QPushButton('Select System')
        self.BtnSelect.setFont(font)

        # init ui
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(20)
        self.setLayout(grid)
        self.figure = plt.figure(figsize=([16, 16]))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalGroupBox = QGroupBox()
        layout = QHBoxLayout()

        self.BtnSelect.setObjectName('BtnSelectSystem')
        layout.addWidget(self.toolbar)
        layout.addWidget(self.BtnSelect)
        layout.setSpacing(10)
        self.verticalGroupBox.setLayout(layout)
        self.verticalGroupBox.setMaximumHeight(100)
        self.BtnSelect.clicked.connect(self.select_file)

        toolbarLayout = QVBoxLayout()
        toolbarLayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        toolbarLayout.addWidget(self.verticalGroupBox)
        grid.addLayout(toolbarLayout, 0, 0)
        grid.addWidget(self.canvas, 1, 0,  Qt.AlignHCenter)
        grid.setRowStretch(1, 2)

        grid.addWidget(self.BtnBack, 3, 0)

        self.show()

    def select_file(self):
        dialog = QFileDialog(self)
        dialog.setDirectory('C:/')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Json Files (*.json)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            path = filenames[0]
            system = SystemUtils.load_system(path)
            if system is None:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Cannot open the selected file, please try again.')
                msg.setWindowTitle("Error Opening json file")
                msg.exec_()
            else:
                self.preview_system(system)

    def preview_system(self, system):
        G, node_names, colors_lst, plt1 = preview_system(system)
        self.figure.clf()
        nx.draw(G, with_labels=True, labels=node_names, node_size=800, node_color=colors_lst,
                pos=nx.kamada_kawai_layout(G))
        self.canvas.draw_idle()


class TesterWidget(QWidget):

    def __init__(self, parent=None):
        super(TesterWidget, self).__init__(parent)

        # load ui file:
        uic.loadUi("TesterUI.ui", self)


class StartWidget(QWidget):

    def __init__(self, parent=None):
        super(StartWidget, self).__init__(parent)

        # load ui file:
        uic.loadUi("StartUI.ui", self)


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

    def setGeneratorScreen(self):
        self.central_widget.setCurrentWidget(self.generator_screen)

    def setVisualizerScreen(self):
        self.central_widget.setCurrentWidget(self.visualizer_screen)

    def setStartScreen(self):
        self.central_widget.setCurrentWidget(self.start_screen)

    def setTesterScreen(self):
        self.central_widget.setCurrentWidget(self.tester_screen)

# Initializing the app
app = QApplication(sys.argv)
UIWindow = UI()
# 670,150 = x,y for startup location, 800x500 = app resolution
UIWindow.setGeometry(670, 150, 800, 500)
UIWindow.show()
app.exec_()
