import random
from PyQt5 import uic
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QFileDialog

from Utils import VisualUtils
from Utils.SystemFactory import SystemFactory
from Utils.SystemUtils import SystemUtils


class GeneratorWidget(QWidget):
    def __init__(self, parent=None):
        super(GeneratorWidget, self).__init__(parent)
        self.generated_system = None
        self.system_name = None
        # load ui file:
        uic.loadUi("UI/GeneratorUI.ui", self)

        # hide irrelevant button
        self.BtnPreview.setVisible(False)
        self.BtnSave.setVisible(False)

        self.BtnGenerate.clicked.connect(self.generateBtnHandler)
        self.BtnSave.clicked.connect(self.saveBtnHandler)
        self.BtnPreview.clicked.connect(self.previewBtnHandler)
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

    def previewBtnHandler(self):
        VisualUtils.preview_system_new_window(self.generated_system)