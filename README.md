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
Install GPSD:
```
sudo apt-get install gpsd gpsd-clients python-gps
```
Since we're using Raspbian Stretch (later version than Jessie), we have disable a systemd service:
```
sudo systemct1 stop gpsd.socket
sudo systemct1 disable gpsd.socket
```
To start gpsd using UART:
```
sudo killall gpsd
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
```
To test the output:
```
cgps -s
```

## MPL3115A2 Sensor Set-Up

|Sensor   |Raspberry Pi  |
|---------|--------------|
|Vin      | 3V           |
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
- http://n5dux.com/ham/raspberrypi/igate.php
- http://www.rowetel.com/?p=5344
- https://github.com/antonjan/Raspberry_Telemetry
- https://hackaday.com/2018/05/02/raspberry-pi-is-up-up-and-away/#more-306026
- https://create.arduino.cc/projecthub/jweers1/arduino-aprs-tracker-wilderness-location-tracking-a50607
- https://www.sparkfun.com/news/389
- https://www.sparkfun.com/tutorials/185
- https://n1aae.com/raspberry-pi-aprs-direwolf-linux-igate-digipeater/

