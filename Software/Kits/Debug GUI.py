import sys
sys.path.append('..')
from NMRInstrument import *

'''To debug GUI without kit'''

# This window do not need any kit connected to the computer to be launched.
# It is useful when programming the GUI and personalizing it.


class KitWindow(MainWindow):

    def __init__(self, *args, **kwargs):
        super(KitWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("NMRinstrument - Debug window")

        self.prefix = "Debug"
        self.closeStartWindowOnLaunch = False
        self.graphTitle = ["Pressure0 ", "Pressure1 ", "Temperature ", "Random ", "Rand"]
        self.sensorsNumber = 5
        self.GPIOsNumber = 3
        self.simulateGPIO = [False for i in range(self.GPIOsNumber)]

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
            },
            {
                "Random" : 0
            },
            {
                "Rand" : 0
            }
        ]
        
        self.initCentralFrame()
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.sampleTime.value() * self.sampleUnitMultiplier)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def checkGPIOstate(self, i):
        if self.simulateGPIO[i]:
            self.GPIOview.setTabIcon(i, QtGui.QIcon(":/GPIOactive.png"))
            return True
        else:
            self.GPIOview.setTabIcon(i, QtGui.QIcon(":/GPIOinactive.png"))
            return False


    def get_measure(self, ID):
        if ID == 0 or ID == 1:
            self.get_pres(ID)
        elif ID == 2:
            self.get_temp()
        else:
            self.y[ID].append(randint(0, 100))


    def get_pres(self, ABP):
        self.y[ABP].append(self.unitMemory[ABP].get(self.Unit[ABP].currentText()) * randint(1, 2))
        self.Graph[ABP].setTitle(self.graphTitle[ABP] + str("%.3f" % round(self.y[ABP][-1], 3)) + " " + self.Unit[ABP].currentText(), color='w')
    
    
    def get_temp(self):
        self.temp = randint(0, 100)
        self.y[2].append(self.temp + self.unitMemory[2].get(self.Unit[2].currentText()))
        self.Graph[2].setTitle(self.graphTitle[2] + str("%.3f" % round(self.y[2][-1], 3)) + " " + self.Unit[2].currentText(), color='w')


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