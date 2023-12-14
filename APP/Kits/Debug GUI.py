# REQUIRED
import sys
sys.path.append('..')
sys.path.append('/libsForKits')
from VMCGUI import *
from datetime import datetime

# EXTRA LIBS
from math import sin, pi
from random import randint


'''To debug GUI without kit'''

# This window doesn't need any kit connected to the computer to be launched.
# It is useful when programming the GUI and personalizing it.


class KitWindow(MainWindow):

    def __init__(self, *args, **kwargs):
        super(KitWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VMCGUI - Debug window")

        # REQUIRED
        self.prefix = "Debug"
        self.closeStartWindowOnLaunch = False
        self.graphTitle = ["Pressure0 ", "Pressure1 ", "Temperature "]
        self.sensorsNumber = len(self.graphTitle)
        self.GPIOsNumber = 3
        self.samplesPerBurst = 1
        self.delayBetweenSamples = 0    # Should be 0 if samplesPerBurst = 1
        self.lineTimeOffset = 0
        self.unitMemory = [
            {
                "Bar" : 1,
                "Pa" : 100000,
                "PSI" : 14.50377
            },
            {
                "Bar" : 1,
                "Pa" : 100000,
                "PSI" : 14.50377
            },
            {
                "Kelvin" : 0,
                "Celsius" : -273.15
            }
        ]

        # EXTRA
        self.simulateGPIO = [False for i in range(self.GPIOsNumber)]
        
        self.initCentralFrame()
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.sampleTime.value() * self.sampleUnitMultiplier)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def checkGPIOstate(self, i):
        state = self.simulateGPIO[i]
        self.setGPIOicon(i, state)
        return state


    def get_measures(self, N):
        sampleTime = datetime.timestamp(datetime.now()) + self.lineTimeOffset
        for n in range(N):
            self.time.append(sampleTime)
            sampleTime += self.delayBetweenSamples

            for ID in range(self.sensorsNumber):
                if ID == 0 or ID == 1:
                    self.get_pres(ID)
                elif ID == 2:
                    self.get_temp(ID)
                else:
                    self.y[ID].append(randint(0, 100))


    def get_pres(self, ABP):
        pres = sin(self.time[-1]/4 + ABP*pi)/4 + 1
        self.y[ABP].append(self.unitMemory[ABP].get(self.Unit[ABP].currentText()) * pres)
        self.Graph[ABP].setTitle(self.graphTitle[ABP] + str("%.3f" % round(self.y[ABP][-1], 3)) + " " + self.Unit[ABP].currentText(), color='w')
    
    
    def get_temp(self, ID):
        temp = randint(0, 100)/100 + 298.15
        self.y[ID].append(temp + self.unitMemory[ID].get(self.Unit[ID].currentText()))
        self.Graph[ID].setTitle(self.graphTitle[ID] + str("%.3f" % round(self.y[ID][-1], 3)) + " " + self.Unit[ID].currentText(), color='w')


    def manualSetGPIO(self, i):
        if i is None:
            i = int(self.sender().objectName())

        self.applyGPIO(i)
        self.simulateGPIO[i] = self.outputManualSetButton[i].isChecked()
        self.checkGPIOstate(i)


    def autoSetGPIO(self, i, value="INVERT"):
        if i is None:
            i = int(self.sender().objectName())

        if value == "INVERT":
            self.simulateGPIO[i] = not self.simulateGPIO[i]
        else:
            self.simulateGPIO[i] = value

        self.checkGPIOstate(i)


    def writeMeasurements(self, pos):       # Write measurements in the opened file
        self.file.write(str(self.time[pos]) + "\t\t" + str(self.y[0][pos] / self.unitMemory[0].get(self.Unit[0].currentText())) + "\t\t" + str(self.y[1][pos] / self.unitMemory[1].get(self.Unit[1].currentText())) + "\t\t" + str(self.y[2][pos] - self.unitMemory[2].get(self.Unit[2].currentText())) + "\n")



def deviceConnection():
    return True