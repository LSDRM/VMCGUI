VMCS : Versatile Measurement and Control Software
============

VMCS is a Graphical User Interface usable with various measurement and control systems, such as Arduino-based or RaspberryPi-based for example, or homemade ones. The aim of it is to allow acquiring real-time datas from any measurement and control device(s), by a standard computer. This project describe some ways of using the tool, but the latter have been thought to allow anyone of programming very easily any "kit" for desired applications. Then, you can build your own system and connect it to a computer where VMCS is running, to plot your measures from the sensors present in the system, and/or control actuators. The main objective of this project is to give an all-in-one solution while enlarging possibilities with measurement and control prototypes, on experimental benches for example.

-----------
How does it work ?
-----------

You basically have a computer, on which runs VMCS (what is only a GUI). Then, you'll have to connect your system to the computer by the way you prefer, which can be almost every way while the used one can be piloted by a python program. For example, by way I mean :
- USB
- VGA
- WiFi
- Ethernet
- Bluetooth
- Jack
- HDMI
- etc...

The only issue is that you'll have to find a way to control your system by the way you choose, through python, if the way you choose haven't been already described in the project resources. This is because, if you create your own measurement and control system, you'll have to write a little python file where gonna be the instructions to get the measures and/or controlling the actuators. Of course, this project is expected to become a collaborative project, where realised system can be shared. So you could find ready-to-use systems if one already correspond to your needs.
