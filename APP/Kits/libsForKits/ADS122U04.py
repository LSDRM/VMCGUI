import ftd2xx as ftd
import time


syncWord = 0x55
RESET = 0x06
POWERDOWN = 0x02
START_RESTART = 0x08
RDATA = 0x10

RREG = {       #Adress to read register value
    0: 0x20,
    1: 0x22,
    2: 0x24,
    3: 0x26,
    4: 0x28
}
WREG = {       #Adress to write register value
    0: 0x40,
    1: 0x42,
    2: 0x44,
    3: 0x46,
    4: 0x48
}

ADSinternalREF = 2.048
tempResolution = 0.03125    # Celsius per bit with a 14-bits resolution.
GPIOs = [0,1,2]

AIn = {    ### See ADS122U04 datasheet, p.41 ###
    0: 0x0F,    #AIn0 - AIn1
    1: 0x1F,    #AIn0 - AIn2
    2: 0x2F,    #AIn0 - AIn3
    3: 0x3F,    #AIn1 - AIn0
    4: 0x4F,    #AIn1 - AIn2
    5: 0x5F,    #AIn1 - AIn3
    6: 0x6F,    #AIn2 - AIn3
    7: 0x7F,    #AIn3 - AIn2
    8: 0x8F,    #AIn0 - GND
    9: 0x9F,    #AIn1 - GND
    10: 0xAF,   #AIn2 - GND
    11: 0xBF,   #AIn3 - GND
    12: 0xCF,   #(REFp - REFn) / 4
    13: 0xDF,   #(AVDD - AVSS) / 4
    14: 0xEF,   #AINp and AINn to AnalogSupply / 2   (zero, to measure offset)
    15: 0xFF,   #RESERVED   (unused)
}


__all__ = ['Device']
class Device:

    def __init__(self, ID=0, baud=9600, frame=ftd.defines.BITS_8, stop=ftd.defines.STOP_BITS_1, parity=ftd.defines.PARITY_NONE, rTimeout=200, wTimeout=200):
        self.d = ftd.open(ID)
        self.d.setBaudRate(baud)
        self.d.setDataCharacteristics(frame, stop, parity)
        self.d.setTimeouts(rTimeout, wTimeout)

        self.liveRegMemory = {x: 0 for x in range(5)}


    def binToVolt(self, binValue, REF):     # For negative values, the ADS122U04 use the Two's complement method. Check ressources about it on internet.
        binValue = binValue & 0xFFFFFF    # The "& 0xFFFFFF" is to ensure that binValue is on 24 bits.
        sign = 1
        if (binValue >> 23):
            sign = -1
            binValue = ~(binValue - 1) & 0xFFFFFF
        return sign * (binValue / pow(2, 23)) * REF
    

    def command(self, operation, data = 0):
        self.d.write(bytes([syncWord]))
        self.d.write(bytes([operation]))
        if (operation == START_RESTART):
            return int.from_bytes(self.d.read(3), 'little')
            # ADD HERE THE FLAG READED FOR liveRegMemory
        elif ((operation >> 4) == 2):
            return int.from_bytes(self.d.read(1), 'little')
        elif ((operation >> 4) == 4):
            self.d.write(bytes([data]))
            self.liveRegMemory[list(WREG.values()).index(operation)] = data     # BE CAREFUL HERE - We are not 100% sure that data has been correctly set.
        elif operation == RESET:
            self.liveRegMemory = {x: 0 for x in range(5)}                       # Same problem here.


    def getTemp(self, regVal=None):    # Return the internal temperature measured by the integrated precision temperature sensor, in Kelvin.    11 bytes (8 sended, 3 received)
        if regVal is None:
            regVal = self.command(RREG[1])

        if not (regVal & 0x01):
            self.command(WREG[1], regVal | 0x01)    # 3 bytes sended

        binValue = self.command(START_RESTART) & 0xFFFFFF   # The "& 0xFFFFFF" is to ensure that binValue is on 24 bits.    5 bytes on line (2 sended, 3 received)
        binValue = binValue >> 10
        sign = 1
        if (binValue >> 13):
            binValue = ~(binValue - 1) & 0xFFFFFF
            sign = -1
        if not (regVal & 0x01):
            self.command(WREG[1], regVal)   # 3 bytes sended
        return (sign * tempResolution * binValue + 273.15)


    def reset(self):    # DO NOT USE THIS METHOD IN A LOOP CONTROLED BY A QTimer, a conflict can occur with the time.sleep() method.
        #RESET
        self.command(RESET)
        time.sleep(0.001)


    def selectAnalog(self, choice):         # 6 bytes on the line (5 write and 1 read)
        self.command(WREG[0], (0xF0 | self.command(RREG[0])) & AIn[choice])


    def setGPIO(self, gpioID, value='INVERT', initialRegVal=None):
        if initialRegVal is None:
            initialRegVal = self.command(RREG[4])
            print(hex(initialRegVal))

        if gpioID not in GPIOs:
            raise ValueError("First argument must be 0, 1 or 2. This is the GPIO ID to set.")

        if value is True:
            reg = {4: initialRegVal | 2**gpioID}
        elif value is False:
            reg = {4: initialRegVal & ~(2**gpioID)}
        elif value == 'INVERT':
            reg = {4: initialRegVal ^ 2**gpioID}
        else:
            raise ValueError("Second argument must be boolean (True or False) or 'INVERT'. This is the state to set for the GPIO.")

        print(hex(reg[4]))
        self.setReg(reg, reset=False)


    def setReg(self, regValues, regToWrite=None, reset=True):    #Write registers values    6 bytes per reg (5 sended, 1 received)
        if regToWrite is None:
            regToWrite = list(regValues.keys())

        if reset:
            self.reset()

        for regID in regToWrite:
            self.command(WREG[regID], regValues.get(regID))
            if regValues.get(regID) != self.command(RREG[regID]):
                return False
        return True


    def supplyREF(self):                    # 11 bytes on the line (7 write and 4 read)
        self.selectAnalog(12)
        return (self.binToVolt(self.command(START_RESTART), ADSinternalREF) * 4)