# REQUIRED
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/libsForKits')
from VMCGUI import *
from datetime import datetime

# EXTRA LIBS
import ftd2xx as ftd
import ADS122U04 as ads
from thermocouples_reference import thermocouples


'''Personalized board with 2 pressure sensors, and 1 thermocouple connection'''

# This board is connected to the computer through a USB to UART RS485 module,
# which allow long distance communication between the board and the computer.
# The USB to UART RS485 module is based on an FT231XS chip : https://ftdichip.com/products/ft231xs/
# The data acquisition board is based on an ADS122U04 chip handling 3 GPIOs, which is an UART ADC : https://www.ti.com/lit/ds/symlink/ads122u04.pdf


class KitWindow(MainWindow):

    def __init__(self, *args, **kwargs):
        super(KitWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VMCGUI - DualPressure / Thermocouple")

        # REQUIRED
        self.prefix = "Kit2"
        self.closeStartWindowOnLaunch = True
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
        
        # EXTRAS
        global deviceMem
        self.resetTemp = False
        self.regValues = {      # Register values of the ADS122U04 (ADC UART)
            0: 0xD0,
            1: 0xD2,
            2: 0x00,
            3: 0x01,
            4: 0x70
        }

        try:
            self.adsDevice = ads.Device()                   # Create and initialize ADS device (UART ADC) through the FTDI chip (USB to UART bridge)
        except ftd.ftd2xx.DeviceError:
            self.adsDevice = deviceMem
        else:
            deviceMem = self.adsDevice

        if not self.adsDevice.setReg(self.regValues):   # Write the registers configuration in the ADS device for this kit
            if self.lineCommunicationFault():
                self.allowShow = False
                return
        
        self.initCentralFrame()     # Initializing central frame, which contains all graphs and GPIOs window.

        self.thermocoupleType = QtWidgets.QComboBox()                                                       # This block add some parameter widgets useful for data calculations or plotting.
        self.thermocoupleType.addItems(['T', 'K', 'J', 'N', 'E', 'M', 'S', 'B', 'R', 'C', 'G', 'D', 'P'])
        self.resetTempButton = QtWidgets.QPushButton()
        self.resetTempButton.setText("Set temp to 0")
        self.resetTempButton.setEnabled(False)
        self.resetTempButton.clicked.connect(lambda: setattr(self, 'resetTemp', True))
        self.ParametersLayout[2].addRow("Thermocouple type :" ,self.thermocoupleType)
        self.ParametersLayout[2].addRow("Reset temperature :", self.resetTempButton)
        self.rowCount[2] = self.ParametersLayout[2].rowCount()                          # Do not forget this command, to update the rowCount of the modified ParametersLayout if you modified one.
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.sampleTime.value() * self.sampleUnitMultiplier)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def checkGPIOstate(self, i):
        state = self.adsDevice.liveRegMemory[4] & (1 << i)
        self.setGPIOicon(i, state)
        return state


    def get_measure(self, ID):
        if ID == 0 or ID == 1:
            self.get_pres(ID)
        elif ID == 2:
            self.get_temp(ID)


    def get_pres(self, ABP):        # Each run of this function take 22 bytes on the line (14 write and 8 read)
        reference = self.adsDevice.supplyREF()
        if not reference:      # To prevent ZeroDivisionError, means read operation failed.
            self.lineFaultCounter += 1
            if self.lineFaultCounter == 5:
                self.timer.stop()
                self.allowShow = not self.lineCommunicationFault()
                if self.allowShow:
                    self.lineFaultCounter = 0
                    self.timer.start()
            return
        self.lineFaultCounter = 0
        self.adsDevice.selectAnalog(8 + ABP)
        voltage = self.adsDevice.binToVolt(self.adsDevice.command(ads.START_RESTART), reference)
        self.y[ABP].append(self.unitMemory[ABP].get(self.Unit[ABP].currentText()) * (voltage - reference * 0.1) * 10 / (reference * 0.8))
        self.Graph[ABP].setTitle(self.graphTitle[ABP] + str("%.3f" % round(self.y[ABP][-1], 3)) + " " + self.Unit[ABP].currentText(), color='w')
    
    
    def get_temp(self, ID):     # 58 bytes (45 sended, 13 received)
        reg = {
            0: 0x6A,
            1: 0xD0
        }
        self.adsDevice.setReg(reg, reset=False)     # 12 bytes on line (10 sended, 2 received)
        binVal = self.adsDevice.command(ads.START_RESTART)  # 5 bytes on line (2 sended, 3 received)
        total_mV = self.adsDevice.binToVolt(binVal, ads.ADSinternalREF * 1000) / (pow(2, (reg.get(0) & 0x0E) >> 1))
        coldJunctionTemp = self.adsDevice.getTemp(reg.get(1)) - 1       # We substract 1, because there is approximatively 1 Kelvin difference between the real cold junction, and the ADS122U04 integrated temperature sensor measurement.     11 bytes (8 sended, 3 received)

        # print(str(hex(binVal)) + '\t' + str(total_mV) + '\t' + str(coldJunctionTemp))

        try:
            temp = thermocouples[self.thermocoupleType.currentText()].inverse_KmV(total_mV, Tref=coldJunctionTemp)
            self.resetTempButton.setEnabled(False)
        except (ValueError, RuntimeError):  # To prevent data out of range of the thermocouple table. This occur when thermocouple is disconnected, or when selected thermocouple is not the installed one.
            self.resetTempButton.setEnabled(True)
            if self.y[ID] and not self.resetTemp:      # If self.y[ID] is not empty and no resetTemp has been called.
                temp = self.y[ID][-1]
            else:               # Else, self.y[ID] is empty or resetTemp has been called.
                temp = 0
                self.resetTemp = False

        self.adsDevice.setReg(self.regValues, list(reg.keys()), False)      # Set back regValues that were modified.    30 bytes (25 sended, 5 received)

        self.y[ID].append(temp + self.unitMemory[ID].get(self.Unit[ID].currentText()))
        self.Graph[ID].setTitle(self.graphTitle[ID] + str("%.3f" % round(self.y[ID][-1], 3)) + " " + self.Unit[ID].currentText(), color='w')


    def lineCommunicationFault(self):
        while not self.adsDevice.setReg(self.regValues):
            aswr = int(Dialog(0x09))
            if aswr == QtWidgets.QMessageBox.Retry:
                self.adsDevice.d.resetDevice()
            elif aswr == QtWidgets.QMessageBox.Cancel:
                self.showSetupWindow()
                return True
        return False


    def manualSetGPIO(self, i):
        if i is None:
            i = int(self.sender().objectName())

        self.applyGPIO(i)
        self.adsDevice.setGPIO(i, self.outputManualSetButton[i].isChecked())
        self.checkGPIOstate(i)


    def autoSetGPIO(self, i, value="INVERT"):
        if i is None:
            i = int(self.sender().objectName())

        self.adsDevice.setGPIO(i, value)
        self.checkGPIOstate(i)


    def writeMeasurements(self, pos):       # Write measurements in the opened file
        self.file.write(str(self.time[pos]) + "\t\t" + str(self.y[0][pos] / self.unitMemory[0].get(self.Unit[0].currentText())) + "\t\t" + str(self.y[1][pos] / self.unitMemory[1].get(self.Unit[1].currentText())) + "\t\t" + str(self.y[2][pos] - self.unitMemory[2].get(self.Unit[2].currentText())) + "\n")


def deviceConnection():     # Check if the USB to UART module is connected to the computer.
    if ftd.listDevices():
        return True
    else:
        Dialog(0x08)
        return False

dialogDict = {
    0x08: {
        "Title": "No FTDI device found",
        "Text": "No FTDI device detected. Please, connect your device before selecting a kit.",
    },
    0x09: {
        "Title": "Unable to communicate with the kit board",
        "Text": "The ADC registers can't be set or too many timeout occurs.\nPlease, make sure the instrumentation board is powered and connected to the USB-UART module.",
        "Buttons": QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel,
        "Icon": QtWidgets.QMessageBox.Warning
    }
}