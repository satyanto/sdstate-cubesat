# sdstate-cubesat

## New Raspberry Pi Set-Up

```
sudo apt-get update
```
Enable interfaces
```
sudo raspi-config
```
Enable Interface options VNC, I2C, SPI, Serial, etc.

(Optional) Install Remote Desktop
```
apt-get install xrdp
```

## Feather M0 Arduino IDE & Transmit/Receive Setup:
Download the Arduino IDE, go to preferences and add the URL below for Additional Boards Manager (click on the small icon on the side):

__https://adafruit.github.io/arduino-board-index/package_adafruit_index.json__

Click OK.

Now, go to the 'Tools' tab, mouse over 'Board:' and go to 'Boards Manager...' and install the following:

* "Arduino SAMD Boards"

* "Arduino SAMD Beta Boards"

* "Adafruit SAMD Boards"

Restart the Arduino IDE.

Now connect the Adafruit Feather M0 with USB and go to the 'Tools' tab, go to 'Board:' and pick 'Adafruit Feather M0'.

And that's it!

## GPS Set-Up (Using Adafruit Ultimate GPS Breakout Board)
|GPS      |Raspberry Pi  |
|---------|--------------|
|Vin      | 3.3V         |
|GND      | GND          |
|RX       | UART  TX     |
|TX       | UART  RX     |

1. Set up minicom, so we can test out the UART ports.
```
sudo apt-get install minicom
```
2. Edit the /boot/cmdline.txt file, so that it looks like this:
(We are simply deleting references to ttyAMA0)
Here is what looks like on the current Raspberry Pi (may differ):
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p7 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait splash plymouth.ignore-serial-consoles
```
(single line)

3. We can now test out what sort of data we are receiving from the UART serial port, but we first need to change the settings for the minicom:
```
sudo minicom -s
```
Go to serial port, change serial device to:    /dev/ttyS0
Go to Bps/Par/Bits, change baudrate to:   9600







## MPL3115A2 Sensor Set-Up

|Sensor   |Raspberry Pi  |
|---------|--------------|
|Vin      | 3.3V         |
|GND      | GND          |
|SCL      | i2c SCL      |
|SDA      | i2c SDA      |

First we gotta set-up the Raspberry Pi:
```
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
```
Set up modules:
```
sudo nano /etc/modules

i2c-bcm2708
i2c-dev
```
Remove blacklists:
```
sudo nano /etc/modprobe.d/raspi-blacklist.conf

#blacklist spi-bcm2708
#blacklist i2c-bcm2708
```
The MPL3115A2 requires a repeated start command in it's I2C communication - the Raspberry Pi doesn't do this out of the box, but we can use a kernel module.
```
sudo su -
echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined
exit
```


Additional Reading:
- http://www.hobbytronics.co.uk/raspberry-pi-serial-port
- http://n5dux.com/ham/raspberrypi/igate.php
- http://www.rowetel.com/?p=5344
- https://github.com/antonjan/Raspberry_Telemetry
- https://hackaday.com/2018/05/02/raspberry-pi-is-up-up-and-away/#more-306026
- https://create.arduino.cc/projecthub/jweers1/arduino-aprs-tracker-wilderness-location-tracking-a50607
- https://www.sparkfun.com/news/389
- https://www.sparkfun.com/tutorials/185
- https://n1aae.com/raspberry-pi-aprs-direwolf-linux-igate-digipeater/

