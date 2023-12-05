VMCS : Versatile Measurement and Control Software
============

VMCS is a Graphical User Interface usable with various measurement and control systems, such as Arduino-based or RaspberryPi-based for example, or homemade ones. The aim of it is to allow acquiring and plotting real-time datas from any measurement and control device(s), by a standard computer. This project describe some ways of using the tool, but the latter have been thought to allow anyone of programming very easily any "kit" under python for desired applications. Then, you can build your own system and connect it to a computer where VMCS is running, to plot your measures from the sensors present in the system, and/or control actuators. The main objective of this project is to give an all-in-one solution while enlarging possibilities with measurement and control prototypes, on experimental benches for example.

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

Your measurements would basically been took by sensors, with analog or digital interface. If it's analog, you'll need to use an ADC to convert measures to numerical values, and send it to the computer through the desired interface. But you can also use the built-in ADC of the computer's Jack port for example, if you have only one sensor.
Nevertheless, you may need to power up your sensor(s). This can be done by a power regulation stage, but you must be very careful that the power can't damage the used computer port, if the interface method isn't wireless.


## Speed
