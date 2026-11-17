# REQUIRED
import sys
sys.path.append('..')
sys.path.append('/libsForKits')
from VMCGUI import *
from datetime import datetime

# EXTRA LIBS
from math import sin, pi
from random import randint


"""
Debug GUI Window
=================

A VMCGUI kit for debugging and testing the GUI without requiring
actual hardware connection.

This kit generates simulated sensor data and provides a complete
GUI interface for testing all VMCGUI features including:
- Multiple sensor visualization
- GPIO control simulation
- Data recording
- Unit conversion

Perfect for development, testing, and GUI customization.
"""

# This window doesn't need any kit connected to the computer to be launched.
# It is useful when programming the GUI and personalizing it.


class KitWindow(MainWindow):
    """
    Debug GUI Window Class
    
    Main window class for the debug kit, extending VMCGUI's MainWindow
    to provide simulated sensor data and GPIO control.
    
    Attributes:
        prefix (str): Default prefix for saved files
        closeStartWindowOnLaunch (bool): Keep start window open for debugging
        graphTitle (list): Titles for simulated sensors
        sensorsNumber (int): Number of simulated sensors (3)
        GPIOsNumber (int): Number of simulated GPIO pins (3)
        simulateGPIO (list): Simulated GPIO states
        unitMemory (list): Unit conversion dictionaries for pressure/temperature
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the debug window.
        
        Sets up simulated sensors, GPIO states, and starts the data
        generation timer.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
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
        """
        Check the state of a simulated GPIO pin.
        
        Returns the current simulated state of a GPIO pin and updates
        the corresponding UI icon.
        
        Args:
            i (int): GPIO identifier/pin number
            
        Returns:
            bool: Current simulated state of the GPIO pin
        """
        state = self.simulateGPIO[i]
        self.setGPIOicon(i, state)
        return state


    def get_measures(self, N):
        """
        Generate simulated measurements for all sensors.
        
        Creates N samples of simulated data for pressure and temperature
        sensors using mathematical functions and random values.
        
        Args:
            N (int): Number of samples to generate
        """
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
        """
        Generate simulated pressure measurement.
        
        Creates simulated pressure data using a sine wave function
        for realistic-looking test data.
        
        Args:
            ABP (int): Sensor identifier (0 or 1 for pressure sensors)
            
        Note:
            Generates pressure values that oscillate between 0.75 and 1.25
            in the selected unit, then updates the graph title.
        """
        pres = sin(self.time[-1]/4 + ABP*pi)/4 + 1
        self.y[ABP].append(self.unitMemory[ABP].get(self.Unit[ABP].currentText()) * pres)
        self.Graph[ABP].setTitle(self.graphTitle[ABP] + str("%.3f" % round(self.y[ABP][-1], 3)) + " " + self.Unit[ABP].currentText(), color='w')
    
    
    def get_temp(self, ID):
        """
        Generate simulated temperature measurement.
        
        Creates simulated temperature data using random values around
        room temperature (25°C / 298.15K).
        
        Args:
            ID (int): Sensor identifier (2 for temperature sensor)
            
        Note:
            Generates temperature values between 298.15K and 299.15K
            (25°C to 26°C) with unit conversion, then updates the graph title.
        """
        temp = randint(0, 100)/100 + 298.15
        self.y[ID].append(temp + self.unitMemory[ID].get(self.Unit[ID].currentText()))
        self.Graph[ID].setTitle(self.graphTitle[ID] + str("%.3f" % round(self.y[ID][-1], 3)) + " " + self.Unit[ID].currentText(), color='w')


    def manualSetGPIO(self, i):
        """
        Manually set the state of a simulated GPIO pin.
        
        Updates the simulated GPIO state based on the corresponding
        UI button state.
        
        Args:
            i (int): GPIO identifier/pin number
        """
        if i is None:
            i = int(self.sender().objectName())

        self.applyGPIO(i)
        self.simulateGPIO[i] = self.outputManualSetButton[i].isChecked()
        self.checkGPIOstate(i)


    def autoSetGPIO(self, i, value="INVERT"):
        """
        Automatically set the state of a simulated GPIO pin.
        
        Provides programmatic control of simulated GPIO pins with
        support for toggling (INVERT) or setting to specific states.
        
        Args:
            i (int): GPIO identifier/pin number
            value (str/bool): Desired state. "INVERT" to toggle, bool for specific state
        """
        if i is None:
            i = int(self.sender().objectName())

        if value == "INVERT":
            self.simulateGPIO[i] = not self.simulateGPIO[i]
        else:
            self.simulateGPIO[i] = value

        self.checkGPIOstate(i)


    def writeMeasurements(self, pos):
        """
        Write simulated measurements to the opened file.
        
        Writes a line of simulated measurements from all sensors to the
        currently opened data file with their default unit values.
        
        Args:
            pos (int): Position/index of the measurement to write
        """
        self.file.write(str(self.time[pos]) + "\t\t" + str(self.y[0][pos] / self.unitMemory[0].get(self.Unit[0].currentText())) + "\t\t" + str(self.y[1][pos] / self.unitMemory[1].get(self.Unit[1].currentText())) + "\t\t" + str(self.y[2][pos] - self.unitMemory[2].get(self.Unit[2].currentText())) + "\n")



def deviceConnection():
    """
    Check if the debug system is "connected".
    
    For the debug kit, this always returns True since no actual
    hardware connection is required.
    
    Returns:
        bool: Always True for the debug kit
    """
    return True