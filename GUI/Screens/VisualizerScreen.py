import networkx as nx
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton, QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout, \
    QMessageBox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Utils.SystemUtils import SystemUtils
from Utils.VisualUtils import preview_system
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


class VisualizerWidget(QWidget):

    def __init__(self, parent=None):
        super(VisualizerWidget, self).__init__(parent)
        # load ui file:
        self.verticalGroupBox = None
        self.canvas = None
        self.toolbar = None
        self.figure = None
        uic.loadUi("UI/VisualizerUI.ui", self)
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
        dialog.setDirectory("C:\BMC_Systems")
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
