#   Hafidh Satyanto
#   Library for MPL3115A2 sensor

from smbus import SMBus
import time
import csv

def Get_Data():
    bus = smbus.SMBus(1)
    bus.write_byte_data(0x60, 0x26, 0xB9)
    bus.write_byte_data(0x60, 0x13, 0x07)
    bus.write_byte_data(0x60, 0x26, 0xB9)
    time.sleep(1)
    data = bus.read_i2c_block_data(0x60, 0x00, 6)
    altitude = (((data[1]*65536)+(data[2]*256)+(data[3]&0xF0))/16)/16
    temp = ((data[4]*256)+(data[5]&0xF0))/16
    ctemp = temp/16
    ftemp = ctemp*1.8+32
    bus.write_byte_data(0x60, 0x26, 0x39)
    time.sleep(1)
    data=bus.read_i2c_block_data(0x60, 0x00, 4)
    press=((data[1]*65536)+(data[2]*256)+(data[3]&0xF0))/16
    pressure=(pres/4)/1000 #given in kPa

    return pressure,ctemp,ftemp,altitude

if __name__ == "__main__":
    Get_Data()
