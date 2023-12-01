EESchema Schematic File Version 4
LIBS:DualPressure_V1-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Customs:ABP2D ABP2D0
U 1 1 63406D3C
P 3900 3800
F 0 "ABP2D0" H 3900 4215 50  0000 C CNN
F 1 "ABP2D" H 3900 4124 50  0000 C CNN
F 2 "SamacSys_Parts:ABP2D" H 3900 3800 50  0001 C CNN
F 3 "" H 3900 3800 50  0001 C CNN
	1    3900 3800
	1    0    0    -1  
$EndComp
$Comp
L Customs:ABP2D ABP2D1
U 1 1 63406F6E
P 5200 3800
F 0 "ABP2D1" H 5200 4215 50  0000 C CNN
F 1 "ABP2D" H 5200 4124 50  0000 C CNN
F 2 "SamacSys_Parts:ABP2D" H 5200 3800 50  0001 C CNN
F 3 "" H 5200 3800 50  0001 C CNN
	1    5200 3800
	1    0    0    -1  
$EndComp
$Comp
L SamacSys_Parts:ADS122U04IPW IC1
U 1 1 6340928D
P 3500 4500
F 0 "IC1" H 4300 4765 50  0000 C CNN
F 1 "ADS122U04IPW" H 4300 4674 50  0000 C CNN
F 2 "SamacSys_Parts:SOP65P640X120-16N" H 4950 4600 50  0001 L CNN
F 3 "http://www.ti.com/lit/ds/symlink/ads122u04.pdf" H 4950 4500 50  0001 L CNN
F 4 "24-bit, 2-kSPS, 4-ch, low-power, small-size delta-sigma ADC w/ PGA, VREF, 2x IDACs & UART interface" H 4950 4400 50  0001 L CNN "Description"
F 5 "1.2" H 4950 4300 50  0001 L CNN "Height"
F 6 "595-ADS122U04IPW" H 4950 4200 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Texas-Instruments/ADS122U04IPW?qs=gt1LBUVyoHlLONlNwdsm%2Fg%3D%3D" H 4950 4100 50  0001 L CNN "Mouser Price/Stock"
F 8 "Texas Instruments" H 4950 4000 50  0001 L CNN "Manufacturer_Name"
F 9 "ADS122U04IPW" H 4950 3900 50  0001 L CNN "Manufacturer_Part_Number"
	1    3500 4500
	1    0    0    -1  
$EndComp
Text Label 5100 4800 0    50   ~ 0
3.3V
Text Label 5100 4900 0    50   ~ 0
5V
Text Label 5100 5200 0    50   ~ 0
5V
$Comp
L power:GND #PWR0101
U 1 1 6340C18A
P 3500 5200
F 0 "#PWR0101" H 3500 4950 50  0001 C CNN
F 1 "GND" V 3505 5072 50  0000 R CNN
F 2 "" H 3500 5200 50  0001 C CNN
F 3 "" H 3500 5200 50  0001 C CNN
	1    3500 5200
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 6340C67A
P 3500 4850
F 0 "#PWR0102" H 3500 4600 50  0001 C CNN
F 1 "GND" V 3505 4722 50  0000 R CNN
F 2 "" H 3500 4850 50  0001 C CNN
F 3 "" H 3500 4850 50  0001 C CNN
	1    3500 4850
	0    1    1    0   
$EndComp
Wire Wire Line
	3500 4800 3500 4850
Connection ~ 3500 4850
Wire Wire Line
	3500 4850 3500 4900
$Comp
L SamacSys_Parts:MAX14840EATA+ IC0
U 1 1 6340D08A
P 6300 4500
F 0 "IC0" H 6800 4765 50  0000 C CNN
F 1 "MAX14840EATA+" H 6800 4674 50  0000 C CNN
F 2 "SamacSys_Parts:SON65P300X300X80-9N" H 7150 4600 50  0001 L CNN
F 3 "https://pdfserv.maximintegrated.com/en/ds/MAX14840E-MAX14841E.pdf" H 7150 4500 50  0001 L CNN
F 4 "-40NC to +125NC" H 7150 4400 50  0001 L CNN "Description"
F 5 "0.8" H 7150 4300 50  0001 L CNN "Height"
F 6 "N/A" H 7150 4200 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Maxim-Integrated/MAX14840EATA%2b?qs=U8%2FOE6X5Fv9GPXw9Qhloyw%3D%3D" H 7150 4100 50  0001 L CNN "Mouser Price/Stock"
F 8 "Maxim Integrated" H 7150 4000 50  0001 L CNN "Manufacturer_Name"
F 9 "MAX14840EATA+" H 7150 3900 50  0001 L CNN "Manufacturer_Part_Number"
	1    6300 4500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 6340E7ED
P 7300 4800
F 0 "#PWR0103" H 7300 4550 50  0001 C CNN
F 1 "GND" V 7305 4672 50  0000 R CNN
F 2 "" H 7300 4800 50  0001 C CNN
F 3 "" H 7300 4800 50  0001 C CNN
	1    7300 4800
	0    -1   -1   0   
$EndComp
Text Label 7300 4500 0    50   ~ 0
3.3V
$Comp
L power:GND #PWR0104
U 1 1 6340EC33
P 6800 5300
F 0 "#PWR0104" H 6800 5050 50  0001 C CNN
F 1 "GND" H 6805 5127 50  0000 C CNN
F 2 "" H 6800 5300 50  0001 C CNN
F 3 "" H 6800 5300 50  0001 C CNN
	1    6800 5300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 6340EDCF
P 5600 3650
F 0 "#PWR0105" H 5600 3400 50  0001 C CNN
F 1 "GND" V 5605 3522 50  0000 R CNN
F 2 "" H 5600 3650 50  0001 C CNN
F 3 "" H 5600 3650 50  0001 C CNN
	1    5600 3650
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 6340EFB3
P 4300 3650
F 0 "#PWR0106" H 4300 3400 50  0001 C CNN
F 1 "GND" V 4305 3522 50  0000 R CNN
F 2 "" H 4300 3650 50  0001 C CNN
F 3 "" H 4300 3650 50  0001 C CNN
	1    4300 3650
	0    -1   -1   0   
$EndComp
Text Label 3500 3650 2    50   ~ 0
5V
Text Label 4800 3650 2    50   ~ 0
5V
$Comp
L Device:R R0
U 1 1 6341A86E
P 7800 4650
F 0 "R0" H 7870 4696 50  0000 L CNN
F 1 "120" H 7870 4605 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 7730 4650 50  0001 C CNN
F 3 "~" H 7800 4650 50  0001 C CNN
	1    7800 4650
	1    0    0    -1  
$EndComp
Wire Wire Line
	7300 4700 7650 4700
Wire Wire Line
	7650 4700 7650 4800
Wire Wire Line
	7650 4800 7800 4800
Wire Wire Line
	7300 4600 7650 4600
Wire Wire Line
	7650 4600 7650 4500
Wire Wire Line
	7650 4500 7800 4500
Text Label 4300 3950 0    50   ~ 0
AIN0
Text Label 5600 3950 0    50   ~ 0
AIN1
NoConn ~ 5600 3800
NoConn ~ 4800 3800
NoConn ~ 4800 3950
NoConn ~ 4300 3800
NoConn ~ 3500 3800
NoConn ~ 3500 3950
Text Label 5100 5000 0    50   ~ 0
AIN0
Text Label 5100 5100 0    50   ~ 0
AIN1
Text Label 3500 4700 2    50   ~ 0
3.3V
Wire Wire Line
	6300 4600 6250 4600
$Comp
L SamacSys_Parts:LM2576D2TR4-5G REG0
U 1 1 633FF0F6
P 7500 2450
F 0 "REG0" H 8200 2715 50  0000 C CNN
F 1 "LM2576D2TR4-5G" H 8200 2624 50  0000 C CNN
F 2 "SamacSys_Parts:D2TSUFFIX-CASE936A-02-ISSUEC" H 8750 2550 50  0001 L CNN
F 3 "" H 8750 2450 50  0001 L CNN
F 4 "Voltage Regulators - Switching Regulators 5V 3A Buck PWM" H 8750 2350 50  0001 L CNN "Description"
F 5 "" H 8750 2250 50  0001 L CNN "Height"
F 6 "863-LM2576D2TR4-5G" H 8750 2150 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/onsemi/LM2576D2TR4-5G?qs=2OtswVQKCOEvcMP8GU0oog%3D%3D" H 8750 2050 50  0001 L CNN "Mouser Price/Stock"
F 8 "onsemi" H 8750 1950 50  0001 L CNN "Manufacturer_Name"
F 9 "LM2576D2TR4-5G" H 8750 1850 50  0001 L CNN "Manufacturer_Part_Number"
	1    7500 2450
	1    0    0    -1  
$EndComp
$Comp
L SamacSys_Parts:AP7333-33SAG-7 REG1
U 1 1 6340145C
P 6350 2050
F 0 "REG1" H 6850 2315 50  0000 C CNN
F 1 "AP7333-33SAG-7" H 6850 2224 50  0000 C CNN
F 2 "SamacSys_Parts:SOT96P240X135-3N" H 7200 2150 50  0001 L CNN
F 3 "https://www.diodes.com/assets/Datasheets/AP7333.pdf" H 7200 2050 50  0001 L CNN
F 4 "LDO Regulator Pos 3.3V 0.3A 3Pin SOT23 Diodes Inc AP7333 AP7333-33SAG-7, Single Linear Voltage Regulator, 300mA 3.3 V, +/-2%, 3-Pin SOT-23" H 7200 1950 50  0001 L CNN "Description"
F 5 "1.35" H 7200 1850 50  0001 L CNN "Height"
F 6 "621-AP7333-33SAG-7" H 7200 1750 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Diodes-Incorporated/AP7333-33SAG-7?qs=vIZ3oKQCLxpWqm5zu2HqxA%3D%3D" H 7200 1650 50  0001 L CNN "Mouser Price/Stock"
F 8 "Diodes Inc." H 7200 1550 50  0001 L CNN "Manufacturer_Name"
F 9 "AP7333-33SAG-7" H 7200 1450 50  0001 L CNN "Manufacturer_Part_Number"
	1    6350 2050
	1    0    0    -1  
$EndComp
$Comp
L Device:C C0
U 1 1 63402731
P 7700 1900
F 0 "C0" H 7815 1946 50  0000 L CNN
F 1 "100u" H 7815 1855 50  0000 L CNN
F 2 "Capacitor_SMD:CP_Elec_8x10.5" H 7738 1750 50  0001 C CNN
F 3 "~" H 7700 1900 50  0001 C CNN
	1    7700 1900
	1    0    0    -1  
$EndComp
Text Label 7500 1650 2    50   ~ 0
POWER
$Comp
L power:GND #PWR0108
U 1 1 63402CBF
P 7700 2050
F 0 "#PWR0108" H 7700 1800 50  0001 C CNN
F 1 "GND" H 7705 1877 50  0000 C CNN
F 2 "" H 7700 2050 50  0001 C CNN
F 3 "" H 7700 2050 50  0001 C CNN
	1    7700 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	7500 2450 7500 1650
Wire Wire Line
	7500 1650 7700 1650
Wire Wire Line
	7700 1650 7700 1750
$Comp
L power:GND #PWR0109
U 1 1 6340B584
P 7050 3200
F 0 "#PWR0109" H 7050 2950 50  0001 C CNN
F 1 "GND" H 7055 3027 50  0000 C CNN
F 2 "" H 7050 3200 50  0001 C CNN
F 3 "" H 7050 3200 50  0001 C CNN
	1    7050 3200
	1    0    0    -1  
$EndComp
$Comp
L Device:L L0
U 1 1 6340C1CA
P 6800 2550
F 0 "L0" V 6990 2550 50  0000 C CNN
F 1 "100u" V 6899 2550 50  0000 C CNN
F 2 "Inductor_SMD:L_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 6800 2550 50  0001 C CNN
F 3 "~" H 6800 2550 50  0001 C CNN
	1    6800 2550
	0    -1   -1   0   
$EndComp
$Comp
L Device:C C1
U 1 1 6340DB4A
P 6550 2850
F 0 "C1" H 6665 2896 50  0000 L CNN
F 1 "1000u" H 6665 2805 50  0000 L CNN
F 2 "Capacitor_SMD:CP_Elec_10x10.5" H 6588 2700 50  0001 C CNN
F 3 "~" H 6550 2850 50  0001 C CNN
	1    6550 2850
	1    0    0    -1  
$EndComp
Connection ~ 7050 3150
$Comp
L power:GND #PWR0110
U 1 1 63410090
P 7350 2050
F 0 "#PWR0110" H 7350 1800 50  0001 C CNN
F 1 "GND" H 7355 1877 50  0000 C CNN
F 2 "" H 7350 2050 50  0001 C CNN
F 3 "" H 7350 2050 50  0001 C CNN
	1    7350 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 2050 6150 2550
Text Label 6150 2050 2    50   ~ 0
5V
Wire Wire Line
	7050 3150 7500 3150
Text Label 8900 2450 0    50   ~ 0
5V
$Comp
L SamacSys_Parts:AM-K-PCB U0
U 1 1 6341456D
P 3100 2950
F 0 "U0" H 3550 3215 50  0000 C CNN
F 1 "AM-K-PCB" H 3550 3124 50  0000 C CNN
F 2 "SamacSys_Parts:AMKPCB" H 3850 3050 50  0001 L CNN
F 3 "" H 3850 2950 50  0001 L CNN
F 4 "SOCKET, K, ANSI, MINI, PCB; Gender:Socket; Thermocouple Type:K; Product Range:-; SVHC:No SVHC (15-Jan-2019); For Use With:K Type Thermocouples RoHS Compliant: Yes" H 3850 2850 50  0001 L CNN "Description"
F 5 "8" H 3850 2750 50  0001 L CNN "Height"
F 6 "" H 3850 2650 50  0001 L CNN "Mouser Part Number"
F 7 "" H 3850 2550 50  0001 L CNN "Mouser Price/Stock"
F 8 "LABFACILITY" H 3850 2450 50  0001 L CNN "Manufacturer_Name"
F 9 "AM-K-PCB" H 3850 2350 50  0001 L CNN "Manufacturer_Part_Number"
	1    3100 2950
	1    0    0    -1  
$EndComp
NoConn ~ 4000 2950
Text Label 6400 3850 2    50   ~ 0
POWER
$Comp
L Device:C C2
U 1 1 63440523
P 6050 2850
F 0 "C2" H 6165 2896 50  0000 L CNN
F 1 "1u" H 6165 2805 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 6088 2700 50  0001 C CNN
F 3 "~" H 6050 2850 50  0001 C CNN
	1    6050 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 2150 6050 2150
Text Label 6050 2150 2    50   ~ 0
3.3V
$Comp
L Device:R R1
U 1 1 6344AB3B
P 5450 4500
F 0 "R1" V 5400 4700 50  0000 C CNN
F 1 "47" V 5450 4500 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 5380 4500 50  0001 C CNN
F 3 "~" H 5450 4500 50  0001 C CNN
	1    5450 4500
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 6344C684
P 5450 4600
F 0 "R2" V 5400 4800 50  0000 C CNN
F 1 "47" V 5450 4600 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 5380 4600 50  0001 C CNN
F 3 "~" H 5450 4600 50  0001 C CNN
	1    5450 4600
	0    1    1    0   
$EndComp
Wire Wire Line
	5800 4600 5800 4800
Wire Wire Line
	5800 4800 6300 4800
$Comp
L Device:R R3
U 1 1 6345D9BB
P 5450 4700
F 0 "R3" V 5400 4900 50  0000 C CNN
F 1 "47" V 5450 4700 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 5380 4700 50  0001 C CNN
F 3 "~" H 5450 4700 50  0001 C CNN
	1    5450 4700
	0    1    1    0   
$EndComp
Wire Wire Line
	5100 4500 5300 4500
Wire Wire Line
	5100 4600 5300 4600
Wire Wire Line
	5100 4700 5300 4700
Wire Wire Line
	5600 4600 5800 4600
Wire Wire Line
	5600 4500 6300 4500
$Comp
L Device:R R5
U 1 1 634637AB
P 3150 4600
F 0 "R5" V 3100 4400 50  0000 C CNN
F 1 "47" V 3150 4600 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 3080 4600 50  0001 C CNN
F 3 "~" H 3150 4600 50  0001 C CNN
	1    3150 4600
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 63464BA3
P 3150 4500
F 0 "R4" V 3100 4300 50  0000 C CNN
F 1 "47" V 3150 4500 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 3080 4500 50  0001 C CNN
F 3 "~" H 3150 4500 50  0001 C CNN
	1    3150 4500
	0    1    1    0   
$EndComp
Wire Wire Line
	3300 4600 3500 4600
Wire Wire Line
	3300 4500 3500 4500
Text Label 2850 4600 2    50   ~ 0
GPIO0
Text Label 2500 4500 2    50   ~ 0
GPIO1
Text Label 5900 4950 0    50   ~ 0
GPIO2
Wire Wire Line
	5600 4700 5700 4700
Wire Wire Line
	5700 4700 5700 4950
Text Label 5350 3100 0    50   ~ 0
GPIO0
Text Label 5350 3000 0    50   ~ 0
GPIO1
Text Label 5350 2900 0    50   ~ 0
GPIO2
$Comp
L Device:R R6
U 1 1 6347B812
P 3000 2600
F 0 "R6" H 3000 2750 50  0000 L CNN
F 1 "1M" H 3050 2650 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 2930 2600 50  0001 C CNN
F 3 "~" H 3000 2600 50  0001 C CNN
	1    3000 2600
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R7
U 1 1 6347BC40
P 3000 3400
F 0 "R7" H 3000 3550 50  0000 L CNN
F 1 "1M" H 3050 3450 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 2930 3400 50  0001 C CNN
F 3 "~" H 3000 3400 50  0001 C CNN
	1    3000 3400
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR0112
U 1 1 6347C125
P 3000 3600
F 0 "#PWR0112" H 3000 3350 50  0001 C CNN
F 1 "GND" H 3005 3427 50  0000 C CNN
F 2 "" H 3000 3600 50  0001 C CNN
F 3 "" H 3000 3600 50  0001 C CNN
	1    3000 3600
	-1   0    0    -1  
$EndComp
Text Label 3000 2350 0    50   ~ 0
5V
$Comp
L Device:R R8
U 1 1 6347C844
P 2750 2850
F 0 "R8" V 2650 2850 50  0000 C CNN
F 1 "1k" V 2750 2850 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 2680 2850 50  0001 C CNN
F 3 "~" H 2750 2850 50  0001 C CNN
	1    2750 2850
	0    -1   1    0   
$EndComp
$Comp
L Device:R R9
U 1 1 6347CC55
P 2750 3150
F 0 "R9" V 2650 3150 50  0000 C CNN
F 1 "1k" V 2750 3150 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 2680 3150 50  0001 C CNN
F 3 "~" H 2750 3150 50  0001 C CNN
	1    2750 3150
	0    -1   1    0   
$EndComp
$Comp
L Device:C C7
U 1 1 6347CED9
P 2500 3400
F 0 "C7" H 2650 3500 50  0000 R CNN
F 1 "10n" H 2750 3400 50  0000 R CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 2538 3250 50  0001 C CNN
F 3 "~" H 2500 3400 50  0001 C CNN
	1    2500 3400
	-1   0    0    -1  
$EndComp
$Comp
L Device:C C6
U 1 1 6347D497
P 2500 2600
F 0 "C6" H 2650 2700 50  0000 R CNN
F 1 "10n" H 2750 2600 50  0000 R CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 2538 2450 50  0001 C CNN
F 3 "~" H 2500 2600 50  0001 C CNN
	1    2500 2600
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR0113
U 1 1 63486059
P 2500 3600
F 0 "#PWR0113" H 2500 3350 50  0001 C CNN
F 1 "GND" H 2505 3427 50  0000 C CNN
F 2 "" H 2500 3600 50  0001 C CNN
F 3 "" H 2500 3600 50  0001 C CNN
	1    2500 3600
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR0114
U 1 1 63486393
P 2500 2400
F 0 "#PWR0114" H 2500 2150 50  0001 C CNN
F 1 "GND" H 2505 2227 50  0000 C CNN
F 2 "" H 2500 2400 50  0001 C CNN
F 3 "" H 2500 2400 50  0001 C CNN
	1    2500 2400
	1    0    0    1   
$EndComp
Wire Wire Line
	3000 3550 3000 3600
Wire Wire Line
	2600 2850 2500 2850
Wire Wire Line
	2600 3150 2500 3150
Wire Wire Line
	2500 3150 2500 3250
Wire Wire Line
	2500 2750 2500 2850
Wire Wire Line
	2500 2450 2500 2400
Wire Wire Line
	2500 3550 2500 3600
Wire Wire Line
	3000 2350 3000 2450
$Comp
L Device:C C8
U 1 1 634C1DCD
P 2500 3000
F 0 "C8" H 2650 3100 50  0000 R CNN
F 1 "10u" H 2750 3000 50  0000 R CNN
F 2 "Capacitor_SMD:C_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 2538 2850 50  0001 C CNN
F 3 "~" H 2500 3000 50  0001 C CNN
	1    2500 3000
	-1   0    0    -1  
$EndComp
Connection ~ 2500 2850
Connection ~ 2500 3150
Text Label 2100 2850 2    50   ~ 0
AIN2
Text Label 2100 3150 2    50   ~ 0
AIN3
Wire Wire Line
	2500 2850 2100 2850
Wire Wire Line
	2500 3150 2100 3150
Text Label 3500 5000 2    50   ~ 0
AIN3
Text Label 3500 5100 2    50   ~ 0
AIN2
Wire Wire Line
	2900 2850 3000 2850
Wire Wire Line
	2900 3150 3000 3150
Wire Wire Line
	3000 2750 3000 2850
Wire Wire Line
	3000 3150 3000 3250
Wire Wire Line
	3100 2950 3000 2950
Wire Wire Line
	3000 2950 3000 2850
Connection ~ 3000 2850
Wire Wire Line
	3100 3050 3000 3050
Wire Wire Line
	3000 3050 3000 3150
Connection ~ 3000 3150
$Comp
L Device:C C5
U 1 1 63537CE2
P 2850 4850
F 0 "C5" H 2965 4896 50  0000 L CNN
F 1 "FC" H 2965 4805 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2888 4700 50  0001 C CNN
F 3 "~" H 2850 4850 50  0001 C CNN
	1    2850 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 4700 2850 4600
$Comp
L power:GND #PWR0115
U 1 1 6353FA62
P 2850 5050
F 0 "#PWR0115" H 2850 4800 50  0001 C CNN
F 1 "GND" H 2855 4877 50  0000 C CNN
F 2 "" H 2850 5050 50  0001 C CNN
F 3 "" H 2850 5050 50  0001 C CNN
	1    2850 5050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 5000 2850 5050
Wire Wire Line
	2850 4600 3000 4600
$Comp
L Device:C C4
U 1 1 63543D42
P 2500 4850
F 0 "C4" H 2615 4896 50  0000 L CNN
F 1 "FC" H 2615 4805 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 2538 4700 50  0001 C CNN
F 3 "~" H 2500 4850 50  0001 C CNN
	1    2500 4850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0116
U 1 1 63544208
P 2500 5050
F 0 "#PWR0116" H 2500 4800 50  0001 C CNN
F 1 "GND" H 2505 4877 50  0000 C CNN
F 2 "" H 2500 5050 50  0001 C CNN
F 3 "" H 2500 5050 50  0001 C CNN
	1    2500 5050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2500 4700 2500 4500
Wire Wire Line
	2500 4500 3000 4500
Wire Wire Line
	2500 5000 2500 5050
$Comp
L Device:C C3
U 1 1 6354C43D
P 5700 5150
F 0 "C3" H 5815 5196 50  0000 L CNN
F 1 "FREECHOICE" H 5815 5105 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric_Pad1.15x1.40mm_HandSolder" H 5738 5000 50  0001 C CNN
F 3 "~" H 5700 5150 50  0001 C CNN
	1    5700 5150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0117
U 1 1 6354C4EA
P 5700 5300
F 0 "#PWR0117" H 5700 5050 50  0001 C CNN
F 1 "GND" H 5705 5127 50  0000 C CNN
F 2 "" H 5700 5300 50  0001 C CNN
F 3 "" H 5700 5300 50  0001 C CNN
	1    5700 5300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5700 5000 5700 4950
Connection ~ 5700 4950
Wire Wire Line
	5700 4950 5900 4950
$Comp
L SamacSys_Parts:USB2066-05-RBHM-15-STB-00-00-A J1
U 1 1 6362FF8C
P 8550 4750
F 0 "J1" H 9000 5015 50  0000 C CNN
F 1 "USB2066-05-RBHM-15-STB-00-00-A" H 9000 4924 50  0000 C CNN
F 2 "SamacSys_Parts:USB206605RBHM15STB0000A" H 9300 4850 50  0001 L CNN
F 3 "" H 9300 4750 50  0001 L CNN
F 4 "GCT (GLOBAL CONNECTOR TECHNOLOGY) - USB2066-05-RBHM-15-STB-00-00-A - USB Connector, Mini USB Type B, USB 2.0, Receptacle, 5 Positions, Surface Mount, Right Angle" H 9300 4650 50  0001 L CNN "Description"
F 5 "4.25" H 9300 4550 50  0001 L CNN "Height"
F 6 "640-2665RBHM15STB00A" H 9300 4450 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/GCT/USB2066-05-RBHM-15-STB-00-00-A?qs=KUoIvG%2F9IlZEo87a0wQR%252BA%3D%3D" H 9300 4350 50  0001 L CNN "Mouser Price/Stock"
F 8 "GCT (GLOBAL CONNECTOR TECHNOLOGY)" H 9300 4250 50  0001 L CNN "Manufacturer_Name"
F 9 "USB2066-05-RBHM-15-STB-00-00-A" H 9300 4150 50  0001 L CNN "Manufacturer_Part_Number"
	1    8550 4750
	1    0    0    -1  
$EndComp
Text Label 9500 5200 3    50   ~ 0
SHIELD
Wire Wire Line
	9450 4750 9500 4750
Wire Wire Line
	9500 4750 9500 4850
Wire Wire Line
	9500 5050 9450 5050
Wire Wire Line
	9450 4950 9500 4950
Connection ~ 9500 4950
Wire Wire Line
	9500 4950 9500 5050
Wire Wire Line
	9450 4850 9500 4850
Connection ~ 9500 4850
Wire Wire Line
	9500 4850 9500 4950
Wire Wire Line
	9500 5050 9500 5200
Connection ~ 9500 5050
Wire Wire Line
	7800 4500 8100 4500
Wire Wire Line
	8100 4500 8100 4750
Wire Wire Line
	8100 4750 8550 4750
Connection ~ 7800 4500
Wire Wire Line
	7800 4800 8000 4800
Connection ~ 7800 4800
Wire Wire Line
	8000 4800 8000 4850
Wire Wire Line
	8000 4850 8550 4850
$Comp
L Device:R R10
U 1 1 6364A079
P 7800 5150
F 0 "R10" H 7870 5196 50  0000 L CNN
F 1 "120" H 7870 5105 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 7730 5150 50  0001 C CNN
F 3 "~" H 7800 5150 50  0001 C CNN
	1    7800 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	8550 4950 8000 4950
Wire Wire Line
	8000 4950 8000 5000
Wire Wire Line
	8000 5000 7800 5000
Wire Wire Line
	8550 5050 8100 5050
Wire Wire Line
	8100 5050 8100 5300
Wire Wire Line
	8100 5300 7800 5300
Text Label 7550 5100 2    50   ~ 0
#ENABLE
Text Label 7550 5200 2    50   ~ 0
ENABLE
Wire Wire Line
	7800 5000 7650 5000
Wire Wire Line
	7650 5000 7650 5100
Wire Wire Line
	7650 5100 7550 5100
Connection ~ 7800 5000
Wire Wire Line
	7800 5300 7650 5300
Wire Wire Line
	7650 5300 7650 5200
Wire Wire Line
	7650 5200 7550 5200
Connection ~ 7800 5300
Wire Wire Line
	6300 4700 6250 4700
Wire Wire Line
	6250 4700 6250 4650
Text Label 6200 4650 2    50   ~ 0
#ENABLE
Wire Wire Line
	6200 4650 6250 4650
Connection ~ 6250 4650
Wire Wire Line
	6250 4650 6250 4600
$Comp
L power:GND #PWR0107
U 1 1 63660643
P 8250 5550
F 0 "#PWR0107" H 8250 5300 50  0001 C CNN
F 1 "GND" H 8255 5377 50  0000 C CNN
F 2 "" H 8250 5550 50  0001 C CNN
F 3 "" H 8250 5550 50  0001 C CNN
	1    8250 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	8450 5150 8450 5200
$Comp
L power:GND #PWR0111
U 1 1 6369D88F
P 8900 2550
F 0 "#PWR0111" H 8900 2300 50  0001 C CNN
F 1 "GND" V 8905 2422 50  0000 R CNN
F 2 "" H 8900 2550 50  0001 C CNN
F 3 "" H 8900 2550 50  0001 C CNN
	1    8900 2550
	0    -1   -1   0   
$EndComp
$Comp
L SamacSys_Parts:STX-3000 J0
U 1 1 636A0688
P 6400 3850
F 0 "J0" H 6800 4115 50  0000 C CNN
F 1 "STX-3000" H 6800 4024 50  0000 C CNN
F 2 "SamacSys_Parts:STX3000" H 7050 3950 50  0001 L CNN
F 3 "http://www.kycon.com/Pub_Eng_Draw/STX-3000.pdf" H 7050 3850 50  0001 L CNN
F 4 "Phone Connectors 3.5mm PCB STEREO BLK PLASTIC NON THREADED" H 7050 3750 50  0001 L CNN "Description"
F 5 "5.4" H 7050 3650 50  0001 L CNN "Height"
F 6 "806-STX-3000" H 7050 3550 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Kycon/STX-3000?qs=kjZ2mQLP346Nbz1X9BOzfg%3D%3D" H 7050 3450 50  0001 L CNN "Mouser Price/Stock"
F 8 "Kycon" H 7050 3350 50  0001 L CNN "Manufacturer_Name"
F 9 "STX-3000" H 7050 3250 50  0001 L CNN "Manufacturer_Part_Number"
	1    6400 3850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0118
U 1 1 636A60DE
P 8050 3850
F 0 "#PWR0118" H 8050 3600 50  0001 C CNN
F 1 "GND" V 8055 3722 50  0000 R CNN
F 2 "" H 8050 3850 50  0001 C CNN
F 3 "" H 8050 3850 50  0001 C CNN
	1    8050 3850
	0    -1   -1   0   
$EndComp
Text Label 7200 3950 0    50   ~ 0
SHIELD
$Comp
L SamacSys_Parts:SBRT3U60SAF-13 D0
U 1 1 6362A8A1
P 7350 3850
F 0 "D0" H 7650 4117 50  0000 C CNN
F 1 "SBRT3U60SAF-13" H 7650 4026 50  0000 C CNN
F 2 "SamacSys_Parts:SODFL5226X110N" H 7800 3850 50  0001 L CNN
F 3 "https://4donline.ihs.com/images/VipMasterIC/IC/DIOD/DIOD-S-A0002833665/DIOD-S-A0002833531-1.pdf?hkey=EF798316E3902B6ED9A73243A3159BB0" H 7800 3750 50  0001 L CNN
F 4 "Rectifier Diode Super Barrier Rectifier 60V 3A 2-Pin SMAF T/R" H 7800 3650 50  0001 L CNN "Description"
F 5 "1.1" H 7800 3550 50  0001 L CNN "Height"
F 6 "621-SBRT3U60SAF-13" H 7800 3450 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Diodes-Incorporated/SBRT3U60SAF-13?qs=rN85NNvew%2FTN5dk%252B1NkkKw%3D%3D" H 7800 3350 50  0001 L CNN "Mouser Price/Stock"
F 8 "Diodes Inc." H 7800 3250 50  0001 L CNN "Manufacturer_Name"
F 9 "SBRT3U60SAF-13" H 7800 3150 50  0001 L CNN "Manufacturer_Part_Number"
	1    7350 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	7200 3850 7350 3850
$Comp
L SamacSys_Parts:2-1445057-3 J2
U 1 1 63647502
P 4450 2900
F 0 "J2" H 4900 3165 50  0000 C CNN
F 1 "2-1445057-3" H 4900 3074 50  0000 C CNN
F 2 "SamacSys_Parts:214450573" H 5200 3000 50  0001 L CNN
F 3 "https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocNm=1773458-4_MICRO_MATE_N_LOK&DocType=Data+Sheet&DocLang=English&PartCntxt=2-1445057-3&DocFormat=pdf" H 5200 2900 50  0001 L CNN
F 4 "Connector Header Surface Mount, Right Angle 3 position 0.118\" (3.00mm)" H 5200 2800 50  0001 L CNN "Description"
F 5 "5.67" H 5200 2700 50  0001 L CNN "Height"
F 6 "571-2-1445057-3" H 5200 2600 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/TE-Connectivity-AMP/2-1445057-3?qs=RfHrfbgRAL0JwvXbugDVow%3D%3D" H 5200 2500 50  0001 L CNN "Mouser Price/Stock"
F 8 "TE Connectivity" H 5200 2400 50  0001 L CNN "Manufacturer_Name"
F 9 "2-1445057-3" H 5200 2300 50  0001 L CNN "Manufacturer_Part_Number"
	1    4450 2900
	1    0    0    -1  
$EndComp
NoConn ~ 4450 2900
NoConn ~ 4450 3000
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 636869DE
P 8000 3900
F 0 "#FLG0101" H 8000 3975 50  0001 C CNN
F 1 "PWR_FLAG" H 8000 4073 50  0000 C CNN
F 2 "" H 8000 3900 50  0001 C CNN
F 3 "~" H 8000 3900 50  0001 C CNN
	1    8000 3900
	-1   0    0    1   
$EndComp
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 6368C3C7
P 6250 1900
F 0 "#FLG0102" H 6250 1975 50  0001 C CNN
F 1 "PWR_FLAG" H 6250 2073 50  0000 C CNN
F 2 "" H 6250 1900 50  0001 C CNN
F 3 "~" H 6250 1900 50  0001 C CNN
	1    6250 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7950 3850 8000 3850
Wire Wire Line
	8000 3850 8000 3900
Wire Wire Line
	8050 3850 8000 3850
Connection ~ 8000 3850
Wire Wire Line
	6150 2050 6250 2050
Wire Wire Line
	6250 1900 6250 2050
Connection ~ 6250 2050
Wire Wire Line
	6250 2050 6350 2050
$Comp
L Device:R FC0
U 1 1 6363FCD4
P 8250 5350
F 0 "FC0" H 8250 5200 50  0000 L CNN
F 1 "R" H 8320 5305 50  0001 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 8180 5350 50  0001 C CNN
F 3 "~" H 8250 5350 50  0001 C CNN
	1    8250 5350
	1    0    0    -1  
$EndComp
$Comp
L Device:R FC1
U 1 1 636405A4
P 8450 5350
F 0 "FC1" H 8450 5200 50  0000 L CNN
F 1 "R" H 8520 5305 50  0001 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 8380 5350 50  0001 C CNN
F 3 "~" H 8450 5350 50  0001 C CNN
	1    8450 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	8250 5200 8250 5150
Wire Wire Line
	8250 5150 8450 5150
Wire Wire Line
	8250 5500 8250 5550
Text Label 8450 5700 0    50   ~ 0
SHIELD
Wire Wire Line
	8450 5700 8450 5500
Connection ~ 8450 5150
Wire Wire Line
	8450 5150 8550 5150
$Comp
L Connector:TestPoint TP1
U 1 1 63652AED
P 8700 1700
F 0 "TP1" V 8700 1900 50  0000 L CNN
F 1 "TestPoint" V 8745 1888 50  0001 L CNN
F 2 "TestPoint:TestPoint_THTPad_D2.5mm_Drill1.2mm" H 8900 1700 50  0001 C CNN
F 3 "~" H 8900 1700 50  0001 C CNN
	1    8700 1700
	0    1    1    0   
$EndComp
$Comp
L Connector:TestPoint TP2
U 1 1 63653058
P 8700 1800
F 0 "TP2" V 8700 2000 50  0000 L CNN
F 1 "TestPoint" V 8745 1988 50  0001 L CNN
F 2 "TestPoint:TestPoint_THTPad_D2.5mm_Drill1.2mm" H 8900 1800 50  0001 C CNN
F 3 "~" H 8900 1800 50  0001 C CNN
	1    8700 1800
	0    1    1    0   
$EndComp
$Comp
L Connector:TestPoint TP3
U 1 1 63653322
P 8700 1900
F 0 "TP3" V 8700 2100 50  0000 L CNN
F 1 "TestPoint" V 8745 2088 50  0001 L CNN
F 2 "TestPoint:TestPoint_THTPad_2.5x2.5mm_Drill1.2mm" H 8900 1900 50  0001 C CNN
F 3 "~" H 8900 1900 50  0001 C CNN
	1    8700 1900
	0    1    1    0   
$EndComp
Text Label 8700 1600 2    50   ~ 0
POWER
Text Label 8700 1700 2    50   ~ 0
5V
Text Label 8700 1800 2    50   ~ 0
3.3V
$Comp
L power:GND #PWR0119
U 1 1 63654653
P 8700 1900
F 0 "#PWR0119" H 8700 1650 50  0001 C CNN
F 1 "GND" V 8705 1772 50  0000 R CNN
F 2 "" H 8700 1900 50  0001 C CNN
F 3 "" H 8700 1900 50  0001 C CNN
	1    8700 1900
	0    1    1    0   
$EndComp
$Comp
L Connector:TestPoint TP0
U 1 1 63650CC3
P 8700 1600
F 0 "TP0" V 8700 1800 50  0000 L CNN
F 1 "TestPoint" V 8450 1500 50  0000 L CNN
F 2 "TestPoint:TestPoint_THTPad_D2.5mm_Drill1.2mm" H 8900 1600 50  0001 C CNN
F 3 "~" H 8900 1600 50  0001 C CNN
	1    8700 1600
	0    1    1    0   
$EndComp
$Comp
L Connector:TestPoint TX0
U 1 1 6365A60D
P 6300 4800
F 0 "TX0" H 6300 5000 50  0000 R CNN
F 1 "TestPoint" H 6242 4917 50  0001 R CNN
F 2 "TestPoint:TestPoint_THTPad_D2.5mm_Drill1.2mm" H 6500 4800 50  0001 C CNN
F 3 "~" H 6500 4800 50  0001 C CNN
	1    6300 4800
	-1   0    0    1   
$EndComp
Connection ~ 6300 4800
$Comp
L Connector:TestPoint RX0
U 1 1 6365B08C
P 6300 4500
F 0 "RX0" H 6200 4700 50  0000 L CNN
F 1 "TestPoint" H 6358 4527 50  0001 L CNN
F 2 "TestPoint:TestPoint_THTPad_D2.5mm_Drill1.2mm" H 6500 4500 50  0001 C CNN
F 3 "~" H 6500 4500 50  0001 C CNN
	1    6300 4500
	1    0    0    -1  
$EndComp
Connection ~ 6300 4500
Wire Wire Line
	6950 2550 7050 2550
Wire Wire Line
	6150 2550 6550 2550
$Comp
L SamacSys_Parts:SK34A D1
U 1 1 6367DBF9
P 7050 2550
F 0 "D1" V 7304 2680 50  0000 L CNN
F 1 "SK34A" V 7395 2680 50  0000 L CNN
F 2 "SamacSys_Parts:DIOM5126X230N" H 7500 2550 50  0001 L CNN
F 3 "https://componentsearchengine.com/Datasheets/2/SK34A.pdf" H 7500 2450 50  0001 L CNN
F 4 "TAIWAN SEMICONDUCTOR - SK34A - DIODE, SCHOTTKY, 3A, 40V, SMA" H 7500 2350 50  0001 L CNN "Description"
F 5 "2.3" H 7500 2250 50  0001 L CNN "Height"
F 6 "821-SK34A" H 7500 2150 50  0001 L CNN "Mouser Part Number"
F 7 "https://www.mouser.co.uk/ProductDetail/Taiwan-Semiconductor/SK34A?qs=tHU%2FlV7kTyTipVMF4LfRPw%3D%3D" H 7500 2050 50  0001 L CNN "Mouser Price/Stock"
F 8 "Taiwan Semiconductor" H 7500 1950 50  0001 L CNN "Manufacturer_Name"
F 9 "SK34A" H 7500 1850 50  0001 L CNN "Manufacturer_Part_Number"
	1    7050 2550
	0    1    1    0   
$EndComp
Connection ~ 7050 2550
Wire Wire Line
	7050 2550 7500 2550
Wire Wire Line
	6050 3150 6550 3150
Wire Wire Line
	6050 2150 6050 2700
Wire Wire Line
	6050 3000 6050 3150
Wire Wire Line
	6550 3000 6550 3150
Connection ~ 6550 3150
Wire Wire Line
	6550 3150 7050 3150
Wire Wire Line
	6550 2700 6550 2550
Connection ~ 6550 2550
Wire Wire Line
	6550 2550 6650 2550
Wire Wire Line
	7500 2650 7500 3150
Wire Wire Line
	7050 3150 7050 3200
$EndSCHEMATC
