EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr User 19031 12568
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
Text Label 10900 2000 2    50   ~ 0
~RESET
Text Label 12700 5000 0    50   ~ 0
G5
Text Label 12700 5100 0    50   ~ 0
G6
Text Label 12700 3100 0    50   ~ 0
A0
Text Label 12700 3200 0    50   ~ 0
A1
Text Label 10900 5100 2    50   ~ 0
BATT_VIN
Text Label 12700 3600 0    50   ~ 0
D1-CAM_TRIG
Text Label 10900 4500 2    50   ~ 0
I2C_SCL
Text Label 10900 4600 2    50   ~ 0
I2C_SDA
Text Label 12700 2900 0    50   ~ 0
~SPI_CS
Text Label 10900 2700 2    50   ~ 0
USB_D-
Text Label 10900 2800 2    50   ~ 0
USB_D+
Text Label 10900 2100 2    50   ~ 0
~BOOT
Text Label 10900 4100 2    50   ~ 0
AUD_IN-CAM_PCLK
Text Label 12700 3900 0    50   ~ 0
UART_RX1
Text Label 12700 4900 0    50   ~ 0
G4
Text Label 10900 4000 2    50   ~ 0
AUD_OUT-CAM_MCLK
Text Label 12700 3800 0    50   ~ 0
UART_TX1
Text Label 12700 4800 0    50   ~ 0
G3
Text Label 10900 4200 2    50   ~ 0
AUD_LRCLK
Text Label 10900 4800 2    50   ~ 0
I2C_SCL1
Text Label 12700 4600 0    50   ~ 0
G1
Text Label 10900 4300 2    50   ~ 0
AUD_BCLK
Text Label 10900 4900 2    50   ~ 0
I2C_SDA1
Text Label 12700 4700 0    50   ~ 0
G2
Text Label 10900 4700 2    50   ~ 0
I2C_~INT
Text Label 12700 3300 0    50   ~ 0
PWM0
Text Label 12700 3400 0    50   ~ 0
PWM1
Text Label 12700 3500 0    50   ~ 0
D0
Text Label 12700 4500 0    50   ~ 0
G0
$Comp
L MicroMod_Processor_Board_(2):MICROMOD-2222 J1
U 1 1 449C7C68
P 11800 3900
F 0 "J1" H 11000 6020 59  0000 L BNN
F 1 "MICROMOD-2222" H 11000 2000 59  0000 L BNN
F 2 "SparkFun_MicroMod_ESP32:M.2-CARD-E-22" H 11800 3900 50  0001 C CNN
F 3 "" H 11800 3900 50  0001 C CNN
	1    11800 3900
	1    0    0    -1  
$EndComp
$Comp
L MicroMod_Processor_Board_(2):OSHW-LOGOS LOGO3
U 1 1 03FD88E0
P 13550 11400
F 0 "LOGO3" H 13550 11400 50  0001 C CNN
F 1 "OSHW-LOGOS" H 13550 11400 50  0001 C CNN
F 2 "SparkFun_MicroMod_ESP32:OSHW-LOGO-S" H 13550 11400 50  0001 C CNN
F 3 "" H 13550 11400 50  0001 C CNN
	1    13550 11400
	1    0    0    -1  
$EndComp
Text Notes 9000 900  0    100  ~ 0
MicroMod Connector
Text Label 10900 3600 2    50   ~ 0
SWDIO
Text Label 10900 3700 2    50   ~ 0
SWDCK
Text Label 10900 2300 2    50   ~ 0
3.3V_EN
Text Label 10900 2400 2    50   ~ 0
RTC_3V_BATT
Text Label 10900 3000 2    50   ~ 0
USBHOST_D-
Text Label 10900 3100 2    50   ~ 0
USBHOST_D+
Text Label 10900 3300 2    50   ~ 0
CAN-TX
Text Label 10900 3400 2    50   ~ 0
CAN-RX
Text Label 10900 3900 2    50   ~ 0
AUD_MCLK
Text Label 12700 1900 0    50   ~ 0
SDIO_SCK-SPI_SCK1
Text Label 12700 2000 0    50   ~ 0
SDIO_CMD-SPI_COPI1
Text Label 12700 2100 0    50   ~ 0
SDIO_DATA0-SPI_CIPO1
Text Label 12700 2200 0    50   ~ 0
SDIO_DATA1
Text Label 12700 2300 0    50   ~ 0
SDIO_DATA2
Text Label 12700 2400 0    50   ~ 0
SDIO_DATA3-~SPI_CS1
Text Label 12700 2600 0    50   ~ 0
SPI_SCK
Text Label 12700 2700 0    50   ~ 0
SPI_COPI-LED_DAT
Text Label 12700 2800 0    50   ~ 0
SPI_CIPO-LED_CLK
Text Label 12700 4000 0    50   ~ 0
UART_RTS1
Text Label 12700 4100 0    50   ~ 0
UART_CTS1
Text Label 12700 4200 0    50   ~ 0
UART_TX2
Text Label 12700 4300 0    50   ~ 0
UART_RX2
Text Label 12700 5200 0    50   ~ 0
G7
Text Label 12700 5300 0    50   ~ 0
G8
Text Label 12700 5400 0    50   ~ 0
G9-CAM_HSYNC
Text Label 12700 5500 0    50   ~ 0
G10-CAM_VSYNC
Text Label 12700 5600 0    50   ~ 0
G11-SWO
$Comp
L power:+3.3V #PWR?
U 1 1 5F943365
P 10900 1900
F 0 "#PWR?" H 10900 1750 50  0001 C CNN
F 1 "+3.3V" V 10915 2028 50  0000 L CNN
F 2 "" H 10900 1900 50  0001 C CNN
F 3 "" H 10900 1900 50  0001 C CNN
	1    10900 1900
	0    -1   -1   0   
$EndComp
Text Label 10900 2600 2    50   ~ 0
V_USB
$Comp
L power:GND #PWR?
U 1 1 5F944AFD
P 10900 5600
F 0 "#PWR?" H 10900 5350 50  0001 C CNN
F 1 "GND" V 10905 5472 50  0000 R CNN
F 2 "" H 10900 5600 50  0001 C CNN
F 3 "" H 10900 5600 50  0001 C CNN
	1    10900 5600
	0    1    1    0   
$EndComp
$EndSCHEMATC
