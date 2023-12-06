VMCS : Versatile Measurement and Control Software
============

VMCS is a PyQt-based Graphical User Interface usable with various measurement and control systems, such as Arduino-based or RaspberryPi-based for example, or homemade ones. The aim of it is to allow acquiring and plotting real-time datas from any measurement and control device(s), by a standard computer. This project describe some ways of using the tool, but the latter have been thought to allow anyone of programming very easily any "kit" under python for desired applications. Then, you can build your own system and connect it to a computer where VMCS is running, to plot your measures from the sensors present in the system, and/or control actuators. The main objective of this project is to give an all-in-one solution while enlarging possibilities with measurement and control prototypes, on experimental benches for example.
> DISCLAIMER : This software stills a prototype and can encouter some bugs, or programming mistakes. I personnaly encourage python-skilled programmers to try giving more proper versions or letting me know of issues that could be improved.

-----------
How does it work ?
-----------

You basically have a computer, on which runs VMCS (what is only a GUI). Then, you'll have to connect your system to the computer by the way you prefer, which can be almost every way while the used one can be controlled by a python program. For example, by way I mean :
- USB
- VGA
- WiFi
- Ethernet
- Bluetooth
- Jack
- HDMI
- etc...

The only issue is that you'll have to find a way to control your system by the way you choose, through python, if the way you choose haven't been already described in the project resources. This is because, if you create your own measurement and control system, you'll have to write a little python file where gonna be the instructions to get the measures and/or controlling the actuators. Of course, this project is expected to become a collaborative project, where realised systems can be shared. So you could find ready-to-use systems if one already correspond to your needs.

VMCS do not really have limits for number of sensors and number of GPIOs, since the GUI shall adapt its layout depending on the given number of sensors and accessible GPIOs in the python program. As you can see below, here is a standard application for VMCS, but you can also put external signals on the GPIOs to control VMCS and start a record for example. You can also choose another interface to communicate with an external GPIO board.

![SchemVMCS](https://github.com/B137P107/VMCS/assets/90220128/ec387962-d1fc-4e69-8b0a-8cb1f4c35e2e)


### Measurement

Your measurements would basically been took by sensors, with analog or digital interface. If it's analog, you'll need to use an ADC to convert measures to numerical values, and send it to the computer through the desired interface. But you can also use the built-in ADC of the computer's Jack port for example, if you have only one sensor. Then, measurements gonna be called by the "kit" python program, to get plotted in the VMCS GUI.
> You may need to power up your sensor(s). This can be done by a power regulation stage, but you must be very careful that the power can't damage the used computer port, if the interface method isn't wireless.

### Control

Here, the control word refer to controlling external devices, or controlling the VMCS interface. In most of cases, controlling things gonna be done by controlling GPIOs. Those GPIOs can be integrated on the acquisition board, or being connected to the computer through another interface from the one for the acquisition board. Controlling external devices could also be done without GPIOs, by interfacing direcly actuators to the computer. Because VMCS is an all-in-one solution, including measurement and control in a single interface, controlling external devices could be done depending on the measurement values.

----------
Speed rates
----------

Ultimately, VMCS is intended to being able to plot datas with a very high time-resolution, up to the fastest existing devices such as 10 GSPS ADC, which means a sample every 0.1 ns. But, for now, since graphs plotted in VMCS are using DateAxisItem from the pyqtgraph package, the maximum resolution is the one of timestamp, which is used in the DateAxisItem. The timestamp resolution is about 1 µs.
Another point is that, VMCS works currently in a 1-by-1 sample mode, and between each sample there is a loop to plot the last one taken. This loop is pretty long because python is a slow to update each graph, and the travelling data through the interface connection can be very slow too. To give an order, this loop has been measured at about 400 ms between each sample with the first version of the _DualPressure - Thermocouple_ kit. This kit was using an UART protocol with RS485 standard interface 10 meters long between the computer and the acquisition board, using the following devices and parameters :
- a USB to UART bridge (FT231XS) ;
- two RS485 transceivers, at both ends of the interface (MAX14840) ;
- a 24 bits ADC with a sample rate of 2000 SPS (ADS122U04) ;
- 3 analog sensors ;
- a 9600 baud rate on communication line ;
- with 102 bytes exchanged per loop between the computer and the acquisition board, neglecting the usage of GPIOs integrated to the ADC.

Then, we can calculate that the data exchange on the line contribute for $102\times 8\times 1/9600 = 85\ ms$ per loop theorically. This means that the approximative rest of about 315 ms is due to the execution of pythons instructions. So the lever to improve the speed rate of the system, is to minimizing the number of python instructions per sample update. To perform this, we can consider acquiring multiple samples in a row without asking for each sample, and instead asking for a quantity N of samples. Then, the plot(s) in VMCS shall update by bursts of N samples, each separated by the used conversion rate of the ADC. In the figure below, I provide an example of an UART frame from the computer (using a USB to UART bridge or other), asking for N samples to the acquisition board. Because there is more than 1 sensor on the acquisition board, the ADC will need to switch from the first to the second sensor. This is usually performed by rewriting a register in the ADC, which need to send another frame to the ADC. Because we don't want to send too much frame from the VMCS interface (which is python-based and slow), we may use a microcontroller between the computer and the ADC, that be in charge of sending those switching sensor frame.

![FrameExample_SpeedVMCS](https://github.com/B137P107/VMCS/assets/90220128/39207165-092f-4367-8cf9-02612f43396d)


----------
Some examples of use
----------
