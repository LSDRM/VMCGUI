VMCGUI : Versatile Measurement and Control GUI
============
VMCGUI is a PyQt-based Graphical User Interface usable with various measurement and control systems, such as Arduino-based or RaspberryPi-based devices for example, or homemade prototypes. Because developers always reprogram GUIs to plot data of each cnceived system, we provide here an interface that can be used with any system, without rewriting the source code. For each system you conceive, you'll have to write a little file containing informations on it, then VMCGUI shall adapt its layer to your needs. The aim of this is to allow acquiring and plotting real-time data from any measurement and control device(s), by a standard computer. This project describes some ways of using the tool, but these have been designed to make it very easy for anyone to program any "kit" in Python for the desired applications. Then, you can build your own system and connect it to a computer where VMCGUI is running, plot your measures from the sensors present in the system, and/or control actuators. The main objective of this project is to give an all-in-one solution while enlarging possibilities with measurement and control prototypes, on experimental benches for example.

![VMCGUIdebugWindow](https://github.com/LSDRM/VMCGUI/assets/90220128/dec16cbf-e683-49de-94b1-37517d74c975)

> DISCLAIMER : This software is still a prototype and can encouter some bugs, or programming mistakes. I personnaly encourage python-skilled programmers to try giving more proper versions or letting me know about issues that could be fixed.

# [Link to available kits](https://github.com/LSDRM/VMC_Kits)

-----------
Features
-----------

- Adaptative interface to number of sensors and accessible GPIOs.
- Designed to allow very fast sample rate mode.
- Usable without or with any communication protocol from the computer.
- All-in-one solution to correlate control with taken measures.
- Record real-time measurements at sample rate.
- Processing recorded measurements.

-----------
How does it work ?
-----------

You basically have a computer, on which runs VMCGUI. Then, you'll have to connect your system to the computer by the way you prefer, which can be almost every way while the used one can be controlled by a python program. For example, by way I mean :
- USB
- VGA
- WiFi
- Ethernet
- Bluetooth
- Jack
- HDMI
- etc...

The only thing is that you'll have to find a way to control your system by the way you choose, through python, if the way you choose has not been already described in the project resources. This is because, if you create your own measurement and control system, you'll have to write a python file with the instructions to get the measures and/or control the actuators. In short, this python file will make the link between VMCGUI and your system, through the desired communication port. Of course, this project is expected to become a collaborative project, where realised systems can be shared. So you could look at [ready-to-use systems](https://github.com/LSDRM/VMC_Kits) if there is already a project correspond to your needs.

VMCGUI does not really have limits for number of sensors and number of GPIOs, since the GUI shall adapt its layout depending on the given number of sensors and accessible GPIOs in the python program. As you can see below, here is a standard application for VMCGUI, but you can also put external signals on the GPIOs to control VMCGUI and start a record for example. You can also choose another communication port to communicate with an external GPIO board.

![SchemVMCGUI](https://github.com/LSDRM/VMCGUI/assets/90220128/94628862-4fd2-4fd5-8ba4-6a6e3a3556e8)

Measurement
---------

Your measurements would basically be taken by sensors, with analog or digital outputs. If it's analog, you'll need to use an ADC to convert measures to numerical values, and send it to the computer through the desired protocol/communication port. But you can also use the built-in ADC of the computer's Jack port for example, if you have only one sensor. Then, measurements can be called by the "kit" python program, to get plotted in the VMCGUI.
> You may need to power up your sensor(s). This can be done by a power regulation stage, but care must be taken to ensure that the power supply does not damage the computer port used, if the communication method is not wireless.

Control
---------

Here, the word 'control' refers to controlling external devices, or controlling the VMCGUI. In most cases, control can be done by GPIOs. Those GPIOs can be integrated on the acquisition board, or can be connected to the computer through another communication method on the acquisition board. Controlling external devices could also be done without GPIOs, by interfacing direcly actuators to the computer, through a serial port for example. Because VMCGUI is an all-in-one solution including measurement and control in a single interface, controlling external devices could be done depending on the measurement values.

Speed rates
----------

Ultimately, VMCGUI is intended to being able to plot data with a very high time-resolution, up to the fastest existing devices such as 10 GSPS ADC, which means sampling every 0.1 ns. But, for now, since graphs plotted in VMCGUI are using DateAxisItem from the pyqtgraph package, the maximum resolution is the one of timestamp, which is used in the DateAxisItem package. The timestamp **maximum resolution is about 1 µs**.
Another point is that, when VMCGUI works in a 1-by-1 sample mode, a loop is executed between each sample to plot. This loop is quite long because python is slow to update each graph, and the transfer of data through the communication line can also be slow. To give an order of magnitude, this loop has been measured at about 400 ms between each sample with the first version of the [_DualPressure - Thermocouple_](https://github.com/LSDRM/VMCS/tree/88da0f7f0afaeebaeeff0f13b5e0fb5d95d4da9f/Kits/Personnalized/DualPressure%20-%20Thermocouple) kit, which was working in 1-by-1 sample mode. This kit was using an UART protocol with RS485 standard on a 10 meters long communication line between the computer and the acquisition board, using the following devices and parameters :
- a USB to UART bridge chip (FT231XS) ;
- two RS485 transceivers, at both ends of the line (MAX14840) ;
- a 24 bits ADC with a sample rate of 2000 SPS (ADS122U04) ;
- 3 analog sensors ;
- a 9600 baud rate on communication line ;
- for a total of 102 bytes exchanged per loop between the computer and the acquisition board, neglecting the usage of GPIOs integrated to the ADC.

Then, we can calculate that the data exchange on the line contribute for $102\times 8\times 1/9600 = 85\ ms$ per loop theorically. This means that the approximative remaining of ca. 315 ms is due to the execution of pythons instructions. So the lever to improve the speed rate of the system, is to minimize the number of python instructions updating the sampling. To perform this, we can consider acquiring multiple samples in a row without asking for each sample, and instead asking for a quantity N of samples. Then, the plot(s) in VMCGUI shall update by groups of N samples, each separated by the used analog-to-digital conversion rate. In the figure below, I provide an example of an UART frame from the computer in N-by-N mode (using a USB to UART bridge or other), asking for N samples to the acquisition board. Because there is more than 1 sensor on the acquisition board, the ADC will need to switch from the first to the second sensor. This is usually performed by rewriting a register in the ADC, which needs to send another frame to the ADC. Because we don't want to send too much frame from the VMCGUI (which is python-based and slow), we may use a microcontroller between the computer and the ADC, in charge of sending frames from the switching sensors. In this configuration, the microcontroller must be preprogrammed to understand what it has to do when receiving the frames containing the number N. The preprogramming can be performed on starting VMCGUI in the "kit" python file, or outside VMCGUI using another software (e.g. Arduino IDE for an Arduino-based acquisition board). The used microcontroller can either store all N samples before sending them, or immediatly send each sample after acquisition.

![FrameExample_SpeedVMCGUI](https://github.com/LSDRM/VMCGUI/assets/90220128/02528a34-c2c1-4371-a49f-7c6ee312eada)

----------
Recording measurements and data processing
----------

VMCGUI provides a recording solution to store your measurements in files. Once recorded, you can reopen and plot your datas to generate SVG, matplotlib, CSV,... files and graphs.
> Math operations on plots and between plots in the "Load Data" window are also possible but still under debugging.

----------
Some examples of use
----------

#### Using an Arduino
The configuration that may be the most used with VMCGUI is probably using an Arduino connected to the computer through USB. This configuration is probably the most simple to set up, because it doesn't need complex development of special data acquisition board. You only need to connect your sensors and actuators to the Arduino as suggested in the documentation of the sensors/actuators, or in the Arduino's documentation if it exists. Then, you'll need to talk to the Arduino through python commands, in the "kit" python file of VMCGUI. This can be performed in a very simple way with the _pyfirmata_ library (see https://realpython.com/arduino-python/).
![ArduinoVMCGUI](https://github.com/LSDRM/VMCGUI/assets/90220128/c96c5503-698c-4395-bbb2-7d02e16ce7b0)

#### Customized acquisition board over long distances
Since VMCGUI has been firstly developed for long distance (about 10 meters) applications and highly noisy environment, the main configuration that has been studied is the following one, using UART communication protocol through RS485 or RS422 standards. This configuration enables one to embed the acquisition board on a system with difficult accessibility, through wire connections. The "Data Acquisition IC" could be a microcontroller with ADC, or directly an ADC that has UART communication protocol (e.g. ADS122U04 which include GPIOs).
> Note that in the latter case, with direct connection to an UART ADC, you will not be able to have very fast sample rate with more than one sensor. This is because an ADC generally needs to receive commands to switch its conversion channels between sensors. Then, the N-by-N mode is not possible in this exact configuration.

![VMCGUI_LongDistanceConfiguration](https://github.com/LSDRM/VMCGUI/assets/90220128/cb748075-adc9-4e3e-bb2a-635fa3053f11)

#### Wireless acquisition board
The previous configuration shows one way of integrating the frame grabber on long-distance or hard-to-reach systems. This configuration enables the acquisition board to be integrated into systems with a wireless connection to the computer. Setting up such a configuration may be a little trickier, but remains a possibility for your system if wireless connection is essential.

![WirelessVMCGUI](https://github.com/LSDRM/VMCGUI/assets/90220128/45908e5b-929a-4879-90e2-334011e7733c)

-----------
Install
-----------

First of all, make sure you already have installed Python 3.8 at least on your computer. No elaborate compatibility tests have been performed for different python versions with the interface, but I recommend to use versions not too far from the ones given in the next section.

Clone this repository to the folder you want on your computer, then run `pip install -r "C:\...\VMCGUI\APP\requirements.txt"` in the command prompt. Don't forget to replace `C:\...\` by the path where you cloned the current repository.
> The previous path is given under Windows format, so be sure of using the correct path format if you are not working under Windows.

Now, you can start the interface using python with the following command : `python VMCGUI.py`

----------
Compatibility
----------

For now, VMCGUI has been developped under Windows 10, and has not been tested on Mac and Linux. The app is given as Python source code, so needs Python and few libraries to be installed. VMCGUI is reported to works fine with versions :
- Python 3.11.3
- pyqtgraph 0.13.3
- numpy 1.24.3
- scipy 1.10.1
- PyQt5 5.15.9
- PyQtWebEngine 5.15.6
