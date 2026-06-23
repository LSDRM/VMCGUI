# REQUIRED
import sys
sys.path.append('..')
sys.path.append('/libsForKits')
from VMCGUI import *
from datetime import datetime

# EXTRA LIBS
from pyfirmata2 import *


"""
Arduino Multi-Channel Oscilloscope
===================================

A VMCGUI kit for using an Arduino as a multi-channel oscilloscope.

This kit allows visualization of analog signals from up to 4 Arduino
analog inputs (A0-A3) with additional digital GPIO control.

Features:
    - 4 analog input channels
    - 12 digital GPIO pins
    - Real-time data visualization
    - Data recording capabilities
    - Unit conversion support
"""

# INIT FIRMATA
port = ArduinoNano.AUTODETECT
board = ArduinoNano(port)
it = util.Iterator(board)
it.start()
board.analog[0].mode = INPUT
board.analog[1].mode = INPUT
board.analog[2].mode = INPUT
board.analog[3].mode = INPUT
arduino_REF = 5

class KitWindow(MainWindow):
    """
    Arduino Multi-Channel Oscilloscope Window
    
    Main window class for the Arduino oscilloscope kit, extending the
    VMCGUI MainWindow class to provide Arduino-specific functionality.
    
    Attributes:
        prefix (str): Default prefix for saved files
        graphTitle (list): Titles for each analog input channel
        sensorsNumber (int): Number of analog sensors (4 for A0-A3)
        GPIOsNumber (int): Number of digital GPIO pins (12)
        unitMemory (list): Unit conversion dictionaries for voltage/current
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the Arduino oscilloscope window.
        
        Sets up the window title, sensor configuration, GPIO settings,
        and starts the data acquisition timer.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        super(KitWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VMCGUI - Arduino multi-channel oscilloscope")

        # REQUIRED
        self.prefix = "Arduino-MultiChan-Oscillo"
        self.closeStartWindowOnLaunch = True    # With this version of VMCGUI, I recommend to keep this to True, to prevent multiple windows trying to access to the the same port/communication interface.
        self.graphTitle = ["A0 ", "A1 ", "A2 ", "A3 "]
        self.sensorsNumber = len(self.graphTitle)   # self.sensorsNumber should correspond to the number of titles in self.graphTitle
        self.GPIOsNumber = 12
        self.samplesPerBurst = 1
        self.delayBetweenSamples = 0    # Should be 0 if samplesPerBurst = 1
        self.lineTimeOffset = 0
        self.unitMemory = [     # len(self.unitMemory) should be equal to the sensorsNumber. If you have multiple times a same sensor, you'll have multiple times the same dictionnary (see python dict).
            {                   # For example here, the first sensor may be a pressure sensor, and the second one a temperature sensor.
                "Voltage" : 0,
                "Current" : 0
            },
            {
                "Voltage" : 0,
                "Current" : 0
            },
            {
                "Voltage" : 0,
                "Current" : 0
            },
            {
                "Voltage" : 0,
                "Current" : 0
            }
        ]
        
        self.initCentralFrame()     # Call the initCentralFrame() method from the MainWindow class in VMCGUI.py will automatically generate the layout according to the number of sensors and GPIOs.
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.sampleTime.value() * self.sampleUnitMultiplier)
        self.timer.timeout.connect(self.update_plot_data)   # Call udate_plot_data() method from VMCGUI.py each times the interval time is reached.
        self.timer.start()


    def checkGPIOstate(self, i):
        """
        Check the state of an Arduino digital GPIO pin.
        
        Reads the current state of a digital GPIO pin from the Arduino
        board and updates the corresponding UI icon.
        
        Args:
            i (int): GPIO identifier/pin number
            
        Returns:
            bool: True if GPIO is HIGH, False if LOW
        """
        state = board.digital[i].read()  # HERE, you must replace GPIO[i].isActive() with the instruction you'll use to check if the GPIO with identifier 'i' is active. "state" takes a bool value.
        self.setGPIOicon(i, state)
        return state


    def get_measures(self, N):
        """
        Retrieve measurements from Arduino analog inputs.
        
        Reads analog values from all configured Arduino analog inputs
        (A0-A3) and stores them for visualization.
        
        Args:
            N (int): Number of samples to acquire
            
        Note:
            Analog values are scaled by the Arduino reference voltage (5V).
        """
        sampleTime = datetime.timestamp(datetime.now()) + self.lineTimeOffset

        # Place here the block of code to retrieve your measurements from your system.
        # If your system works in a 1-by-1 sample mode, you must ask for a sample of measure for each of your sensors, and store them.
        # If your system works in an N-by-N samples mode, you must ask for N samples of measure for each of your sensors, and store them.

        for n in range(N):                  # This block works for both 1-by-1 and N-by-N modes.
            self.time.append(sampleTime)
            sampleTime += self.delayBetweenSamples

            for ID in range(self.sensorsNumber):
                self.y[ID].append(board.analog[ID].value * arduino_REF)


    # EXTRA
    def manualSetGPIO(self, i):
        """
        Manually set the state of an Arduino digital GPIO pin.
        
        Sets the state of a digital GPIO pin based on the corresponding
        UI button state. Note that Arduino digital pins start from pin 2.
        
        Args:
            i (int): GPIO identifier (0-based index, maps to Arduino pin i+2)
            
        Note:
            The actual Arduino pin number is i+2 to account for the
            offset between the UI index and physical pin numbering.
        """
        if i is None:
            i = int(self.sender().objectName())

        self.applyGPIO(i)
        board.digital[i+2].write(self.outputManualSetButton[i].isChecked()) # Here, you may set the state of GPIO with identifier 'i' to the value of "self.outputManualSetButton[i].isChecked()" which is boolean.
        self.checkGPIOstate(i)


    def autoSetGPIO(self, i, value="INVERT"):
        """
        Automatically set the state of an Arduino digital GPIO pin.
        
        Provides programmatic control of GPIO pins with support for
        toggling (INVERT) or setting to specific states.
        
        Args:
            i (int): GPIO identifier (0-based index, maps to Arduino pin i+2)
            value (str/bool): Desired state. "INVERT" to toggle, bool for specific state
            
        Note:
            The actual Arduino pin number is i+2 to account for the
            offset between the UI index and physical pin numbering.
        """
        if i is None:
            i = int(self.sender().objectName())

        if value == "INVERT":    # Here, you'll need to make the instruction to set the GPIO with identifier 'i' to the given 'value' (if value is not "INVERT", it is boolean). If 'value' is "INVERT", the GPIO state need to be inverted.
            val = not board.digital[i+2].read()
        else:
            val = value

        board.digital[i+2].write(val)
        self.checkGPIOstate(i)


    def writeMeasurements(self, pos):
        """
        Write Arduino measurements to the opened file.
        
        Writes a line of measurements from all analog inputs to the
        currently opened data file. Measurements are written with their
        default unit values (first unit in each unitMemory dictionary).
        
        Args:
            pos (int): Position/index of the measurement to write
        """
        string = str(self.time[pos])
        for i in range(self.sensorsNumber):
            string = string + "\t\t" + str(self.y[i][pos] / self.unitMemory[i].get(self.Unit[i].currentText()))

        self.file.write(string + "\n")
        # The line above is used when recording measurements, it writes the measure of each sensor in the selected file, with the default unit value (default unit is the first one in each self.unitMemory[i] dictionnary).



def deviceConnection():
    """
    Check if the Arduino board is properly connected.
    
    Verifies that the Arduino board is connected and Firmata protocol
    is working correctly.
    
    Returns:
        bool: True if Arduino is connected and Firmata is working, False otherwise
        
    Note:
        Uses board.get_firmata_version() to check Firmata communication.
        If connection fails, displays a dialog (0x04) to inform the user.
    """
    if board.get_firmata_version():    # HERE, you should replace system.isConnected() by your method checking if the system is properly connected.
        return True
    else:
        Dialog(0x04)
        return False