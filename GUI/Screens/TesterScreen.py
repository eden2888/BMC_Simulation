from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from z3 import unsat

from Utils import VisualUtils
from Utils.SystemUtils import SystemUtils


class TesterWidget(QWidget):

    def __init__(self, parent=None):
        super(TesterWidget, self).__init__(parent)

        # load ui file:
        uic.loadUi("GUI/UI/TesterUI.ui", self)
        self.LabelResults.hide()
        self.populateComboBox()
        self.BtnRun.clicked.connect(self.runTester)
        self.BtnPrev1.clicked.connect(lambda: self.previewSystem(1))
        self.BtnPrev2.clicked.connect(lambda: self.previewSystem(2))
        self.LineTimeout.setText('60')

    def runTester(self):
        sys1 = SystemUtils.load_system('c:\BMC_Systems\{}.json'.format(self.Sys1ComboBox.currentText()))
        sys2 = SystemUtils.load_system('c:\BMC_Systems\{}.json'.format(self.Sys2ComboBox.currentText()))
        predictive_sys1 = SystemUtils.create_predictive_kripke_structure(sys1)
        predictive_sys2 = SystemUtils.create_predictive_kripke_structure(sys2)
        checker = SystemUtils.check_simulation(predictive_sys1, sys2)
        res_text = str(checker.check())
        if checker.check() != unsat:
            res_text = res_text + '\n' + str(checker.model())
            res_text = res_text[:-1]
            text = res_text.split('[')[0].upper()
            res_lst = []
            mat_lst = res_text.split('[')[1].split(',')
            mat_lst[0] = '\n ' + mat_lst[0]
            for val in mat_lst:
                converted = val.replace('T', 'T[').replace(' =', '] =').replace('__', ',').replace('T[rue', 'True').replace('[T', 'T').replace(' T', 'T')
                res_lst.append(converted)
            for elle in sorted(res_lst):
                text += elle
            self.LabelResults.setText(text)
        else:
            self.LabelResults.setText('UNSAT')
        self.LabelResults.show()

    def populateComboBox(self):
        systems_lst = SystemUtils.get_all_systems_from_path()
        remove_ends = [lambda x: x[:-5] for x in systems_lst]
        for system in systems_lst:
            self.Sys1ComboBox.addItem(system[:-5])
            self.Sys2ComboBox.addItem(system[:-5])

    def previewSystem(self, sys_num):
        if sys_num == 1:
            sys_name = self.Sys1ComboBox.currentText()
        else:
            sys_name = self.Sys2ComboBox.currentText()
        system = SystemUtils.load_system('c:\BMC_Systems\{}.json'.format(sys_name))
        VisualUtils.preview_system_new_window(system)
