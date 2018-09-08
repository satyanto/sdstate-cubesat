import time
import csv
import lib_MPL3115A2
from smbus import SMBus

deg = u'\N{DEGREE SIGN}'

csv_filename = 'Data: '+time.strftime('%mm%dd%yy_%Hh%Mm%Ss')+'.csv'
dataFile = open(csv_filename,'w')
dataFile.write('Time,Pressure (kPa),Temperature ('+deg.encode("utf8")+'C),Temperature ('+deg.encode("utf8")+'F),Altitude (m),'+'\n')
dataFile.close()

while True:
    MPL3115A2_Data = lib_MPL3115A2.Get_Data()
    with open(csv_filename, 'a') as csvFile:
         dataLogger = csv.writer(csvFile, delimiter=',', lineterminator='\n')
         dataLogger.writerow([time.strftime('%m/%d/%Y %H:%M:%S%z'),
                            str(MPL3115A2_Data[0]),
                            str(MPL3115A2_Data[1]),
                            str(MPL3115A2_Data[2]),
                            str(MPL3115A2_Data[3])])
    time.sleep(2)
