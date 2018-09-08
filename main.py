import time
import serial
import csv
from smbus import SMBus
import lib_MPL3115A2

serialport = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

deg = u'\N{DEGREE SIGN}'

counter = 0

#import main_datalogger

csv_filename = 'Data: '+time.strftime('%mm%dd%yy_%Hh%Mm%Ss')+'.csv'
dataFile = open(csv_filename,'w')
dataFile.write('Time,Pressure (kPa),Temperature ('+deg.encode("utf8")+'C),Temperature ('+deg.encode("utf8")+'F),Altitude (m),'+'\n')
dataFile.close()

while True:
    counter += 1
    #serialdata = serial.readline()
    #serialdatasliced = serialdata[ : 1]
    #if (serialdata == "X"):
    #    serialport.write("Command Mode")
    #    time.sleep(1)
    #    slicemore = serialdata [1 : ]
    #    if (slicemore == "hello"):
    #        serialport.write("I wuv u")
    #    else if (slicemore == "i hate u"):
    #        serialport.write("but i wuv u")
    #    else:
    #        serialport.write("ok sir")
    #        time.sleep(1)
    #else:
    MPL3115A2_Data = lib_MPL3115A2.Get_Data()
    print str(MPL3115A2_Data[0])
    print str(MPL3115A2_Data[1])
    print str(MPL3115A2_Data[2])
    print str(MPL3115A2_Data[3])
    datapacket = "#: %d, kPa: %.2f, C: %.1f, F: %.1f, m: %d" % (counter, MPL3115A2_Data[0], MPL3115A2_Data[1], MPL3115A2_Data[2], MPL3115A2_Data[3])
    serialport.write(datapacket)
    time.sleep(2)
    with open(csv_filename, 'a') as csvFile:
     dataLogger = csv.writer(csvFile, delimiter=',', lineterminator='\n')
     dataLogger.writerow([time.strftime('%m/%d/%Y %H:%M:%S%z'),
                        str(MPL3115A2_Data[0]),
                        str(MPL3115A2_Data[1]),
                        str(MPL3115A2_Data[2]),
                        str(MPL3115A2_Data[3])])
