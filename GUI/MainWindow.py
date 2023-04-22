import random
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtGui import QFont, QValidator, QRegularExpressionValidator, QIntValidator

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QMenuBar, QStatusBar, QWidget, \
    QStackedWidget, QSizePolicy, QFileDialog, QGridLayout, QGroupBox, QDesktopWidget, QHBoxLayout, QMessageBox, \
    QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import uic
from PyQt5.QtCore import Qt, QRegularExpression
import matplotlib
from PyQt5.uic.properties import QtWidgets, QtCore
from z3 import unsat

from Utils import VisualUtils
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

        # set input validators:
        self.setInputValidators()

        # connect input boxes to validation handler:
        self.LineSysName.textChanged.connect(lambda: self.checkInputValidity(self.LineSysName))
        self.LineSysSize.textChanged.connect(lambda: self.checkInputValidity(self.LineSysSize))
        self.LineSysDensity.textChanged.connect(lambda: self.checkInputValidity(self.LineSysDensity))
        self.LineInitDensity.textChanged.connect(lambda: self.checkInputValidity(self.LineInitDensity))
        self.LineAttProb.textChanged.connect(lambda: self.checkInputValidity(self.LineAttProb))
        self.LineSysAttributes.textChanged.connect(lambda: self.checkInputValidity(self.LineSysAttributes))

        # assign randomize buttons to logic:
        self.BtnRndSize.clicked.connect(lambda: self.randomizeParameterValue(self.LineSysSize, 0, 1000))
        self.BtnRndRelDensity.clicked.connect(lambda: self.randomizeParameterValue(self.LineSysDensity, 0, 100))
        self.BtnRndInitDensity.clicked.connect(lambda: self.randomizeParameterValue(self.LineInitDensity, 0, 100))
        self.BtnRndAttProb.clicked.connect(lambda: self.randomizeParameterValue(self.LineAttProb, 0, 100))

    def checkInputValidity(self, lineEdit):
        if lineEdit.hasAcceptableInput() or lineEdit.text() == '':
            lineEdit.setStyleSheet('background-color: rgb(217, 226, 255)')
            self.BtnGenerate.setEnabled(True)
        else:
            lineEdit.setStyleSheet('background-color: red')
            self.BtnGenerate.setEnabled(False)

    def setInputValidators(self):
        # Validators setup:
        fileNameRegex = QRegularExpression('[\w]+$')
        attributeRegex = QRegularExpression('\w')
        nameValidator = QRegularExpressionValidator(fileNameRegex)
        attributeValidator = QRegularExpressionValidator(attributeRegex)
        intSizeValidator = QIntValidator(1, 1000)
        percentValidator = QIntValidator(0, 100)
        # Assign to line edits
        self.LineSysName.setPlaceholderText('System Name')
        self.LineSysName.setValidator(nameValidator)
        self.LineSysSize.setPlaceholderText('Number of nodes in the system (1-1000)')
        self.LineSysSize.setValidator(intSizeValidator)
        self.LineSysDensity.setPlaceholderText('Density in percents (0 - 100)')
        self.LineSysDensity.setValidator(percentValidator)
        self.LineInitDensity.setPlaceholderText('Density in percents (0 - 100)')
        self.LineInitDensity.setValidator(percentValidator)
        self.LineAttProb.setPlaceholderText('Probability in percents (0 - 100)')
        self.LineAttProb.setValidator(percentValidator)
        self.LineSysAttributes.setPlaceholderText('List of attributes: p,q,...')
        self.LineSysAttributes.setValidator(attributeValidator)

    def generateBtnHandler(self):
        # get input parameters
        self.system_name = self.LineSysName.text()
        system_size = int(self.LineSysSize.text())
        system_relation_density = int(self.LineSysDensity.text())
        initials_density = int(self.LineInitDensity.text())
        attributes = self.LineSysAttributes.text()
        attribute_prob = int(self.LineAttProb.text())

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

    def randomizeParameterValue(self, lineEdit, minVal, maxVal):
        lineEdit.setText(str(random.randint(minVal, maxVal)))


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
        grid.addWidget(self.canvas, 1, 0, Qt.AlignHCenter)
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
        self.LabelResults.hide()
        self.populateComboBox()
        self.BtnRun.clicked.connect(self.runTester)
        self.BtnPrev1.clicked.connect(lambda: self.previewSystem(1))
        self.BtnPrev2.clicked.connect(lambda: self.previewSystem(2))
        self.LineSubSysSize.setText('1')
        self.LineTimeout.setText('60')
    def runTester(self):
        sys1 = SystemUtils.load_system('c:\BMC_Systems\{}.json'.format(self.Sys1ComboBox.currentText()))
        sys2 = SystemUtils.load_system('c:\BMC_Systems\{}.json'.format(self.Sys2ComboBox.currentText()))
        checker = SystemUtils.check_simulation(sys1, sys2)
        res_text = str(checker.check())
        if checker.check() != unsat:
            res_text = res_text + '\n' + str(checker.model())
        self.LabelResults.setText(res_text)
        self.LabelResults.show()

    def populateComboBox(self):
        systems_lst = SystemUtils.get_all_systems_from_path()
        remove_ends = [lambda x: x[:-5] for x in systems_lst]
        for system in systems_lst:
            self.Sys1ComboBox.addItem(system[:-5])
            self.Sys2ComboBox.addItem(system[:-5])

    def previewSystem(self,sys_num):
        if sys_num == 1:
            sys_name = self.Sys1ComboBox.currentText()
        else:
            sys_name = self.Sys2ComboBox.currentText()
        print('c:\BMC_Systems\{}.json'.format(sys_name))
        system = SystemUtils.load_system('c:\BMC_Systems\{}.json'.format(sys_name))
        VisualUtils.preview_system_new_window(system)


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
        self.tester_screen.BtnBack.clicked.connect(self.setStartScreen)

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
