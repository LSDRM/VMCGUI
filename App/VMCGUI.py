##############
### VMCGUI ###
##############

# GitHub : https://github.com/LSDRM/VMCGUI
# Contributor : Corentin COUTELLIER (https://github.com/B137P107)
# Initiated at : CEA/Laboratory Structure and Dynamics by Magnetic Resonance
# Date : 2023/12/07
# Version : 1.0

import icons
import importlib
import pyqtgraph as pg
import numpy as np
import math
import sys
import os
import re
import time
import operator
import _globals
from datetime import datetime
from scipy.signal import savgol_filter
from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.suffix = ".kit"
        self.dir = ""
        self.dirMem = self.dir
        self.dirOk = False
        self.recON = False
        self.showSetup = False
        self.allowShow = True
        self.sampleUnitMultiplier = 1
        self.totalUnitMultiplier = 1
        self.lineFaultCounter = 0
        
        self.toolBar = QtWidgets.QToolBar("Main Toolbar")           # Set the toolbar
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar.addAction("Select another kit", self.showSetupWindow)
        self.toolBar.addSeparator()
        self.toolBar.addAction("Load Data", SetupWindow.showDataPlot)
        self.toolBar.addSeparator()
        self.toolBar.addAction("Select directory", self.getDir)
        self.dirPathLabel = QtWidgets.QLabel("")
        self.dirPathLabel.setStyleSheet("border: 1px solid black;")
        self.dirPathLabel.setMaximumWidth(300)
        self.toolBar.addWidget(self.dirPathLabel)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(QtWidgets.QLabel(" File name : "))
        self.fileNameText = QtWidgets.QLineEdit()
        self.fileNameText.setMaxLength(30)
        self.fileNameText.setMaximumWidth(300)
        self.toolBar.addWidget(self.fileNameText)
        self.toolBar.addSeparator()
        self.recButton = QtWidgets.QToolButton(self)
        self.recButton.setIcon(QtGui.QIcon(":/REC.png"))
        self.recButton.setText(" REC")
        self.recButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        #self.recButton.setCheckable(True)
        self.recButton.clicked.connect(self.setupRec)
        self.toolBar.addWidget(self.recButton)
        self.updateFileButton = QtWidgets.QPushButton(self)
        self.updateFileButton.setText("Update File Manually")
        self.updateFileButton.setEnabled(False)
        self.updateFileButton.clicked.connect(self.updateFile)
        self.toolBar.addWidget(self.updateFileButton)
        self.toolBar.addWidget(QtWidgets.QLabel(" Auto update file : "))
        self.autoUpdateFile = QtWidgets.QCheckBox()
        self.autoUpdateFile.setChecked(True)
        self.autoUpdateFile.setEnabled(False)
        self.autoUpdateFile.stateChanged.connect(lambda: self.updateFileButton.setEnabled(self.recON and not self.autoUpdateFile.isChecked()))
        self.toolBar.addWidget(self.autoUpdateFile)
        self.toolBar.setIconSize(QtCore.QSize(20,20))
        
        self.graphToolBar = QtWidgets.QToolBar("Graph Toolbar")     # Set the graph toolbar
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.graphToolBar)
        self.graphToolBar.addWidget(QtWidgets.QLabel(" Sample Time : "))
        self.sampleTime = QtWidgets.QSpinBox()
        self.sampleTime.setRange(500, 1000)
        self.sampleTime.setKeyboardTracking(False)
        self.sampleTime.valueChanged.connect(self.update_sample_time)
        self.graphToolBar.addWidget(self.sampleTime)
        self.sampleTimeUnit = QtWidgets.QComboBox()
        self.sampleTimeUnit.addItems(["ms", "s", "min", "hour", "day"])
        self.sampleTimeUnit.currentTextChanged.connect(self.update_sample_time_unit)
        self.graphToolBar.addWidget(self.sampleTimeUnit)
        self.graphToolBar.addSeparator()
        self.graphToolBar.addWidget(QtWidgets.QLabel(" Total Time : "))
        self.totalTime = QtWidgets.QSpinBox()
        self.totalTime.setRange(2, 600)
        self.totalTime.setKeyboardTracking(False)
        self.totalTime.valueChanged.connect(self.update_total_time)
        self.graphToolBar.addWidget(self.totalTime)
        self.totalTimeUnit = QtWidgets.QComboBox()
        self.totalTimeUnit.addItems(["s", "min", "hour", "day"])
        self.totalTimeUnit.currentTextChanged.connect(self.update_total_time_unit)
        self.graphToolBar.addWidget(self.totalTimeUnit)
        self.graphToolBar.addSeparator()
        self.clearGraphButton = QtWidgets.QPushButton(self)
        self.clearGraphButton.setText("Clear Graphs")
        self.clearGraphButton.clicked.connect(self.clearGraph)
        self.graphToolBar.addWidget(self.clearGraphButton)

        self.totalTime.setValue(10)
        self.totalTimeUnit.setCurrentText("min")
        self.sampleTime.setValue(200)
        self.sampleTimeUnit.setCurrentText("ms")

        self.yellow = pg.mkPen(color=(255, 255, 0))
        self.orange = pg.mkPen(color=(255, 165, 0), width=2)
        self.blue = pg.mkPen(color=(0, 0, 255))
        self.red = pg.mkPen(color=(255, 0, 0))


    def initCentralFrame(self):

        if not all(len(x) == self.sensorsNumber for x in (self.graphTitle, self.unitMemory)):       # Check if self.sensorsNumber is equal to len(self.graphTitle) and to len(self.unitMemory).
            raise ValueError("The number of sensors must be equal with the number of graph titles and measurement units.")

        self.ParametersLayout = []
        self.pltPrecision = []
        self.Parameters = []
        self.Splitter = []
        self.minBox = []
        self.maxBox = []
        self.Graph = []
        self.Data = []
        self.Unit = []
        self.OldUnit = []
        self.rowCount = []
        self.enableSmooth = []

        if self.GPIOsNumber != 0:
            self.initGPIOs()

        self.winLength = [QtWidgets.QSpinBox() for i in range(self.sensorsNumber)]
        self.order = [QtWidgets.QSpinBox() for i in range(self.sensorsNumber)]
        self.ySmooth = [[] for i in range(self.sensorsNumber)]

        self.mainFrame = QtWidgets.QWidget()
        self.leftWidget = QtWidgets.QWidget()
        self.rightWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QHBoxLayout(self.mainFrame)
        self.leftLayout = QtWidgets.QHBoxLayout(self.leftWidget)
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightWidget)

        self.setCentralWidget(self.mainFrame)

        if self.GPIOsNumber != 0:
            self.GPIOview = QtWidgets.QTabWidget(self)                                  # START - Initializing GPIO config box
            self.GPIOview.setIconSize(QtCore.QSize(16,16))
            self.applyGPIObutton = QtWidgets.QPushButton("Apply", self)
            self.applyGPIObutton.setFixedSize(75,25)
            self.applyGPIObutton.setDefault(True)
            self.applyGPIObutton.clicked.connect(lambda: self.applyGPIO(None))
            self.resetGPIObutton = QtWidgets.QPushButton("Reset", self)
            self.resetGPIObutton.setFixedSize(75,25)
            self.resetGPIObutton.clicked.connect(self.resetGPIO)
            self.buttonsLayout = QtWidgets.QHBoxLayout()
            self.buttonsLayout.addWidget(self.applyGPIObutton)
            self.buttonsLayout.addWidget(self.resetGPIObutton)
            self.buttonsLayout.setAlignment(self.applyGPIObutton, QtCore.Qt.AlignRight)
            self.rightLayout.addWidget(self.GPIOview)
            self.rightLayout.addLayout(self.buttonsLayout)
            for i in range(self.GPIOsNumber):
                self.GPIOlayoutContainer.append(QtWidgets.QWidget())
                self.GPIOtab.append(QtWidgets.QFormLayout(self.GPIOlayoutContainer[i]))
                self.enableGPIOcheck.append(QtWidgets.QCheckBox())
                self.enableGPIOcheck[i].stateChanged.connect(lambda: self.enableGPIO(None))
                self.enableGPIOcheck[i].setObjectName(str(i))
                self.GPIOtab[i].addRow("Enable", self.enableGPIOcheck[i])
                self.selectGPIOmode.append(QtWidgets.QComboBox())
                self.selectGPIOmode[i].addItems(["Input", "Output"])
                self.selectGPIOmode[i].currentTextChanged.connect(lambda: self.updateGPIOmode(None))
                self.selectGPIOmode[i].setObjectName(str(i))
                self.GPIOtab[i].addRow(self.selectGPIOmode[i])
                self.GPIOview.addTab(self.GPIOlayoutContainer[i], "GPIO " + str(i))     # END - Initializing GPIO config box
                self.GPIOview.setTabIcon(i, QtGui.QIcon(":/GPIOinactive.png"))
            for i in range(self.GPIOsNumber):
                self.updateGPIOmode(i)
            for i in range(self.GPIOsNumber):
                self.enableGPIO(i)

        for i in range(self.sensorsNumber):
            self.Graph.append(pg.PlotWidget(title=self.graphTitle[i], background=(60,60,60), axisItems={'bottom': pg.DateAxisItem()}))
            self.Parameters.append(QtWidgets.QGroupBox(title=self.graphTitle[i] + "Graph Settings"))

        self.topSplit = QtWidgets.QSplitter(QtCore.Qt.Horizontal)       # START - Initializing splitters
        self.bottomSplit = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.topAndBottomSplit = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.leftNrightMainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.leftNrightMainSplitter.addWidget(self.leftWidget)
        self.leftNrightMainSplitter.addWidget(self.rightWidget)
        self.mainLayout.addWidget(self.leftNrightMainSplitter)      # Adding a splitter to a layout, add also the widgets contained within the splitter to the layout.

        for i in range(self.sensorsNumber):
            if i == self.sensorsNumber-1 and self.sensorsNumber%2 != 0:
                self.Splitter.append(QtWidgets.QSplitter(QtCore.Qt.Vertical))
            else:
                self.Splitter.append(QtWidgets.QSplitter(QtCore.Qt.Horizontal))

            self.Splitter[i].addWidget(self.Graph[i])
            self.Splitter[i].addWidget(self.Parameters[i])

        for i in range(0, self.sensorsNumber, 2):
            self.topSplit.addWidget(self.Splitter[i])
        for i in range(1, self.sensorsNumber, 2):
            self.bottomSplit.addWidget(self.Splitter[i])
        self.topAndBottomSplit.addWidget(self.topSplit)
        self.topAndBottomSplit.addWidget(self.bottomSplit)

        if self.sensorsNumber%2 != 0:
            self.totalSplit = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
            self.totalSplit.addWidget(self.topAndBottomSplit)
            self.totalSplit.addWidget(self.Splitter[-1])
            self.leftLayout.addWidget(self.totalSplit)
        else:
            self.leftLayout.addWidget(self.topAndBottomSplit)           # END - Initializing splitters
        
        self.Splitter[-1].splitterMoved.connect(lambda: print("Yo"))

        for i in range(self.sensorsNumber):                         # Initialize Graph Parameters Boxes
            self.ParametersLayout.append(QtWidgets.QFormLayout())
            self.maxBox.append(QtWidgets.QDoubleSpinBox())
            self.maxBox[i].setMaximum(sys.float_info.max)
            self.maxBox[i].setMinimum(-sys.float_info.max)
            self.maxBox[i].setValue(40)
            self.maxBox[i].setDecimals(0)
            self.maxBox[i].setKeyboardTracking(False)
            self.minBox.append(QtWidgets.QDoubleSpinBox())
            self.minBox[i].setMaximum(sys.float_info.max)
            self.minBox[i].setMinimum(-sys.float_info.max)
            self.minBox[i].setValue(0)
            self.minBox[i].setDecimals(0)
            self.minBox[i].setKeyboardTracking(False)
            self.maxBox[i].valueChanged.connect(lambda: self.setMax(None))
            self.minBox[i].valueChanged.connect(lambda: self.setMin(None))
            self.pltPrecision.append(QtWidgets.QSpinBox())
            self.pltPrecision[i].setMinimum(0)
            self.pltPrecision[i].setMaximum(323)
            self.pltPrecision[i].valueChanged.connect(lambda: self.setPlotPrecision(None))
            self.Unit.append(QtWidgets.QComboBox())
            for name,val in self.unitMemory[i].items():
                self.Unit[i].addItem(name)
            self.Unit[i].currentTextChanged.connect(lambda: self.update_graph(None))
            self.OldUnit.append(self.Unit[i].currentText())

            self.enableSmooth.append(QtWidgets.QCheckBox())
            self.enableSmooth[i].setChecked(False)
            self.enableSmooth[i].stateChanged.connect(self.initSmooth)

            self.ParametersLayout[i].addRow("Max value :", self.maxBox[i])
            self.ParametersLayout[i].addRow("Min value :", self.minBox[i])
            self.ParametersLayout[i].addRow("Decimals :", self.pltPrecision[i])
            self.ParametersLayout[i].addRow("Unit :", self.Unit[i])
            self.ParametersLayout[i].addRow("Smoothing :", self.enableSmooth[i])    # By Savitzky-Golay method.
            self.rowCount.append(self.ParametersLayout[i].rowCount())
            self.Parameters[i].setLayout(self.ParametersLayout[i])
            self.maxBox[i].setObjectName(str(i))
            self.minBox[i].setObjectName(str(i))
            self.pltPrecision[i].setObjectName(str(i))
            self.Unit[i].setObjectName(str(i))
            self.enableSmooth[i].setObjectName(str(i))
        
        self.y = [[] for i in range(self.sensorsNumber)]    #y is a list of each graph vertical data (list of sensorsNumber lists)
        self.yLen = []                                      #yLen is a list that contains length of y[0], y[1], y[2], etc...
        self.time = []

        for i in range(self.sensorsNumber):          # Setting graphs features
            self.Graph[i].setMouseEnabled(x=False, y=True)
            self.Graph[i].setMenuEnabled(False)
            self.Data.append(self.Graph[i].plot(self.time, self.y[i], pen=self.orange))
            self.Graph[i].getAxis('left').setPen('w')
            self.Graph[i].getAxis('left').setTextPen('w')
            self.Graph[i].getAxis('bottom').setPen('w')
            self.Graph[i].getAxis('bottom').setTextPen('w')
            self.Graph[i].getAxis('bottom').setHeight(25)
            self.Graph[i].getAxis('bottom').setTickFont(QtGui.QFont().setWeight(50))
        

    def update_plot_data(self):
        # timePLUS = time.perf_counter()

        totalPoints = self.totalTimeMs / self.timer.interval()
        if len(self.time) < totalPoints:
            start = 0
        else:
            start = (len(self.time)-int(totalPoints)+1)

        self.time = self.time[start:]
        for i in range(self.sensorsNumber):
            self.y[i] = self.y[i][start:]

        self.get_measures(self.samplesPerBurst)

        self.yLen.clear()                                   # The following block ensure safe data plotting (same length for all lists)
        for i in range(self.sensorsNumber):                 # But it means that if one data is missed, all others are too (for one point)
            self.yLen.append(len(self.y[i]))
        while (sum(self.yLen) % self.sensorsNumber) != 0:   # Check if all y lists length are equals (to prevent measurement missing)
            for i in range(self.sensorsNumber):             # If not, all lists are adjusted by removing last data on longest(s) one(s)
                self.y[i] = self.y[i][:self.yLen[i-1]]      # This ensure a safe data plotting with x time list
                self.yLen[i] = len(self.y[i])
        if len(self.time) > len(self.y[0]):                 # len(x) must be same as len(y[all]) for plotting
            self.time = self.time[:-1]

        for i in range(self.GPIOsNumber):       # This block set the GPIOs for output mode
            try:
                if isinstance(self.outputModeConfig[i][1], str):
                    yData = self.y[self.graphTitle.index(self.outputModeConfig[i][1])][-1]  # Get the last y data from the selected graph, which the title is contained in self.outputModeConfig[i][1]
                    if yData >= self.outputModeConfig[i][2]:
                        if self.outputModeConfig[i][4] == "HIGH over limit":
                            self.autoSetGPIO(i, True)
                        elif self.outputModeConfig[i][4] == "LOW over limit":
                            self.autoSetGPIO(i, False)
                    elif yData < self.outputModeConfig[i][3]:
                        if self.outputModeConfig[i][4] == "HIGH over limit":
                            self.autoSetGPIO(i, False)
                        elif self.outputModeConfig[i][4] == "LOW over limit":
                            self.autoSetGPIO(i, True)
            except IndexError:
                pass


        if self.recON:
            self.writeMeasurements(-1)
            # timePLUS = time.perf_counter()
            if self.autoUpdateFile.isChecked():
                self.updateFile()
            # timeMINUS = time.perf_counter()
            # print(timeMINUS - timePLUS)
        
        for i in range(self.sensorsNumber):
            if self.enableSmooth[i].isChecked():
                self.winLength[i].setMaximum(len(self.time))
                if self.order[i].maximum() < 16:
                    if self.winLength[i].maximum() > 16:
                        self.order[i].setMaximum(16)
                    else:
                        self.order[i].setMaximum(self.winLength[i].maximum()-1)
                self.ySmooth[i] = savgol_filter(self.y[i], self.winLength[i].value(), self.order[i].value(), mode='mirror').tolist()
                self.Data[i].setData(self.time, self.ySmooth[i])
            else:
                self.Data[i].setData(self.time, self.y[i])   # Update the data plot.

        # timeMINUS = time.perf_counter()
        # print(timeMINUS - timePLUS)


    def applyGPIO(self, i=None):
        print("Applied")
        
        if i is None:
            target = range(self.GPIOsNumber)
        else:
            target = [i]

        for i in target:
            try:
                for n in range(self.sensorsNumber):
                    self.Graph[n].removeItem(self.upLimitLine[i])
                    self.Graph[n].removeItem(self.downLimitLine[i])
            except IndexError:
                pass
            
            if self.enableGPIOcheck[i].isChecked():
                self.GPIOmode[i] = self.selectGPIOmode[i].currentText()
                if self.GPIOmode[i] == "Input":
                    self.outputModeConfig[i] = []
                    self.inputModeConfig[i] = [         # Usage : self.inputModeConfig[GPIO_ID][parameter_line][0 or 1] -> to get checkbox or combobox from "Input" mode parameters.
                        [self.inputClearGraph[i].isChecked(), self.inputClearGraphWhen[i].currentText()],
                        [self.inputGetData[i].isChecked(), self.inputGetDataWhen[i].currentText()],
                        [self.inputNewRecordFile[i].isChecked(), self.inputNewRecordFileWhen[i].currentText()]
                    ]
                elif self.GPIOmode[i] == "Output":
                    self.inputModeConfig[i] = []
                    self.outputModeConfig[i] = [self.outputMode[i].currentText()]
                    if self.outputModeConfig[i][-1] == "Auto":
                        self.outputModeConfig[i].append(self.outputActiveOn[i].currentText())
                        if self.outputModeConfig[i][-1] == "REC":
                            self.outputModeConfig[i].append(self.outputREC_HighOrLow[i].currentText())
                            if self.outputModeConfig[i][-1] == "HIGH on REC":
                                self.autoSetGPIO(i, self.recON)
                            elif self.outputModeConfig[i][-1] == "LOW on REC":
                                self.autoSetGPIO(i, not self.recON)
                        else:
                            self.outputModeConfig[i].append(self.outputUpLimit[i].value())
                            self.outputModeConfig[i].append(self.outputDownLimit[i].value())
                            self.outputModeConfig[i].append(self.outputHighOrLow[i].currentText())
                            self.upLimitLine[i] = pg.InfiniteLine(pos=self.outputModeConfig[i][2], angle=0, pen=pg.mkPen(color=(0, 255, 255)), label="GPIO " + str(i) + " - Up limit", labelOpts={'movable':'True', 'color':(255,255,255)})
                            self.downLimitLine[i] = pg.InfiniteLine(pos=self.outputModeConfig[i][3], angle=0, pen=pg.mkPen(color=(0, 255, 255)), label="GPIO " + str(i) + " - Down limit", labelOpts={'movable':'True', 'color':(255,255,255)})
                            self.Graph[self.graphTitle.index(self.outputModeConfig[i][1])].addItem(self.upLimitLine[i], ignoreBounds=True)
                            self.Graph[self.graphTitle.index(self.outputModeConfig[i][1])].addItem(self.downLimitLine[i], ignoreBounds=True)
                    else:
                        self.outputModeConfig[i].append(self.outputManualSetButton[i].isChecked())

                else:
                    raise ValueError('self.GPIOmode[i] must be "Input" or "Output".')

        print(self.GPIOmode[0])
        print(self.inputModeConfig[0])
        print(self.outputModeConfig[0])


    def clearGraph(self):
        del self.time[:-1]
        for i in range(self.sensorsNumber):
            del self.y[i][:-1]


    def closeEvent(self, event):
        global setup

        try:
            self.GPIOparametersWindow.close()
        except AttributeError:
            pass

        if self.recON:
            aswr = int(Dialog(0x03))
            if aswr == QtWidgets.QMessageBox.Yes:
                self.start_stop_Rec()
                if self.showSetup:
                    setup.show()
                event.accept()
            elif aswr == QtWidgets.QMessageBox.No:
                event.ignore()
        else:
            if self.showSetup:
                try:
                    setup.show()
                except NameError:
                    pass
            event.accept()


    def enableGPIO(self, i=None):
        if i is None:
            i = int(self.sender().objectName())
        print("Enable checked " + str(i) + " : " + str(self.enableGPIOcheck[i].isChecked()))

        print(self.GPIOtab[i].rowCount())
        for n in range(self.GPIOtab[i].rowCount() - 1):     # This loop enable or disable subwidgets under the enableGPIOcheck checkbox.
            print("This is n : " + str(n))
            try:
                self.GPIOtab[i].itemAt(n+1, QtWidgets.QFormLayout.FieldRole).widget().setEnabled(self.enableGPIOcheck[i].isChecked())
            except AttributeError:
                temp = self.GPIOtab[i].itemAt(n+1, QtWidgets.QFormLayout.FieldRole).layout()
                for x in range(temp.count()):
                    temp.itemAt(x).widget().setEnabled(self.enableGPIOcheck[i].isChecked())

        if self.enableGPIOcheck[i].isChecked():
            self.updateGPIOmode(i)
        else:
            if (self.GPIOmode[i] == "Output") and (self.checkGPIOstate(i)):
                self.autoSetGPIO(i, False)
            self.inputModeConfig[i] = []
            self.outputModeConfig[i] = []
            self.GPIOmode[i] = str
            self.applyGPIO()

        print(self.GPIOmode[0])
        print(self.inputModeConfig[0])
        print(self.outputModeConfig[0])


    def getDir(self):
        if self.recON == False:
            self.dirMem = self.dir
            self.dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select directory", "", QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks) + "/"
            if self.dir == "/":
                self.dir = self.dirMem      ##################################### NOT NEEDED ? ##########################################
            if self.dir == "":
                self.dirOk = False
            else:
                self.dirOk = True
            self.dirPathLabel.setText(self.dir)
        else:
            Dialog(0x01)


    def getFileName(self):
        if self.fileNameText.text() == "":
            self.fileName = datetime.now().strftime(self.prefix + "_%Y_%m_%d_%H_%M_%S_%f")[:-3]
            self.fileNameText.setText(self.fileName)
        else:
            self.fileName = self.fileNameText.text()


    def getLastTimestamp(self):
        self.file = open(self.dir + self.fileName + self.suffix, 'rb')

        pos = 0
        counter = 0
        while counter != 2:
            pos -= 1
            self.file.seek(pos, os.SEEK_END)
            byte = self.file.read(1)
            if byte == b'\n':
                counter += 1

        lastTimestamp = float(self.file.readline().decode('utf-8').split()[0])
        self.file.close()

        return lastTimestamp


    def initGPIOs(self):
        self.GPIOtab = []
        self.GPIOlayoutContainer = []
        self.enableGPIOcheck = []
        self.selectGPIOmode = []

        self.GPIOmode = [str for i in range(self.GPIOsNumber)]
        self.inputModeConfig = [[] for i in range(self.GPIOsNumber)]
        self.outputModeConfig = [[] for i in range(self.GPIOsNumber)]

        self.upLimitLine = [[] for i in range(self.GPIOsNumber)]
        self.downLimitLine = [[] for i in range(self.GPIOsNumber)]

        self.outputMode = [QtWidgets.QComboBox() for i in range(self.GPIOsNumber)]
        self.outputActiveOn = [QtWidgets.QComboBox() for i in range(self.GPIOsNumber)]
        self.outputUpLimit = [QtWidgets.QDoubleSpinBox() for i in range(self.GPIOsNumber)]
        self.outputDownLimit = [QtWidgets.QDoubleSpinBox() for i in range(self.GPIOsNumber)]
        self.outputHighOrLow = [QtWidgets.QComboBox() for i in range(self.GPIOsNumber)]
        self.outputManualSetButton = [QtWidgets.QPushButton() for i in range(self.GPIOsNumber)]
        self.outputREC_HighOrLow = [QtWidgets.QComboBox() for i in range(self.GPIOsNumber)]
        self.inputClearGraph = [QtWidgets.QCheckBox() for i in range(self.GPIOsNumber)]
        self.inputClearGraphWhen = [QtWidgets.QComboBox() for i in range(self.GPIOsNumber)]
        self.inputClearGraphLayout = [QtWidgets.QHBoxLayout() for i in range(self.GPIOsNumber)]
        self.inputGetData = [QtWidgets.QCheckBox() for i in range(self.GPIOsNumber)]
        self.inputGetDataWhen = [QtWidgets.QComboBox() for i in range(self.GPIOsNumber)]
        self.inputGetDataLayout = [QtWidgets.QHBoxLayout() for i in range(self.GPIOsNumber)]

        self.inputNewRecordFile = [QtWidgets.QCheckBox() for i in range(self.GPIOsNumber)]
        self.inputNewRecordFileWhen = [QtWidgets.QComboBox() for i in range(self.GPIOsNumber)]
        self.inputNewRecordFileLayout = [QtWidgets.QHBoxLayout() for i in range(self.GPIOsNumber)]

        # self.outputActiveOn = [QtWidgets.QComboBox() for x in range(self.GPIOsNumber)]
        # for x in self.outputActiveOn:
        #     x.addItems(self.graphTitle)
        # self.outputOverValue = [QtWidgets.QDoubleSpinBox() for x in range(self.GPIOsNumber)]
        # for x in self.outputOverValue:
        #     x.setRange(-sys.float_info.max, sys.float_info.max)

        # for x in range(self.GPIOsNumber):
        #     self.GPIOmode.append({
        #             "Input" : [],
        #             "Output" : [("Active on : ", self.outputActiveOn[x]), ("Over value : ", self.outputOverValue[x])]
        #         })


    def initSmooth(self):
        i = int(self.sender().objectName())
        while self.ParametersLayout[i].rowCount() > self.rowCount[i]:
            self.ParametersLayout[i].removeRow(self.ParametersLayout[i].getWidgetPosition(self.enableSmooth[i])[0] + 1)
        
        self.ySmooth[i].clear()

        if self.enableSmooth[i].isChecked():
            self.winLength[i] = QtWidgets.QSpinBox()
            self.winLength[i].setRange(2, len(self.time))
            self.winLength[i].setValue(10)
            self.winLength[i].setAccelerated(True)
            self.winLength[i].setKeyboardTracking(False)
            self.winLength[i].valueChanged.connect(self.preserveWindowOrderIntegrity)
            self.order[i] = QtWidgets.QSpinBox()
            self.order[i].setRange(1, self.winLength[i].maximum()-1)
            self.order[i].setValue(1)
            self.order[i].setAccelerated(True)
            self.order[i].setKeyboardTracking(False)
            self.order[i].valueChanged.connect(self.preserveWindowOrderIntegrity)
            self.ParametersLayout[i].insertRow(self.ParametersLayout[i].getWidgetPosition(self.enableSmooth[i])[0] + 1, "Filter window length :", self.winLength[i])
            self.ParametersLayout[i].insertRow(self.ParametersLayout[i].getWidgetPosition(self.winLength[i])[0] + 1, "Polynomial order :", self.order[i])

            self.winLength[i].setObjectName(str(i) + ' wl')
            self.order[i].setObjectName(str(i) + ' po')


    def preserveWindowOrderIntegrity(self):
        sender = self.sender().objectName().split()
        i = int(sender[0])
        senderName = sender[1]

        if self.order[i].value() >= self.winLength[i].value():
            if senderName == 'wl':
                self.order[i].setValue(self.winLength[i].value() - 1)
            elif senderName == 'po':
                self.winLength[i].setValue(self.order[i].value() + 1)


    def resetGPIO(self):
        for i in range(self.GPIOsNumber):
            self.enableGPIOcheck[i].setChecked(False)


    def setGPIOicon(self, i, state):
        if state:
            self.GPIOview.setTabIcon(i, QtGui.QIcon(":/GPIOactive.png"))
        else:
            self.GPIOview.setTabIcon(i, QtGui.QIcon(":/GPIOinactive.png"))


    def setupRec(self):
        if self.dirOk == False:
            self.getDir()
        
        if self.dirOk == True:
            self.getFileName()
                
            if os.path.exists(self.dir + self.fileName + self.suffix) & (self.recON == False):
                aswr = int(Dialog(0x02))
                if aswr == QtWidgets.QMessageBox.Yes:
                    self.file = open(self.dir + self.fileName + self.suffix, "r")
                    self.emptyFile = bool(self.file.readline() == "")
                    self.file.close()
                    self.start_stop_Rec()
                elif aswr == QtWidgets.QMessageBox.No:
                    self.recButton.setChecked(False)
            else:
                self.emptyFile = True
                self.start_stop_Rec()
        else:
            Dialog(0x00)
            self.recButton.setChecked(False)


    def showSetupWindow(self):
        self.showSetup = True
        self.close()


    def start_stop_Rec(self):
        if self.recON == False:
            self.file = open(self.dir + self.fileName + self.suffix, "a")
            if self.emptyFile:
                lastTimestamp = 0
                self.file.write("Timestamp\t\t\t" + '\t\t\t'.join(self.graphTitle) + '\n\n')
            else:
                self.file.close()                                               # If the file where writting data is not empty,
                lastTimestamp = self.getLastTimestamp()                         # it is important to check if the last time of
                self.file = open(self.dir + self.fileName + self.suffix, "a")   # the file is not higher than the first one to
            for i in range(len(self.time)):                                     # append to the file.
                if self.time[i] > lastTimestamp:                                # This prevent to write two time the same data.
                    self.writeMeasurements(i)
            self.recON = True
            self.recButton.setIcon(QtGui.QIcon(":/PAUSE.png"))
            self.recButton.setText(" PAUSE")
        else:
            self.recON = False
            self.file.close()
            self.recButton.setIcon(QtGui.QIcon(":/REC.png"))
            self.recButton.setText(" REC")

        for i in range(self.GPIOsNumber):
            if self.enableGPIOcheck[i].isChecked() and self.GPIOmode[i] == "Output" and self.outputModeConfig[i][0] == "Auto" and self.outputModeConfig[i][1] == "REC":
                if self.outputModeConfig[i][-1] == "HIGH on REC":
                    self.autoSetGPIO(i, self.recON)
                elif self.outputModeConfig[i][-1] == "LOW on REC":
                    self.autoSetGPIO(i, not self.recON)

        self.fileNameText.setReadOnly(self.recON)
        self.updateFileButton.setEnabled(self.recON and not self.autoUpdateFile.isChecked())
        self.autoUpdateFile.setEnabled(self.recON)


    def update_graph(self, ID):
        if ID is None:
            ID = int(self.sender().objectName())

        if list(self.unitMemory[ID].values())[0] == 0:
            for i in range(len(self.y[ID])):    # Update temperature graph
                self.y[ID][i] = self.y[ID][i] - self.unitMemory[ID].get(self.OldUnit[ID]) + self.unitMemory[ID].get(self.Unit[ID].currentText())
        else:
            for i in range(len(self.y[ID])):    # Update pressure graph
                self.y[ID][i] = (self.y[ID][i] / self.unitMemory[ID].get(self.OldUnit[ID])) * self.unitMemory[ID].get(self.Unit[ID].currentText())
        self.OldUnit[ID] = self.Unit[ID].currentText()


    def update_sample_time(self):       ######################################################################################## En dessous
        self.update_total_time_unit()
        self.timer.setInterval(self.sampleTime.value() * self.sampleUnitMultiplier)


    def update_sample_time_unit(self):
        if self.sampleTimeUnit.currentText() == "ms":
            self.sampleTime.setRange(500, 1000)
            self.sampleUnitMultiplier = 1
        elif self.sampleTimeUnit.currentText() == "s":
            self.sampleTime.setRange(1, 600)
            self.sampleUnitMultiplier = 1000
        elif self.sampleTimeUnit.currentText() == "min":
            self.sampleTime.setRange(1, 300)
            self.sampleUnitMultiplier = 60000
        elif self.sampleTimeUnit.currentText() == "hour":
            self.sampleTime.setRange(1, 200)
            self.sampleUnitMultiplier = 3600000
        elif self.sampleTimeUnit.currentText() == "day":
            self.sampleTime.setRange(1, 91)
            self.sampleUnitMultiplier = 86400000
        self.update_total_time_unit()
        self.update_sample_time()


    def update_total_time(self):
        self.totalTimeMs = self.totalTime.value() * self.totalUnitMultiplier * 1000


    def update_total_time_unit(self):
        fourPointsTime = 4 * self.sampleTime.value() * self.sampleUnitMultiplier    # Duration time of 4 points in milliseconds
        if self.totalTimeUnit.currentText() == "s":
            if (fourPointsTime / 1000) >= 600:
                self.totalTime.setValue(10)
                self.totalTimeUnit.setCurrentText("min")
            else:
                self.totalTime.setRange(int(fourPointsTime / 1000) + 1, 600)
                self.totalUnitMultiplier = 1
        elif self.totalTimeUnit.currentText() == "min":
            if (fourPointsTime / 60000) >= 300:
                self.totalTime.setValue(5)
                self.totalTimeUnit.setCurrentText("hour")
            else:
                self.totalTime.setRange(int(fourPointsTime / 60000) + 1, 300)
                self.totalUnitMultiplier = 60
        elif self.totalTimeUnit.currentText() == "hour":
            if (fourPointsTime / 3600000) >= 200:
                self.totalTime.setValue(9)
                self.totalTimeUnit.setCurrentText("day")
            else:
                self.totalTime.setRange(int(fourPointsTime / 3600000) + 1, 200)
                self.totalUnitMultiplier = 3600
        elif self.totalTimeUnit.currentText() == "day":
            self.totalTime.setRange(int(fourPointsTime / 86400000) + 1, 365)
            self.totalUnitMultiplier = 86400
        self.update_total_time()        ######################################################################################## Au dessus


    def updateFile(self):
        self.file.close()
        self.file = open(self.dir + self.fileName + self.suffix, "a")


    def updateGPIOmode(self, i=None):
        if i is None:
            i = int(self.sender().objectName())
        print("Mode updated : " + str(i))

        while (self.GPIOtab[i].rowCount() - self.GPIOtab[i].getWidgetPosition(self.selectGPIOmode[i])[0] - 1) != 0:
            self.GPIOtab[i].removeRow(self.GPIOtab[i].getWidgetPosition(self.selectGPIOmode[i])[0] + 1)

        if self.selectGPIOmode[i].currentText() == "Input":
            # print(self.GPIOtab[i].rowCount())
            self.inputClearGraphLayout[i] = QtWidgets.QHBoxLayout()
            self.inputClearGraph[i] = QtWidgets.QCheckBox()
            self.inputClearGraph[i].stateChanged.connect(lambda: self.inputClearGraphWhen[i].setEnabled(self.inputClearGraph[i].isChecked()))
            self.inputClearGraphLayout[i].addWidget(self.inputClearGraph[i])
            self.inputClearGraphWhen[i] = QtWidgets.QComboBox()
            self.inputClearGraphWhen[i].addItems(["Rising edge", "Falling edge", "While HIGH", "While LOW"])
            self.inputClearGraphWhen[i].setEnabled(self.inputClearGraph[i].isChecked())
            self.inputClearGraphLayout[i].addWidget(self.inputClearGraphWhen[i])
            self.GPIOtab[i].addRow("Clear graphs : ", self.inputClearGraphLayout[i])

            self.inputGetDataLayout[i] = QtWidgets.QHBoxLayout()
            self.inputGetData[i] = QtWidgets.QCheckBox()
            self.inputGetData[i].stateChanged.connect(lambda: self.inputGetDataWhen[i].setEnabled(self.inputGetData[i].isChecked()))
            self.inputGetDataLayout[i].addWidget(self.inputGetData[i])
            self.inputGetDataWhen[i] = QtWidgets.QComboBox()
            self.inputGetDataWhen[i].addItems(["Rising edge", "Falling edge", "While HIGH", "While LOW"])
            self.inputGetDataWhen[i].setEnabled(self.inputGetData[i].isChecked())
            self.inputGetDataLayout[i].addWidget(self.inputGetDataWhen[i])
            self.GPIOtab[i].addRow("Get datas : ", self.inputGetDataLayout[i])

            self.inputNewRecordFileLayout[i] = QtWidgets.QHBoxLayout()
            self.inputNewRecordFile[i] = QtWidgets.QCheckBox()
            self.inputNewRecordFile[i].stateChanged.connect(lambda: self.inputNewRecordFileWhen[i].setEnabled(self.inputNewRecordFile[i].isChecked()))
            self.inputNewRecordFileLayout[i].addWidget(self.inputNewRecordFile[i])
            self.inputNewRecordFileWhen[i] = QtWidgets.QComboBox()
            self.inputNewRecordFileWhen[i].addItems(["Rising edge", "Falling edge", "While HIGH", "While LOW"])
            self.inputNewRecordFileWhen[i].setEnabled(self.inputNewRecordFile[i].isChecked())
            self.inputNewRecordFileLayout[i].addWidget(self.inputNewRecordFileWhen[i])
            self.GPIOtab[i].addRow("New record file : ", self.inputNewRecordFileLayout[i])

            # clearGraph
            # getData
            # record in new file
        else:
            self.outputMode[i] = QtWidgets.QComboBox()
            self.outputMode[i].addItems(["Auto", "Manual"])
            self.outputMode[i].currentTextChanged.connect(lambda: self.updateGPIOoutputMode(None))
            self.outputMode[i].setObjectName(str(i))
            self.GPIOtab[i].addRow("Mode : ", self.outputMode[i])
            self.updateGPIOoutputMode(i)


    def updateGPIOoutputActiveOn(self, i=None):
        if i is None:
            i = int(self.sender().objectName())

        while (self.GPIOtab[i].rowCount() - self.GPIOtab[i].getWidgetPosition(self.outputActiveOn[i])[0] - 1) != 0:
            self.GPIOtab[i].removeRow(self.GPIOtab[i].getWidgetPosition(self.outputActiveOn[i])[0] + 1)

        if self.outputActiveOn[i].currentText() == "REC":
            self.outputREC_HighOrLow[i] = QtWidgets.QComboBox()
            self.outputREC_HighOrLow[i].addItems(["HIGH on REC", "LOW on REC"])
            self.GPIOtab[i].addRow("Set : ", self.outputREC_HighOrLow[i])
        else:
            self.outputUpLimit[i] = QtWidgets.QDoubleSpinBox()
            self.outputUpLimit[i].setRange(-sys.float_info.max, sys.float_info.max)
            self.outputUpLimit[i].setDecimals(3)
            self.outputUpLimit[i].valueChanged.connect(lambda: self.updateGPIOoutputLimits())
            self.outputUpLimit[i].setObjectName(str(i) + " up")
            self.GPIOtab[i].addRow("Up limit : ", self.outputUpLimit[i])
            self.outputDownLimit[i] = QtWidgets.QDoubleSpinBox()
            self.outputDownLimit[i].setRange(-sys.float_info.max, sys.float_info.max)
            self.outputDownLimit[i].setDecimals(3)
            self.outputDownLimit[i].valueChanged.connect(lambda: self.updateGPIOoutputLimits())
            self.outputDownLimit[i].setObjectName(str(i) + " down")
            self.GPIOtab[i].addRow("Down limit : ", self.outputDownLimit[i])
            self.outputHighOrLow[i] = QtWidgets.QComboBox()
            self.outputHighOrLow[i].addItems(["HIGH over limit", "LOW over limit"])
            self.GPIOtab[i].addRow("Set : ", self.outputHighOrLow[i])


    def updateGPIOoutputLimits(self):
        senderInfos = self.sender().objectName().split()
        i = int(senderInfos[0])
        sender = senderInfos[1]

        try:
            if self.outputUpLimit[i].value() != self.upLimitLine[i].value():
                self.upLimitLine[i].setPen(pg.mkPen(color=(255,0, 0)))

            if self.outputDownLimit[i].value() != self.downLimitLine[i].value():
                self.downLimitLine[i].setPen(pg.mkPen(color=(255,0, 0)))
        except AttributeError:
            pass

        if self.outputUpLimit[i].value() < self.outputDownLimit[i].value():
            if sender == "up":
                self.outputDownLimit[i].setValue(self.outputUpLimit[i].value())
            elif sender == "down":
                self.outputUpLimit[i].setValue(self.outputDownLimit[i].value())


    def updateGPIOoutputMode(self, i=None):
        if i is None:
            i = int(self.sender().objectName())

        while (self.GPIOtab[i].rowCount() - self.GPIOtab[i].getWidgetPosition(self.outputMode[i])[0] - 1) != 0:
            self.GPIOtab[i].removeRow(self.GPIOtab[i].getWidgetPosition(self.outputMode[i])[0] + 1)

        if self.outputMode[i].currentText() == "Auto":
            self.outputActiveOn[i] = QtWidgets.QComboBox()
            self.outputActiveOn[i].addItems(self.graphTitle + ["REC"])
            self.outputActiveOn[i].currentTextChanged.connect(lambda: self.updateGPIOoutputActiveOn(None))
            self.outputActiveOn[i].setObjectName(str(i))
            self.GPIOtab[i].addRow("Active on : ", self.outputActiveOn[i])
            self.updateGPIOoutputActiveOn(i)
        elif self.outputMode[i].currentText() == "Manual":
            self.outputManualSetButton[i] = QtWidgets.QPushButton()
            self.outputManualSetButton[i].setText("Set HIGH")
            self.outputManualSetButton[i].setCheckable(True)
            self.outputManualSetButton[i].clicked.connect(lambda: self.manualSetGPIO(None))
            self.outputManualSetButton[i].setObjectName(str(i))
            self.GPIOtab[i].addRow(self.outputManualSetButton[i])
            self.manualSetGPIO(i)


    def binToVolt(self, binValue, REF):
        return (binValue / pow(2, 23)) * REF


    def setMax(self, ID):
        if ID is None:
            ID = int(self.sender().objectName())

        if self.maxBox[ID].value() < self.minBox[ID].value():
            self.minBox[ID].setValue(self.maxBox[ID].value())
        self.Graph[ID].setYRange(self.minBox[ID].value(), self.maxBox[ID].value())


    def setMin(self, ID):
        if ID is None:
            ID = int(self.sender().objectName())
        
        if self.maxBox[ID].value() < self.minBox[ID].value():
            self.maxBox[ID].setValue(self.minBox[ID].value())
        self.Graph[ID].setYRange(self.minBox[ID].value(), self.maxBox[ID].value())


    def setPlotPrecision(self, ID):
        if ID is None:
            ID = int(self.sender().objectName())

        prec = self.pltPrecision[ID].value()
        self.maxBox[ID].setDecimals(prec)
        self.minBox[ID].setDecimals(prec)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#


class DataPlot(QtWidgets.QMainWindow):

    def __init__(self, ID, *args, **kwargs):        # , xName, x, yName, y, 
        super(DataPlot, self).__init__(*args, **kwargs)
        
        self.refreshMode = False
        self.LoadData()

        if (self.fileName[0] == '') | self.unopenableFile:
            self.showData = False
            return

        # global DataWindow
        self.refreshMode = True
        self.showData = True
        self.bottomAxis = []
        self.leftAxis = []
        self.Graph = []
        self.Data = []
        self.viewLayout = []
        self.viewWidget = []
        self.Parameters = []
        self.parametersLayout = []
        self.enableDigitSmooth = []
        self.smoothingMethod = []
        self.crosshair_V = []
        self.crosshair_H = []
        self.posLabel = []

        self.filterWindowLength = []
        self.numberOfPoints = []
        self.splineDegree = []
        self.polyorder = []
        self.enableAdvancedSGF = []
        self.deriv = []
        self.delta = []
        self.mode = []
        self.cval = []
        self.SGFdocsButton = []
        self.initialSGFrowCount = []
        self.ySmooth = []
        self.timeSmooth = []
        self.newTabVariables(len(self.graphTitle))

        # self.filterWindowLength = [QtWidgets.QSpinBox() for i in range(len(self.graphTitle))]
        # self.polyorder = [QtWidgets.QSpinBox() for i in range(len(self.graphTitle))]
        # self.enableAdvancedSGF = [QtWidgets.QCheckBox() for i in range(len(self.graphTitle))]
        # self.deriv = [QtWidgets.QSpinBox() for i in range(len(self.graphTitle))]
        # self.SGFdocsButton = [QtWidgets.QPushButton() for i in range(len(self.graphTitle))]
        # self.initialSGFrowCount = [0 for i in range(len(self.graphTitle))]
        # self.ySmooth = [[] for i in range(len(self.graphTitle))]

        self.op = {
            '+' : operator.add,
            '-' : operator.sub,
            '*' : operator.mul,
            '/' : operator.truediv,
            '%' : operator.mod,
            '**' : operator.pow
        }

        self.setWindowTitle("VMCGUI - Data plot window - " + self.fileName[0])
        self.menu = QtWidgets.QMenuBar(self)
        self.viewMenu = QtWidgets.QMenu("View", self)
        self.menu.addMenu(self.viewMenu)
        self.menu.addAction("Refresh", self.LoadData)
        self.setMenuBar(self.menu)

        for i in range(len(self.graphTitle)):
            self.addGraphBox(i)

        self.setTabView()


    def LoadData(self):
        dialog = QtWidgets.QFileDialog(caption="Open File")
        self.unopenableFile = True
        if _globals.firstExec:
            _globals.url = QtCore.QUrl("clsid:0AC0837C-BBF8-452A-850D-79D08E667CA7")     # This refer to "Ce PC" shortcut, to more CLSID shortcut check https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid
            dialog.setDirectoryUrl(_globals.url)
        else:
            dialog.setDirectory(_globals.url)

        if not self.refreshMode:
            self.fileName = dialog.getOpenFileName(filter="Kit File (*.kit)")
        
        if self.fileName[0] != '':
            _globals.url = self.fileName[0]
            _globals.firstExec = False
            file = open(_globals.url, 'r')
            self.graphTitle = file.readline().split()
            if not self.graphTitle:
                Dialog(0x05)
                return
            self.unopenableFile = False
            self.xTitle = self.graphTitle[0]
            self.graphTitle = self.graphTitle[1:]

            self.time = []
            self.y = [[] for i in range(len(self.graphTitle))]

            for i in file:
                line = i.split()
                if line:
                    self.time.append(float(line[0]))
                    for x in range(len(self.graphTitle)):
                        self.y[x].append(float(line[x+1]))
            file.close()

            if self.refreshMode:
                self.refreshGraphs()


    def setTabView(self):
        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)

        for i in range(len(self.graphTitle)):
            self.tabWidget.addTab(self.viewWidget[i], self.graphTitle[i])

        self.tabPlus = QtWidgets.QToolButton(self)
        self.tabPlus.setText('+')
        font = self.tabPlus.font()
        font.setBold(True)
        self.tabPlus.setFont(font)
        self.tabWidget.setCornerWidget(self.tabPlus)
        self.tabPlus.clicked.connect(self.initNewGraph)


    def closestValue(self, input_list, input_value):
        arr = np.asarray(input_list)
        i = (np.abs(arr - input_value)).argmin()
        return arr[i]


    def updateCursorPos(self, pos):
        #mousePoint = p.vb.mapSceneToView(evt[0])
        i = int(self.sender().objectName())

        if self.Graph[i].sceneBoundingRect().contains(pos):
            mousePoint = self.Graph[i].getPlotItem().vb.mapSceneToView(pos)
            x = self.closestValue(self.Data[i].getData()[0].tolist(), mousePoint.x())               # Get the closet value of x in the Data list, from the mouse position.
            y = self.Data[i].getData()[1].tolist()[self.Data[i].getData()[0].tolist().index(x)]     # Get the y position of the curve, from the x position calculated previously.
            self.crosshair_V[i].setPos(x)
            self.crosshair_H[i].setPos(y)
            self.posLabel[i].setText("<span style='font-size: 10pt; color: white'> x = %s, <span style='color: white'> y = %0.2f</span>" % (datetime.fromtimestamp(x).time(), y))


    def addGraphBox(self, i):           ##########################################################################################################################################
        ##########################################################################################################################################################################
        self.leftAxis.append(pg.AxisItem('left', pen=pg.mkPen(color=(255, 255, 255))))      # Generate the graph
        self.bottomAxis.append(pg.DateAxisItem('bottom', pen=pg.mkPen(color=(255, 255, 255))))
        self.Graph.append(pg.PlotWidget(title=self.graphTitle[i], background='k', axisItems={'bottom': self.bottomAxis[i], 'left': self.leftAxis[i]}))
        self.Graph[i].setLimits(xMin=self.time[0], xMax=self.time[-1])
        self.Data.append(self.Graph[i].plot(self.time, self.y[i], pen=pg.mkPen(color=(255, 255, 0))))
        self.Data[i].sigPlotChanged.connect(self.YautoRange)
        self.Data[i].setObjectName(str(i))

        self.Graph[i].setAcceptHoverEvents(True)                                # To trace cursors
        self.Graph[i].scene().sigMouseMoved.connect(self.updateCursorPos)
        self.posLabel.append(pg.LabelItem("", self.Graph[i].getPlotItem(), color='#FFFF00'))#, size="36pt")
        self.posLabel[i].anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))
        self.crosshair_V.append(pg.InfiniteLine(angle=90, movable=False))
        self.crosshair_H.append(pg.InfiniteLine(angle=0, movable=False))
        self.Graph[i].addItem(self.crosshair_V[i], ignoreBounds=True)
        self.Graph[i].addItem(self.crosshair_H[i], ignoreBounds=True)

        self.Parameters.append(QtWidgets.QGroupBox(title="Graph Settings"))     # Generate the graph parameters box
        self.enableDigitSmooth.append(QtWidgets.QCheckBox())
        self.enableDigitSmooth[i].setChecked(False)
        self.enableDigitSmooth[i].stateChanged.connect(self.initDigitSmooth)
        self.smoothingMethod.append(QtWidgets.QComboBox())
        self.smoothingMethod[i].addItems(["Savitzky-Golay", "Interpolate"])
        self.smoothingMethod[i].setEnabled(False)
        self.smoothingMethod[i].currentTextChanged.connect(self.initDigitSmooth)
        self.parametersLayout.append(QtWidgets.QFormLayout())
        self.parametersLayout[i].addRow("Digital smoothing :", self.enableDigitSmooth[i])
        self.parametersLayout[i].addRow("Smoothing method :", self.smoothingMethod[i])
        self.Parameters[i].setLayout(self.parametersLayout[i])
        self.initialRowCount = self.parametersLayout[i].rowCount()

        self.enableDigitSmooth[i].setObjectName(str(i))     #####   B E   C A R E F U L   #####     enableInterlacing, enableDigitSmooth, pointsToInterlace and pointsToSmooth have the same objectName
        self.smoothingMethod[i].setObjectName(str(i))       #####        H E R E          #####     This, for the program, is usefull, but take care of it if any change you do     - Grand Master Yoda
        self.Graph[i].scene().setObjectName(str(i))

        self.viewLayout.append(QtWidgets.QHBoxLayout())     # Put the graph and parameters box in a layout
        self.viewLayout[i].addWidget(self.Graph[i])
        self.viewLayout[i].addWidget(self.Parameters[i])
        self.viewWidget.append(QtWidgets.QWidget())
        self.viewWidget[i].setLayout(self.viewLayout[i])


    def refreshGraphs(self):
        for i in range(len(self.graphTitle)):
            if self.enableDigitSmooth[i].isChecked():
                if self.smoothingMethod[i].currentText() == "Interpolate":
                    self.Graph[i].setLimits(xMin=self.timeSmooth[i][0], xMax=self.timeSmooth[i][-1])
                    self.Graph[i].setXRange(self.timeSmooth[i][0], self.timeSmooth[i][-1])
                    self.Data[i].setData(self.timeSmooth[i], self.ySmooth[i])
                else:
                    self.Graph[i].setLimits(xMin=self.time[0], xMax=self.time[-1])
                    self.Graph[i].setXRange(self.time[0], self.time[-1])
                    self.Data[i].setData(self.time, self.ySmooth[i])
            else:
                self.Graph[i].setLimits(xMin=self.time[0], xMax=self.time[-1])
                self.Graph[i].setXRange(self.time[0], self.time[-1])
                self.Data[i].setData(self.time, self.y[i])
            """liste = self.graphTitle[i].split()                   ########################################################################################################################
            if len(liste) > 1:
                ? = getPos(liste[1])                                ########################################################################################################################
                ?? = getPos(liste[2])
                self.y[i] = self.y[?] (*, +, -, ...) self.y[??]"""  ########################################################################################################################


    def initNewGraph(self):
        command = QtWidgets.QInputDialog.getText(self, "Generate a new graph", "Example : Pressure0 * Pressure1") #, QtWidgets.QLineEdit.Normal)      # Should open a window to configure the new graph
        if command[1]:
            if command[0] == '':
                Dialog(0x04)
            else:
                print(self.graphTitle)
                if command[0] in self.graphTitle:
                    i = self.graphTitle.index(command[0])
                    self.tabWidget.addTab(self.viewWidget[i], self.graphTitle[i])
                else:
                    arguments = command[0].split()
                    deleted = 0
                    for i in range(len(self.graphTitle)):
                        updateArguments = True
                        titLen = len(self.graphTitle[i].split())                    ########################################
                        pos = self.wordPosInString(self.graphTitle[i], command[0]) - deleted         ################# ICI ################## Donne la position par caractère, pas par mot.
                        print(pos)                                                  ########################################
                        if titLen > 1 and pos != -1:
                            for n in range(len(self.graphTitle)):
                                if self.graphTitle[i] in self.graphTitle[n] and n != i:
                                    updateArguments = False
                                    break
                            if updateArguments:
                                del arguments[pos:pos+titLen]
                                deleted = titLen - 1
                                arguments.insert(pos, self.graphTitle[i])
                    print(arguments)
                    try:
                        if len(arguments)%2 != 0:
                            if self.isfloat(arguments[0]):
                                self.y.append([float(arguments[0]) for i in range(len(self.y[0]))])
                            else:
                                self.y.append(self.y[self.graphTitle.index(arguments[0])])

                            for i in range(0, len(arguments)-1, 2):
                                if self.isfloat(arguments[i+2]):
                                    self.y[-1] = [self.op[arguments[i+1]](x,float(arguments[i+2])) for x in self.y[-1]]
                                else:
                                    self.y[-1] = [self.op[arguments[i+1]](x,y) for x,y in zip(self.y[-1], self.y[self.graphTitle.index(arguments[i+2])])]
                        else:
                            print("Boom")
                            raise ValueError
                        self.graphTitle.append(" ".join(arguments))
                        i = len(self.y) - 1
                        self.addGraphBox(i)
                        self.newTabVariables()
                        self.tabWidget.addTab(self.viewWidget[i], self.graphTitle[i])
                    except ValueError:
                        Dialog(0x06)
                print(self.graphTitle)
                print(len(self.y))


    def initDigitSmooth(self):
        i = int(self.sender().objectName())
        while self.parametersLayout[i].rowCount() > self.initialRowCount:
            self.parametersLayout[i].removeRow(self.parametersLayout[i].getWidgetPosition(self.smoothingMethod[i])[0] + 1)
        try:
            self.ySmooth[i].clear()
        except AttributeError:
            self.ySmooth[i].tolist().clear()
            self.timeSmooth[i].tolist().clear()

        self.smoothingMethod[i].setEnabled(self.enableDigitSmooth[i].isChecked())

        if self.smoothingMethod[i].isEnabled():
            if self.smoothingMethod[i].currentText() == "Savitzky-Golay":
                self.initSavitzkyGolayFilter(i)
                self.updateSavitzkyGolayFilter(i)
            elif self.smoothingMethod[i].currentText() == "Interpolate":
                self.initInterpolate(i)
                self.updateInterpolateFilter(i)
            else:
                pass    ################################################################################################################
        else:
            self.Data[i].setData(self.time, self.y[i])  # Digital smoothing is disabled


    def initInterpolate(self, i):
        self.numberOfPoints[i] = QtWidgets.QSpinBox()
        self.numberOfPoints[i].setRange(0, len(self.time)*1000)
        self.numberOfPoints[i].setValue(int(len(self.time)/10))
        self.numberOfPoints[i].valueChanged.connect(lambda: self.updateInterpolateFilter(None))
        self.splineDegree[i] = QtWidgets.QSpinBox()
        self.splineDegree[i].setRange(0, 15)
        self.splineDegree[i].valueChanged.connect(lambda: self.updateInterpolateFilter(None))

        self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.smoothingMethod[i])[0] + 1, "Number of points :", self.numberOfPoints[i])
        self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.numberOfPoints[i])[0] + 1, "Spline degree :", self.splineDegree[i])

        self.numberOfPoints[i].setObjectName(str(i))
        self.splineDegree[i].setObjectName(str(i))


    def updateInterpolateFilter(self, i):
        # if i == None:
        #     i = int(self.sender().objectName())

        # self.timeSmooth[i] = np.linspace(min(self.time), max(self.time), self.numberOfPoints[i].value())
        # try:
        #     spl = make_interp_spline(np.array(self.time), np.array(self.y[i]), self.splineDegree[i].value())
        # except ValueError:
        #     spl = make_interp_spline(np.array(self.time), np.array(self.y[i]), self.splineDegree[i].value()-1)  # Some even spline degree values are illegal.
        # self.ySmooth[i] = spl(self.timeSmooth[i])

        # self.Data[i].setData(self.timeSmooth[i], self.ySmooth[i])
        if i == None:
            i = int(self.sender().objectName())

        self.timeSmooth[i] = np.linspace(min(self.time), max(self.time), self.numberOfPoints[i].value())
        self.ySmooth[i] = np.interp(self.timeSmooth[i], np.array(self.time), np.array(self.y[i]))

        self.Data[i].setData(self.timeSmooth[i], self.ySmooth[i])


    def initSavitzkyGolayFilter(self, i):
        self.filterWindowLength[i] = QtWidgets.QSpinBox()
        self.filterWindowLength[i].setRange(2, len(self.time))
        self.filterWindowLength[i].setValue(10)
        self.filterWindowLength[i].setAccelerated(True)
        self.filterWindowLength[i].setKeyboardTracking(False)
        self.filterWindowLength[i].valueChanged.connect(lambda: self.updateSavitzkyGolayFilter(None))
        self.polyorder[i] = QtWidgets.QSpinBox()
        self.polyorder[i].setRange(1, 16)
        self.polyorder[i].setValue(1)
        self.polyorder[i].setAccelerated(True)
        self.polyorder[i].setKeyboardTracking(False)
        self.polyorder[i].valueChanged.connect(lambda: self.updateSavitzkyGolayFilter(None))
        self.enableAdvancedSGF[i] = QtWidgets.QCheckBox()
        self.enableAdvancedSGF[i].setChecked(False)
        self.enableAdvancedSGF[i].stateChanged.connect(self.initAdvancedSGF)
        self.SGFdocsButton[i] = QtWidgets.QPushButton("SGF docs", self)
        self.SGFdocsButton[i].clicked.connect(lambda: htmlViewer('SGF'))
        self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.smoothingMethod[i])[0] + 1, "Filter window length :", self.filterWindowLength[i])
        self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.filterWindowLength[i])[0] + 1, "Polynomial order :", self.polyorder[i])
        self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.polyorder[i])[0] + 1, "Advanced :", self.enableAdvancedSGF[i])
        self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.enableAdvancedSGF[i])[0] + 1, "About Savitzky-Golay filter :", self.SGFdocsButton[i])
        self.initialSGFrowCount[i] = self.parametersLayout[i].rowCount()

        self.filterWindowLength[i].setObjectName(str(i) + ' wl')
        self.polyorder[i].setObjectName(str(i) + ' po')
        self.enableAdvancedSGF[i].setObjectName(str(i))


    def initAdvancedSGF(self):  ########################################################################################################
        i = int(self.sender().objectName())
        while self.parametersLayout[i].rowCount() > self.initialSGFrowCount[i]:
            self.parametersLayout[i].removeRow(self.parametersLayout[i].getWidgetPosition(self.enableAdvancedSGF[i])[0] + 1)

        if self.enableAdvancedSGF[i].isChecked():
            self.deriv[i] = QtWidgets.QSpinBox()
            self.deriv[i].setRange(0, self.polyorder[i].maximum())
            self.deriv[i].setValue(1)
            self.deriv[i].setAccelerated(True)
            self.deriv[i].setKeyboardTracking(False)
            self.deriv[i].valueChanged.connect(lambda: self.updateSavitzkyGolayFilter(None))
            self.delta[i] = QtWidgets.QDoubleSpinBox()
            self.delta[i].setDecimals(6)
            self.delta[i].setRange(0.000001, self.time[-1] - self.time[0])
            self.delta[i].setValue(1.0)
            self.delta[i].setAccelerated(True)
            self.delta[i].setKeyboardTracking(False)
            self.delta[i].valueChanged.connect(lambda: self.updateSavitzkyGolayFilter(None))
            self.mode[i] = QtWidgets.QComboBox()
            self.mode[i].addItems(['mirror', 'nearest', 'constant', 'wrap', 'interp'])
            self.mode[i].currentTextChanged.connect(lambda: self.updateSavitzkyGolayFilter(None))
            self.cval[i] = QtWidgets.QDoubleSpinBox()
            self.cval[i].setDecimals(6)
            self.cval[i].setRange(2*min(self.ySmooth[i]) - max(self.ySmooth[i]), 2*max(self.ySmooth[i]) - min(self.ySmooth[i]))
            self.cval[i].setValue(sum(self.ySmooth[i]) / len(self.ySmooth[i]))
            self.cval[i].setAccelerated(True)
            self.cval[i].setKeyboardTracking(False)
            self.cval[i].valueChanged.connect(lambda: self.updateSavitzkyGolayFilter(None))
            self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.enableAdvancedSGF[i])[0] + 1, "Derivative order :", self.deriv[i])
            self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.deriv[i])[0] + 1, "Delta value (seconds) :", self.delta[i])
            self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.delta[i])[0] + 1, "Mode to fill edges values :", self.mode[i])
            self.parametersLayout[i].insertRow(self.parametersLayout[i].getWidgetPosition(self.mode[i])[0] + 1, "Constant value :", self.cval[i])

            self.deriv[i].setObjectName(str(i) + ' drv')
            self.delta[i].setObjectName(str(i) + ' dlt')
            self.mode[i].setObjectName(str(i) + ' mde')
            self.cval[i].setObjectName(str(i) + ' cvl')
        
        self.updateSavitzkyGolayFilter(i)


    def isfloat(self, num):
        if num is None:
            return False
        try:
            float(num)
            return True
        except ValueError:
            return False


    def newTabVariables(self, numberOfNewTabs=1):
        for i in range(numberOfNewTabs):
            self.filterWindowLength.append(QtWidgets.QSpinBox())
            self.polyorder.append(QtWidgets.QSpinBox())
            self.enableAdvancedSGF.append(QtWidgets.QCheckBox())
            self.deriv.append(QtWidgets.QSpinBox())
            self.delta.append(QtWidgets.QDoubleSpinBox())
            self.mode.append(QtWidgets.QComboBox())
            self.cval.append(QtWidgets.QDoubleSpinBox())
            self.SGFdocsButton.append(QtWidgets.QPushButton())
            self.initialSGFrowCount.append(0)
            self.numberOfPoints.append(QtWidgets.QSpinBox())
            self.splineDegree.append(QtWidgets.QSpinBox())
            self.ySmooth.append([])
            self.timeSmooth.append([])


    def updateConstant(self, i):
        self.cval[i].setRange(2*min(self.ySmooth[i]) - max(self.ySmooth[i]), 2*max(self.ySmooth[i]) - min(self.ySmooth[i]))
        self.cval[i].setValue(sum(self.ySmooth[i]) / len(self.ySmooth[i]))


    def updateSavitzkyGolayFilter(self, i):
        if i == None:
            sender = self.sender().objectName().split()
            i = int(sender[0])
            senderName = sender[1]

        if self.enableAdvancedSGF[i].isChecked():
            if self.deriv[i].value() > self.polyorder[i].value():
                if senderName == 'drv':
                    self.polyorder[i].setValue(self.deriv[i].value())
                elif senderName == 'po':
                    self.deriv[i].setValue(self.polyorder[i].value())
            self.delta[i].setEnabled(self.deriv[i].value() > 0)
            self.cval[i].setEnabled(self.mode[i].currentText() == 'constant')

        if self.polyorder[i].value() >= self.filterWindowLength[i].value():
            if senderName == 'wl':
                self.polyorder[i].setValue(self.filterWindowLength[i].value() - 1)
            elif senderName == 'po':
                self.filterWindowLength[i].setValue(self.polyorder[i].value() + 1)

        if self.enableAdvancedSGF[i].isChecked():
            self.ySmooth[i] = savgol_filter(self.y[i], self.filterWindowLength[i].value(), self.polyorder[i].value(), self.deriv[i].value(), self.delta[i].value(), mode=self.mode[i].currentText(), cval=self.cval[i].value()).tolist()
            self.Data[i].setData(self.time, self.ySmooth[i])
        else:
            self.ySmooth[i] = savgol_filter(self.y[i], self.filterWindowLength[i].value(), self.polyorder[i].value(), mode='mirror').tolist()
            self.Data[i].setData(self.time, self.ySmooth[i])

        try:
            if senderName != 'cvl':
                self.updateConstant(i)
        except UnboundLocalError:
            pass


    def wordPosInString(self, word, string):
        charPos = string.find(word)
        if charPos == -1:
            return charPos
        else:
            string = string[:charPos]
            return(len(string.split()))

    def YautoRange(self):
        i = int(self.sender().objectName())
        graphRanges = self.Graph[i].getPlotItem().viewRange()
        xmin = graphRanges[0][0]
        xmax = graphRanges[0][1]
        self.Graph[i].autoRange()
        self.Graph[i].setXRange(xmin, xmax)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#


class htmlViewer(QtWebEngineWidgets.QWebEngineView):

    def __init__(self, doc, *args, **kwargs):
        super(htmlViewer, self).__init__(*args, **kwargs)

        global html
        html = self

        if doc == 'SGF':
            self.setWindowTitle("Savitzky-Golay filter documentation")
            link = "https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html"

        self.load(QtCore.QUrl(link)) #QtCore.QUrl.fromLocalFile("scipy.signal.savgol_filter — SciPy v1.10.0 Manual.html"))

        self.show()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#


class SetupWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SetupWindow, self).__init__(*args, **kwargs)

        _globals.firstExec = True
        self.selectButton = []
        self.kitsList = []
        
        self.setWindowTitle("VMCGUI - choose your kit")
        
        # self.secondKitButton = QtWidgets.QPushButton("Second Kit - NMR\nDual Pressure - Temperature")
        # self.secondKitButton.clicked.connect(self.showSecondWindow)
        for x in os.listdir(os.path.dirname(__file__) + '/Kits'):   # Generate buttons for the kits in the "/Kits" directory.
            if x.endswith(".py") and x[0] != '#':
                x = x[:-3]
                self.selectButton.append(QtWidgets.QPushButton(x))
                self.selectButton[-1].clicked.connect(lambda: self.showKit(None))
                self.selectButton[-1].setObjectName(x)
                self.kitsList.append(x)
        self.personalizButton = QtWidgets.QPushButton("Personalized Kit")
        self.loadDataButton = QtWidgets.QPushButton("Load Data")
        self.loadDataButton.clicked.connect(self.showDataPlot)
        
        self.setMinimumSize(350, 110)
        self.mainLayout = QtWidgets.QGridLayout(self)
        # self.mainLayout.addWidget(self.secondKitButton, 0, 1)
        row = 0
        column = 0
        for x in self.kitsList:
            self.mainLayout.addWidget(self.selectButton[self.kitsList.index(x)], row, column)   # Add kit buttons to the layout.
            row += column
            column = not column
        row += 1
        column = 0

        self.mainLayout.addWidget(self.personalizButton, row, column, 1, 2)
        self.mainLayout.addWidget(self.loadDataButton, row+1, column, 1, 2)
        self.setLayout(self.mainLayout)


    # def showSecondWindow(self):
    #     if self.deviceConnection():
    #         self.SecondWin = SecondKitWindow()
    #         if self.SecondWin.allowShow:
    #             self.SecondWin.showMaximized()
    #             self.close()


    def showKit(self, name):
        if name is None:
            name = self.sender().objectName()

        # module_name = name
        # module_file = 'Kits/' + name + '.py'   # os.path.dirname(os.path.realpath(__file__)) + '/Kits/' + name + '.py'
        # if spec:=importlib.util.spec_from_file_location(module_name, module_file):
        #     rebuild_module = importlib.util.module_from_spec(spec)
        #     sys.modules[module_name] = rebuild_module
        #     spec.loader.exec_module(rebuild_module)

        # kit = sys.modules[module_name]

        _globals.currentKit = importlib.import_module("Kits." + name)
        try:
            if _globals.currentKit.deviceConnection():
                self.KitWin = _globals.currentKit.KitWindow()
                if self.KitWin.allowShow:
                    self.KitWin.showMaximized()
                    if self.KitWin.closeStartWindowOnLaunch:
                        self.close()
        except AttributeError:
            Dialog(0x07)


    @classmethod
    def showDataPlot(self):
        _globals.DataWindow.append(DataPlot(_globals.dataPlotID))
        if _globals.DataWindow[-1].showData:
            _globals.dataPlotID += 1
            _globals.DataWindow[-1].show()
        else:
            _globals.DataWindow = _globals.DataWindow[:-1]


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#


class Dialog(QtWidgets.QMessageBox):

    def __init__(self, errorCode, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.errorCode = errorCode
        self.needAnswer = False
            
        if self.errorCode == 0x00:
            self.setWindowTitle("No directory selected")
            self.setText("Please, select a directory path before recording your data.")
        
        elif self.errorCode == 0x01:
            self.setWindowTitle("Cannot change directory")
            self.setText("Please, stop the record before changing directory path.")
        
        elif self.errorCode == 0x02:
            self.setWindowTitle("File already exist")
            self.setText("A file with the same name already exist. Do you want to append data to this file ?\nIf not, you should change the file name to create a new file.")
            self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.setIcon(QtWidgets.QMessageBox.Question)
            self.needAnswer = True
        
        elif self.errorCode == 0x03:
            self.setWindowTitle("A record is in progress !")
            self.setText("This will stop the record, are you sure ?")
            self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            self.setIcon(QtWidgets.QMessageBox.Question)
            self.needAnswer = True

        elif self.errorCode == 0x04:
            self.setWindowTitle("Empty command")
            self.setText("You entered an empty command. This can't be plotted.")

        elif self.errorCode == 0x05:
            self.setWindowTitle("Unopenable file")
            self.setText("This file seems to be currently empty. If this file is on recording, click on the 'Update File' button next to the 'REC' button to make it openable without stop the record.")

        elif self.errorCode == 0x06:
            self.setWindowTitle("Unrecognized command")
            self.setText("This command is not recognized. Don't forget to put space between each argument.")

        elif self.errorCode == 0x07:
            self.setWindowTitle("Unrecognized module")
            self.setText("A class or method seems to miss to the selected kit (.py file in " + os.path.dirname(os.path.realpath(__file__)) + "\\Kits\\).")

        else:
            dic = _globals.currentKit.dialogDict.get(self.errorCode)
            if dic is None:
                raise ValueError("The called dialog with errorCode " + str(hex(self.errorCode)) + " doesn't exist in the dialogDict of " + str(_globals.currentKit))
            if type(dic) != dict:
                raise ValueError("From " + str(_globals.currentKit) + ", dialogDict value with key " + str(hex(self.errorCode)) + " must be a dictionnary.")
            if any(dic.get(key) is None for key in ["Title", "Text"]):
                raise ValueError("\"Title\", \"Text\", or both key(s) are missing from the dialogDict value in " + str(_globals.currentKit) + " for the key : " + str(hex(self.errorCode)))

            self.setWindowTitle(dic.get("Title"))
            self.setText(dic.get("Text"))
            if "Icon" in dic:
                self.setIcon(dic.get("Icon"))
            if "Buttons" in dic:
                self.setStandardButtons(dic.get("Buttons"))
                self.needAnswer = True

        if not self.needAnswer:
            self.exec()
    

    def __eq__(self, arg):
        return self.exec()

    def __int__(self):
        return self.exec()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    _globals.init()
    app = QtWidgets.QApplication(sys.argv)
    setup = SetupWindow()
    setup.show()
    sys.exit(app.exec_())
