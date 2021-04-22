EESchema Schematic File Version 4
EELAYER 30 0
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
L Connector_Generic:Conn_02x20_Odd_Even J2
U 1 1 60A2F8F0
P 4950 3850
F 0 "J2" H 5000 4967 50  0000 C CNN
F 1 "Conn_02x20_Odd_Even" H 5000 4876 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H 4950 3850 50  0001 C CNN
F 3 "~" H 4950 3850 50  0001 C CNN
	1    4950 3850
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x08 J1
U 1 1 60A30749
P 3700 4050
F 0 "J1" H 3618 4567 50  0000 C CNN
F 1 "Conn_01x08" H 3618 4476 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" H 3700 4050 50  0001 C CNN
F 3 "~" H 3700 4050 50  0001 C CNN
	1    3700 4050
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3900 3750 4050 3750
Wire Wire Line
	4050 3750 4050 3450
Wire Wire Line
	4050 3450 4750 3450
Wire Wire Line
	3900 3850 4100 3850
Wire Wire Line
	4100 3850 4100 3550
Wire Wire Line
	4100 3550 4750 3550
Wire Wire Line
	3900 3950 4150 3950
Wire Wire Line
	4150 3950 4150 3650
Wire Wire Line
	4150 3650 4750 3650
Wire Wire Line
	3900 4050 4750 4050
Wire Wire Line
	3900 4150 4200 4150
Wire Wire Line
	4200 4150 4200 3850
Wire Wire Line
	4200 3850 4750 3850
Wire Wire Line
	3900 4450 4300 4450
Wire Wire Line
	4300 4450 4300 3750
Wire Wire Line
	4300 3750 4750 3750
Wire Wire Line
	3900 4350 4400 4350
Wire Wire Line
	4400 4350 4400 4150
Wire Wire Line
	4400 4150 4750 4150
Text Label 4450 3450 0    50   ~ 0
RES
Text Label 4450 3550 0    50   ~ 0
DC
Text Label 4450 3650 0    50   ~ 0
CS
Text Label 4450 3750 0    50   ~ 0
VCC
Text Label 4450 3850 0    50   ~ 0
DIN
Text Label 4450 4050 0    50   ~ 0
CLK
Text Label 4450 4150 0    50   ~ 0
GND
$EndSCHEMATC
