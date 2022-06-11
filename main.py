"""Main program contains, calculation of river discharge, level of water in the river
    and river cross section"""

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
import sys
import json
import math



class Ui_MainWindow(object):
    def __init__(self):
        self.dx = None
        self.L = None
        self.Mt = None
        self.Tt = None
        self.Tw = None
        self.x = None
        self.Nx = None
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot_data)
        with open('settings.json') as self.file:
            self.parameters = json.load(self.file)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("2D simulation of the flood wave")
        MainWindow.resize(785, 763)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 771, 401))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        # create a horizontal layout
        # Some random data for scatter plot
        self.x1 = list(range(100))  # 100 time points
        self.y1 = [randint(0, 100) for _ in range(100)]  # 100 data point

        self.x2 = list(range(100))  # 100 time points
        self.y2 = [randint(0, 10) for _ in range(100)]  # 100 data point

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.graphWidget = pg.GraphicsLayoutWidget()
        self.graphWidget.setBackground('w')

        #self.view1 = self.graphWidget.addViewBox(0,0)
        #self.view2 = self.graphWidget.addViewBox(1,0)
        self.graph_item1 = self.graphWidget.addPlot(row=0, col=0, x=self.x1, y=self.y1, pen=pg.mkPen('k',width=1.5))
        self.graph_item1.showGrid(x=True, y=True, alpha=0.3)
        self.graph_item2 = self.graphWidget.addPlot(row=1, col=0, x=self.x2, y=self.y2, pen=pg.mkPen('k',width=1.5))
        self.graph_item2.showGrid(x=True, y=True, alpha=0.3)
        self.curve1 = self.graph_item1.plot(pen=pg.mkPen('k', width=1.5))
        self.curve2 = self.graph_item2.plot(pen=pg.mkPen('k', width=1.5))
        #self.view1.addItem(self.graph_item1)
        #self.view2.addItem(self.graph_item2)
        self.horizontalLayout_4.addWidget(self.graphWidget)

        # end of horizontal layout
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(0, 630, 761, 71))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.defaultsButton = QtWidgets.QPushButton(self.frame_3, clicked=lambda: self.default())
        self.defaultsButton.setGeometry(QtCore.QRect(544, 20, 165, 40))
        self.defaultsButton.setObjectName("defaultsButton")
        self.startButton = QtWidgets.QPushButton(self.frame_3, clicked=lambda: self.timer.start())
        self.startButton.setEnabled(True)
        self.startButton.setGeometry(QtCore.QRect(30, 20, 165, 40))
        self.startButton.setObjectName("startButton")
        self.stopButton = QtWidgets.QPushButton(self.frame_3, clicked = lambda: self.timer.stop())
        self.stopButton.setGeometry(QtCore.QRect(373, 20, 165, 40))
        self.stopButton.setObjectName("stopButton")
        self.pauseButton = QtWidgets.QPushButton(self.frame_3, clicked = lambda: self.timer.stop())
        self.pauseButton.setGeometry(QtCore.QRect(201, 20, 166, 40))
        self.pauseButton.setObjectName("pauseButton")
        self.channelText = QtWidgets.QTextEdit(self.frame)
        self.channelText.setGeometry(QtCore.QRect(110, 410, 121, 31))
        self.channelText.setObjectName("channelText")
        self.channelText.setPlaceholderText(str(self.parameters['L']))
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 410, 101, 31))
        self.label_2.setObjectName("label_2")
        self.ChannelWidthText = QtWidgets.QTextEdit(self.frame)
        self.ChannelWidthText.setGeometry(QtCore.QRect(110, 450, 121, 31))
        self.ChannelWidthText.setObjectName("ChannelWidthText")
        self.ChannelWidthText.setPlaceholderText(str(self.parameters['B']))
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 450, 101, 31))
        self.label_3.setObjectName("label_3")
        self.BottomText = QtWidgets.QTextEdit(self.frame)
        self.BottomText.setGeometry(QtCore.QRect(110, 490, 121, 31))
        self.BottomText.setObjectName("BottomText")
        self.BottomText.setPlaceholderText(str(self.parameters['S0']))
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 490, 101, 31))
        self.label_4.setObjectName("label_4")
        self.CoeffText = QtWidgets.QTextEdit(self.frame)
        self.CoeffText.setGeometry(QtCore.QRect(110, 530, 121, 31))
        self.CoeffText.setObjectName("CoeffText")
        self.CoeffText.setPlaceholderText(str(self.parameters['n']))
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(10, 520, 91, 41))
        self.label_5.setScaledContents(False)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.GravityText = QtWidgets.QTextEdit(self.frame)
        self.GravityText.setGeometry(QtCore.QRect(110, 570, 121, 31))
        self.GravityText.setObjectName("GravityText")
        self.GravityText.setPlaceholderText(str(self.parameters['g']))
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(10, 570, 91, 41))
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(250, 410, 101, 31))
        self.label_7.setObjectName("label_7")
        self.DxText = QtWidgets.QTextEdit(self.frame)
        self.DxText.setGeometry(QtCore.QRect(350, 410, 121, 31))
        self.DxText.setObjectName("DxText")
        self.DxText.setPlaceholderText(str(self.parameters['dx']))
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setGeometry(QtCore.QRect(250, 570, 101, 31))
        self.label_8.setObjectName("label_8")
        self.WaveAmpText = QtWidgets.QTextEdit(self.frame)
        self.WaveAmpText.setGeometry(QtCore.QRect(350, 490, 121, 31))
        self.WaveAmpText.setObjectName("WaveAmpText")
        self.WaveAmpText.setPlaceholderText(str(self.parameters['a']))
        self.DtText = QtWidgets.QTextEdit(self.frame)
        self.DtText.setGeometry(QtCore.QRect(350, 450, 121, 31))
        self.DtText.setObjectName("DtText")
        self.DtText.setPlaceholderText(str(self.parameters['Dt']))
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(250, 530, 91, 31))
        self.label_9.setScaledContents(False)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.WavePeriodText = QtWidgets.QTextEdit(self.frame)
        self.WavePeriodText.setGeometry(QtCore.QRect(350, 530, 121, 31))
        self.WavePeriodText.setObjectName("WavePeriodText")
        self.WavePeriodText.setPlaceholderText(str(self.parameters['Tpw']))
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(250, 450, 101, 31))
        self.label_10.setObjectName("label_10")
        self.TimeBeforeText = QtWidgets.QTextEdit(self.frame)
        self.TimeBeforeText.setGeometry(QtCore.QRect(350, 570, 121, 31))
        self.TimeBeforeText.setObjectName("TimeBeforeText")
        self.TimeBeforeText.setPlaceholderText(str(self.parameters['Ts']))
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(250, 490, 101, 31))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(500, 410, 101, 31))
        self.label_12.setObjectName("label_12")
        self.TimeAfterText = QtWidgets.QTextEdit(self.frame)
        self.TimeAfterText.setGeometry(QtCore.QRect(600, 410, 121, 31))
        self.TimeAfterText.setObjectName("TimeAfterText")
        self.TimeAfterText.setPlaceholderText(str(self.parameters['Ta']))
        self.ABoundaryText = QtWidgets.QTextEdit(self.frame)
        self.ABoundaryText.setGeometry(QtCore.QRect(600, 490, 121, 31))
        self.ABoundaryText.setObjectName("ABoundaryText")
        self.ABoundaryText.setPlaceholderText(str(self.parameters['At1']))
        self.QBoundaryText = QtWidgets.QTextEdit(self.frame)
        self.QBoundaryText.setGeometry(QtCore.QRect(600, 450, 121, 31))
        self.QBoundaryText.setObjectName("QBoundaryText")
        self.QBoundaryText.setPlaceholderText(str(self.parameters['Qt1']))
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setGeometry(QtCore.QRect(500, 530, 91, 31))
        self.label_14.setScaledContents(False)
        self.label_14.setWordWrap(True)
        self.label_14.setObjectName("label_14")
        self.RiverDischargeText = QtWidgets.QTextEdit(self.frame)
        self.RiverDischargeText.setGeometry(QtCore.QRect(600, 530, 121, 31))
        self.RiverDischargeText.setObjectName("RiverDischargeText")
        self.RiverDischargeText.setPlaceholderText(str(self.parameters['Q0']))
        self.label_15 = QtWidgets.QLabel(self.frame)
        self.label_15.setGeometry(QtCore.QRect(500, 450, 101, 31))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(500, 490, 101, 31))
        self.label_16.setObjectName("label_16")
        # self.comboBox = QtWidgets.QComboBox(self.frame)
        # self.comboBox.setGeometry(QtCore.QRect(600, 570, 121, 31))
        # self.comboBox.setObjectName("comboBox")
        # self.comboBox.addItem("")
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setGeometry(QtCore.QRect(500, 570, 91, 31))
        self.label_17.setScaledContents(False)
        self.label_17.setWordWrap(True)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 785, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.file.close()

    def default(self):
        self.channelText.clear()
        self.ChannelWidthText.clear()
        self.BottomText.clear()
        self.CoeffText.clear()
        self.GravityText.clear()
        self.DxText.clear()
        self.WaveAmpText.clear()
        self.DtText.clear()
        self.WavePeriodText.clear()
        self.TimeBeforeText.clear()
        self.TimeAfterText.clear()
        self.ABoundaryText.clear()
        self.QBoundaryText.clear()
        self.RiverDischargeText.clear()
        # self.comboBox.clear()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "2D simulation of the flood wave"))
        self.defaultsButton.setText(_translate("MainWindow", "Defaults"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.pauseButton.setText(_translate("MainWindow", "Pause"))
        self.label_2.setText(_translate("MainWindow", "Channel length [m]:"))
        self.label_3.setText(_translate("MainWindow", "Channel width [m]:"))
        self.label_4.setText(_translate("MainWindow", "Bottom slope:"))
        self.label_5.setText(_translate("MainWindow", "Manning roughness coeff [m^2(-1/3)s]:"))
        self.label_6.setText(_translate("MainWindow", "Gravitation Acceleration      [m/s^2]:"))
        self.label_7.setText(_translate("MainWindow", "Step size (dx) [m]:"))
        self.label_8.setText(_translate("MainWindow", "Time before flood:"))
        self.label_9.setText(_translate("MainWindow", "Flood wave period [h]:"))
        self.label_10.setText(_translate("MainWindow", "Time step (dt) [sec]:"))
        self.label_11.setText(_translate("MainWindow", "Wave amplitude [m]:"))
        self.label_12.setText(_translate("MainWindow", "Time after flood:"))
        self.label_14.setText(_translate("MainWindow", "Initial river discharge:"))
        self.label_15.setText(_translate("MainWindow", "Q boundary value:"))
        self.label_16.setText(_translate("MainWindow", "A boundary value:"))
        # self.comboBox.setItemText(0, _translate("MainWindow", "sin"))
        # self.label_17.setText(_translate("MainWindow", "Flood function:"))
        # self.plotOnCanvas()

    def checkIfValueIsChanged(self, parameter, parameter_key):
        if parameter and parameter != self.parameters[parameter_key]:
            return int(parameter)
        return self.parameters[parameter_key]

    def calculateVariables(self):
        # number of cross sections:
        self.L = self.checkIfValueIsChanged(self.channelText.toPlainText(), 'L')
        self.dx = self.checkIfValueIsChanged(self.DxText.toPlainText(), 'dx')
        self.Nx = int(self.L / self.dx) + 1
        # number of cross section stations
        self.x = [400 * x for x in range(0, self.Nx - 1)]
        # maximum time required for the entrance of the flood wave into the channel
        self.Tw = self.checkIfValueIsChanged(self.WavePeriodText.toPlainText(), 'Tpw') / 2
        # total time of simulation
        self.Tt = self.checkIfValueIsChanged(self.TimeBeforeText.toPlainText(), 'Ts') \
                  + self.Tw \
                  + self.checkIfValueIsChanged(self.TimeAfterText.toPlainText(), 'Ta')
        # total number of time steps
        self.Mt = math.floor(self.Tt * 3600 / self.checkIfValueIsChanged(self.DtText.toPlainText(), 'Dt'))
        # TODO: calculate the rest of parameters (starting from page 15: Mt to yl2)

    def update_plot_data(self):
        self.x1 = self.x1[1:]  # Remove the first y element.
        self.x1.append(self.x1[-1] + 1)  # Add a new value 1 higher than the last.

        self.y1 = self.y1[1:]  # Remove the first
        self.y1.append(randint(0, 100))  # Add a new random value

        self.x2 = self.x2[1:]  # Remove the first y element.
        self.x2.append(self.x2[-1] + 1)  # Add a new value 1 higher than the last.

        self.y2 = self.y2[1:]  # Remove the first
        self.y2.append(randint(0, 10))  # Add a new random value

        self.curve1.setData(self.x1, self.y1)
        self.curve2.setData(self.x2, self.y2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
