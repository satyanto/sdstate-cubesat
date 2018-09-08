import time
import serial
import csv
from smbus import SMBus
import lib_

serialport = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

counter = 0

import main_datalogger

while True:
    counter += 1
    MPL3115A2_Data = lib_MPL3115A2.Get_Data()
    with open(csv_filename, 'a') as csvFile:
         dataLogger = csv.writer(csvFile, delimiter=',', lineterminator='\n')
         dataLogger.writerow([time.strftime('%m/%d/%Y %H:%M:%S%z'),
                            str(MPL3115A2_Data[0]),
                            str(MPL3115A2_Data[1]),
                            str(MPL3115A2_Data[2]),
                            str(MPL3115A2_Data[3])])
    datapacket = "%f %.2f %.1f %.1f %.1f" % (counter, MPL3115A2_Data[0], MPL3115A2_Data[1], MPL3115A2_Data[2], MPL3115A2_Data[3])
    serialport.write(datapacket)
    time.sleep(2)
    serialport.close()
