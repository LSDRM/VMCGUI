# REQUIRED
import sys
sys.path.append('..')
sys.path.append('/libsForKits')
from VMCGUI import *
from datetime import datetime

# EXTRA LIBS
from math import sin, pi


'''Blank Kit python file'''

# This file permits to write a new kit by yourself.
# Every classes, methods and variables already writen in this file are essentials to VMCGUI (except those are referred as EXTRA), if VMCGUI.py has not been modified.
# Therefore, you can add your own classes, methods and variables according to your needs.


class KitWindow(MainWindow):

    def __init__(self, *args, **kwargs):
        super(KitWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VMCGUI - Put the title of your window here")

        # REQUIRED
        self.prefix = "Here the default prefix for your files"
        self.closeStartWindowOnLaunch = True    # With this version of VMCGUI, I recommend to keep this to True, to prevent multiple windows trying to access to the the same port/communication interface.
        self.graphTitle = ["Sensor1 ", "Sensor2 "]
        self.sensorsNumber = len(self.graphTitle)   # self.sensorsNumber should correspond to the number of titles in self.graphTitle
        self.GPIOsNumber = 3
        self.samplesPerBurst = 1
        self.delayBetweenSamples = 0    # Should be 0 if samplesPerBurst = 1
        self.lineTimeOffset = 0
        self.unitMemory = [     # len(self.unitMemory) should be equal to the sensorsNumber. If you have multiple times a same sensor, you'll have multiple times the same dictionnary (see python dict).
            {                   # For example here, the first sensor may be a pressure sensor, and the second one a temperature sensor.
                "Bar" : 1,
                "Pa" : 100000,
                "PSI" : 14.50377
            },
            {
                "Kelvin" : 0,
                "Celsius" : -273.15
            }
        ]
        
        self.initCentralFrame()     # Call the initCentralFrame() method from the MainWindow class in VMCGUI.py will automatically generate the layout according to the number of sensors and GPIOs.
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.sampleTime.value() * self.sampleUnitMultiplier)
        self.timer.timeout.connect(self.update_plot_data)   # Call udate_plot_data() method from VMCGUI.py each times the interval time is reached.
        self.timer.start()


    def checkGPIOstate(self, i):    # If you don't have any GPIO in your system, and set self.GPIOsNumber to 0, you can safely remove this method.
        state = GPIO[i].isActive()  # HERE, you must replace GPIO[i].isActive() with the instruction you'll use to check if the GPIO with identifier 'i' is active. "state" takes a bool value.
        self.setGPIOicon(i, state)
        return state


    def get_measures(self, N):
        sampleTime = datetime.timestamp(datetime.now()) + self.lineTimeOffset

        # Place here the block of code to retrieve your measurements from your system.
        # If your system works in a 1-by-1 sample mode, you must ask for a sample of measure for each of your sensors, and store them.
        # If your system works in an N-by-N samples mode, you must ask for N samples of measure for each of your sensors, and store them.

        for n in range(N):                  # This block works for both 1-by-1 and N-by-N modes.
            self.time.append(sampleTime)
            sampleTime += self.delayBetweenSamples

            for ID in range(self.sensorsNumber):

                # Place here the block of code to process your stored measures.
                # Those stored measures will need to get append to the self.y[ID] list under the corrected unit.
                # In most of cases, you'll need to convert the binary value of each measure to a float value or other.
                # Here is a little example below with the get_pres and get_temp methods.

                if ID == 0:
                    self.get_pres(ID)
                elif ID == 1:
                    self.get_temp(ID)


    # EXTRA
    def get_pres(self, ID):
        pres = sin(self.time[-1]/4 + ID*pi)/4 + 1
        self.y[ID].append(self.unitMemory[ID].get(self.Unit[ID].currentText()) * pres)    # NOTE the '*' here to multiply the value by the unit. (Conversion of pressure is usually made by multiplication)
        self.Graph[ID].setTitle(self.graphTitle[ID] + str("%.3f" % round(self.y[ID][-1], 3)) + " " + self.Unit[ID].currentText(), color='w')    # To actualize the graph title with the last value plotted.
    
    
    # EXTRA
    def get_temp(self, ID):
        temp = randint(0, 100)/100 + 298.15
        self.y[ID].append(temp + self.unitMemory[ID].get(self.Unit[ID].currentText()))    # NOTE the '+' here to add the value to the unit. (Conversion of temperature is usually made by addition).
        self.Graph[ID].setTitle(self.graphTitle[ID] + str("%.3f" % round(self.y[ID][-1], 3)) + " " + self.Unit[ID].currentText(), color='w')    # To actualize the graph title with the last value plotted.


    def manualSetGPIO(self, i):     # If you don't have any GPIO in your system, and set self.GPIOsNumber to 0, you can safely remove this method.
        if i is None:
            i = int(self.sender().objectName())

        self.applyGPIO(i)
        # Here, you may set the state of GPIO with identifier 'i' to the value of "self.outputManualSetButton[i].isChecked()" which is boolean.
        self.checkGPIOstate(i)


    def autoSetGPIO(self, i, value="INVERT"):   # If you don't have any GPIO in your system, and set self.GPIOsNumber to 0, you can safely remove this method.
        if i is None:
            i = int(self.sender().objectName())

        # Here, you'll need to make the instruction to set the GPIO with identifier 'i' to the given 'value' (if value is not "INVERT", it is boolean). If 'value' is "INVERT", the GPIO state need to be inverted.
        self.checkGPIOstate(i)


    def writeMeasurements(self, pos):       # Write a line of measurements in the opened file
        self.file.write(str(self.time[pos]) + "\t\t" + str(self.y[0][pos] / self.unitMemory[0].get(self.Unit[0].currentText())) + "\t\t" + str(self.y[1][pos] - self.unitMemory[1].get(self.Unit[1].currentText())) + "\n")
        # The line above is used when recording measurements, it writes the measure of each sensor in the selected file, with the default unit value (default unit is the first one in each self.unitMemory[i] dictionnary).



def deviceConnection():         # This method serve to check if the whole system is properly connected to the computer.
    if system.isConnected():    # HERE, you should replace system.isConnected() by your method checking if the system is properly connected.
        return True
    else:
        Dialog(0x04)
        return False