"""
Arduino Firmata Test Script
===========================

A simple script to test communication with an Arduino board using the Firmata protocol.
This script reads analog values from pin A0 and prints them to the console.

Usage:
    python #TestArduinoFirmata.py

Note:
    Make sure to replace 'COM4' with the correct serial port for your Arduino.
"""

from pyfirmata2 import *
import time


def main():
    """
    Main function to initialize Arduino board and read analog values.
    
    This function sets up the Arduino board, configures analog input A0,
    and continuously reads and prints analog values.
    
    :return: None
    :rtype: None
    """
    # Initialisation de la carte Arduino
    board = Arduino('COM4')  # Remplace par le bon port si nécessaire
    it = util.Iterator(board)
    it.start()

    # Configuration de la broche analogique A0 en entrée
    #analog_input = board.get_pin('a:0:i')
    board.analog[0].mode = INPUT

    # Boucle de lecture
    while True:
        #board.iterate()  # Remplace l'Iterator de pyfirmata
        analog_value = board.analog[0].value
        if analog_value is not None:  # Vérifie que la lecture est valide
            print(analog_value)
        time.sleep(0.1)


if __name__ == "__main__":
    main()
