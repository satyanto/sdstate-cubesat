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

