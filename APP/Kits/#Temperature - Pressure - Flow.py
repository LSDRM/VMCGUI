import sys
sys.path.append('..')
from VMCS import *

'''Personalized board with 1 CTN (temperature), 1 pressure sensor, and 1 flow sensor.'''


class FirstKitWindow(MainWindow):

    def __init__(self, *args, **kwargs):
        super(FirstKitWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("VMCS - First Kit")
        global deviceMem

        self.prefix = "Kit1"
        self.graphTitle = ["Temperature ", "Pressure ", "Flow "]
        self.sensorsNumber = 3

        self.unitMemory = [
            {
                "Kelvin" : 0,
                "Celsius" : -273.15
            },
            {
                "Bar" : 1,
                "Pa" : 100000,
                "PSI" : 14.50377
            },
            {
                "pF" : 1,
                "uF" : 0.001
            }
        ]
        
        self.regValues = {      # Register values of the ADS122U04 (ADC UART)
            0: 0xD0,
            1: 0xD2,
            2: 0x00,
            3: 0x01,
            4: 0x70
        }

        self.R0 = 10000
        self.Beta = 3901.55
        self.Rambiant = 10000
        self.Tambiant = 298.15

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
        
        self.initCentralFrame()
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.sampleTime.value() * self.sampleUnitMultiplier)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def get_measure(self, ID):
        if ID == 0:
            self.get_temp()
        elif ID == 1:
            self.get_pres()
        elif ID == 2:
            self.get_flow()
    
    
    def get_temp(self):
        self.AIn_1 = randint(0, 100)
        try:
            self.tempResistor = self.R0/(10 / (self.AIn_1 / 1000) - 1)
            self.tempNotFinal = (1/((math.log(self.tempResistor/self.Rambiant)/self.Beta) + (1/self.Tambiant))) - 273.15
            self.temp = self.tempNotFinal - ((3.21*math.pow(10, -9)*math.pow(self.tempNotFinal, 4)) - (1.16*math.pow(10, -6)*math.pow(self.tempNotFinal, 3)) + (4.67*math.pow(10, -4)*math.pow(self.tempNotFinal, 2)) - (0.0214*self.tempNotFinal) + 0.261)
            self.y[0].append(self.temp + self.unitMemory[0].get(self.Unit[0].currentText()))
            self.Graph[0].setTitle(self.graphTitle[0] + str("%.3f" % round(self.y[0][-1], 3)) + " " + self.Unit[0].currentText(), color='w')
        except ZeroDivisionError:
            pass
    
    
    def get_pres(self):
        self.presPa = ((randint(0, 100) / 5000) - 0.1) * (1000000 / 0.8)
        self.y[1].append(self.presPa * self.unitMemory[1].get(self.Unit[1].currentText()))
        self.Graph[1].setTitle(self.graphTitle[1] + str("%.3f" % round(self.y[1][-1], 3)) + " " + self.Unit[1].currentText(), color='w')
    
    
    def get_flow(self):
        self.flow = randint(0, 100)
        self.y[2].append(self.flow * self.unitMemory[2].get(self.Unit[2].currentText()))
        self.Graph[2].setTitle(self.graphTitle[2] + str("%.3f" % round(self.y[2][-1], 3)) + " " + self.Unit[2].currentText(), color='w')


    def writeMeasurements(self, pos):       # Write measurements in the opened file
        self.file.write(str(self.time[pos]) + "\t\t" + str(self.y[0][pos] / self.unitMemory[0].get(self.Unit[0].currentText())) + "\t\t" + str(self.y[1][pos] / self.unitMemory[1].get(self.Unit[1].currentText())) + "\t\t" + str(self.y[2][pos] - self.unitMemory[2].get(self.Unit[2].currentText())) + "\n")


def deviceConnection():
    devList = ftd.listDevices()
    if not devList:
        Dialog(0x04)
        return False
    else:
        return True