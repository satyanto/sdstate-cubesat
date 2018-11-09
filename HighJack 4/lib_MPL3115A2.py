#   Hafidh Satyanto
#   Library for MPL3115A2 sensor

#   Connect Vin to 3V
#   GND to GND
#   SCL to i2c SCL
#   SDA to i2c SDA

import time
import board
import busio
import adafruit_mpl3115a2

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)

sensor.sealevel_pressure = 102250

def Get_Data():
    try:
        pressure = sensor.pressure          #pascals
        altitude = sensor.altitude          #meters
        temperature = sensor.temperature    #celsius

        return pressure,temperature,altitude
    except IOError:
        print('MPL3115A2 Connection Error')
        return 0,0,0

if __name__ == "__main__":
    Get_Data()
