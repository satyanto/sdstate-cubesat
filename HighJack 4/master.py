from smbus import SMBus
import time
import csv
import serial

LIS3DH = False
MPL3115A2 = False
GPS = False

deg = u'\N{DEGREE SIGN}'

try:    ## Import LIS3DH Accelerometer
    import lib_LIS3DH
except ImportError:
    print('Error importing LIS3DH Sensor')
else:
    LIS3DH = True

try:    ## Import MPL3115A2 Barometeric Altimeter
    import lib_MPL3115A2
except ImportError:
    print('Error importing MPL3115A2 Sensor')
else:
    MPL3115A2 = True

try:    ## Import GPS
    import lib_GPS
except ImportError:
    print('Error importing GPS Sensor')
else:
    GPS = True

datarows = [
    'Time',                                                 #0
    'Pressure (kPa)',                                       #1
    'Temperature ('+deg.encode("utf8")+'C)',                #2
    'Temperature ('+deg.encode("utf8")+'F)',                #3
    'Altitude Estimation (m)',                              #4
    'Acceleration (X)',                                     #5
    'Acceleration (Y)',                                     #6
    'Acceleration (Z)',                                     #7
    'Fix Timestamp',                                        #8
    'Fix Quality',                                          #9
    'Latitude ('+deg.encode("utf8")+')',                    #10
    'Longitude ('+deg.encode("utf8")+')',                   #11
    '# Satellites',                                         #12
    'Altitude GPS (m)',                                     #13
    'Speed (knots)',                                        #14
    'Track Angle ('+deg.encode("utf8")+')',                 #15
    'Horizontal Dilution',                                  #16
]

if (LIS3DH==False):
    datarows[5] = 'LIS3DH N/A',
    datarows[6] = 'LIS3DH N/A',
    datarows[7] = 'LIS3DH N/A',

if (MPL3115A2==False):
    datarows[1] = 'MPL3115A2 N/A',
    datarows[2] = 'MPL3115A2 N/A',
    datarows[3] = 'MPL3115A2 N/A',
    datarows[4] = 'MPL3115A2 N/A',

if (GPS==False):
    datarows[8] = 'GPS N/A',
    datarows[9] = 'GPS N/A',
    datarows[10] = 'GPS N/A',
    datarows[11] = 'GPS N/A',
    datarows[12] = 'GPS N/A',
    datarows[13] = 'GPS N/A',
    datarows[14] = 'GPS N/A',
    datarows[15] = 'GPS N/A',
    datarows[16] = 'GPS N/A',

csv_filename = 'Data: '+time.strftime('%mm%dd%yy_%Hh%Mm%Ss')+'.csv'
with open(csv_filename, 'w') as dataInit:
    dataInit = csv.writer(dataInit, delimiter=',', lineterminator='\n')
    dataInit.writerow(datarows)

while True:
    if (MPL3115A2==True):
        MPL3115A2_Data = lib_MPL3115A2.Get_Data()
    else:
        MPL3115A2_Data = [0, 0, 0, 0]

    if (LIS3DH==True):
        LIS3DH_Data = lib_LIS3DH.Get_Data()
    else:
        LIS3DH_Data = [0, 0, 0]
        if (not lib_LIS3DH.Get_Data()):
            print('LIS3DH Data Error')

    if (GPS==True):
        GPS_Data = lib_GPS.Get_Data()
    else:
        GPS_Data = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    with open(csv_filename, 'a') as csvFile:
         dataLogger = csv.writer(csvFile, delimiter=',', lineterminator='\n')
         dataLogger.writerow([time.strftime('%m/%d/%Y %H:%M:%S%z'),
                            str(MPL3115A2_Data[0]),     # pressure kPa
                            str(MPL3115A2_Data[1]),     # temperature C
                            str(MPL3115A2_Data[2]),     # temperature F
                            str(MPL3115A2_Data[3]),     # altitude m
                            str(LIS3DH_Data[0]),        # accel X
                            str(LIS3DH_Data[1]),        # accel Y
                            str(LIS3DH_Data[2]),        # accel Z
                            str(GPS_Data[0]),           # fix timestamp
                            str(GPS_Data[1]),           # fix Quality
                            str(GPS_Data[2]),           # latitude deg
                            str(GPS_Data[3]),           # longitude deg
                            str(GPS_Data[4]),           # # Satellites
                            str(GPS_Data[5]),           # altitude m
                            str(GPS_Data[6]),           # speed knots
                            str(GPS_Data[7]),           # track Angle
                            str(GPS_Data[8]),           # horizontal dilution
                            ])
    time.sleep(2)
