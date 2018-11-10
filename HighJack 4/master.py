from smbus import SMBus
import time
import csv
import serial
#import thread

LIS3DH = False
MPL3115A2 = False
GPS = False

deg = u'\N{DEGREE SIGN}'
apo = u"\u0027" #apostrophe

port = "/dev/ttyACM0"   ## USB Serial Port
serialport = serial.Serial(port,
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1
)

try:    ## Import LIS3DH Accelerometer
    import lib_LIS3DH
except ImportError:
    print('Error importing LIS3DH Sensor')
else:
    LIS3DH = True
    print('LIS3DH Accelerometer Connected')

try:    ## Import MPL3115A2 Barometeric Altimeter
    import lib_MPL3115A2
except ImportError:
    print('Error importing MPL3115A2 Sensor')
else:
    MPL3115A2 = True
    print('MPL3115A2 Altimeter Connected')

try:    ## Import GPS
    import lib_GPS
except ImportError:
    print('Error importing GPS Sensor')
else:
    GPS = True
    print('Adafruit GPS Connected')

datarows = [
    'Time',                                                 #0
    'Pressure (kPa)',                                       #1
    'Temperature ('+deg.encode("utf8")+'C)',                #2
    'Altitude Estimation (m)',                              #3
    'Acceleration (X)',                                     #4
    'Acceleration (Y)',                                     #5
    'Acceleration (Z)',                                     #6
    'Fix Timestamp (Hours)',                                #7
    'Fix Timestamp (Minutes)',                              #8
    'Fix Timestamp (Seconds)',                              #9
    'Fix Type',                                             #10
    '# Satellites',                                         #11
    'Latitude ('+deg.encode("utf8")+')',                    #12
    'Latitude ('+apo.encode("utf8")+')',                    #13
    'Latitude (Direction)',                                 #14
    'Longitude ('+deg.encode("utf8")+')',                   #15
    'Longitude ('+apo.encode("utf8")+')',                   #16
    'Longitude (Direction)',                                #17
    'Altitude GPS (m)',                                     #18
    'Speed (kph)',                                          #19
]

if (LIS3DH==False):
    datarows[4] = 'LIS3DH N/A',
    datarows[5] = 'LIS3DH N/A',
    datarows[6] = 'LIS3DH N/A',

if (MPL3115A2==False):
    datarows[1] = 'MPL3115A2 N/A',
    datarows[2] = 'MPL3115A2 N/A',
    datarows[3] = 'MPL3115A2 N/A',

if (GPS==False):
    datarows[7] = 'GPS N/A',
    datarows[8] = 'GPS N/A',
    datarows[9] = 'GPS N/A',
    datarows[10] = 'GPS N/A',
    datarows[11] = 'GPS N/A',
    datarows[12] = 'GPS N/A',
    datarows[13] = 'GPS N/A',
    datarows[14] = 'GPS N/A',
    datarows[15] = 'GPS N/A',
    datarows[16] = 'GPS N/A',
    datarows[17] = 'GPS N/A',
    datarows[18] = 'GPS N/A',
    datarows[19] = 'GPS N/A',

csv_filename = 'Data: '+time.strftime('%mm%dd%yy_%Hh%Mm%Ss')+'.csv'
with open(csv_filename, 'w') as dataInit:
    dataInit = csv.writer(dataInit, delimiter=',', lineterminator='\n')
    dataInit.writerow(datarows)

while True:
    if (MPL3115A2==True):
        MPL3115A2_Data = lib_MPL3115A2.Get_Data()
        MPL3115A2_Packet = "kPa:%.2f, C:%.1f, approx m:%.1d" % (MPL3115A2_Data[0], MPL3115A2_Data[1], MPL3115A2_Data[2])
    else:
        MPL3115A2_Data = [0, 0, 0, 0]
        MPL3115A2_Packet = ""

    if (LIS3DH==True):
        LIS3DH_Data = lib_LIS3DH.Get_Data()
        LIS3DH_Packet = ""
    else:
        LIS3DH_Data = [0, 0, 0]
        LIS3DH_Packet = ""

    if (GPS==True):
        GPS_Data = lib_GPS.Get_Data()
        GPS_Packet_fix = 'gps-fix:'+str(GPS_Data[1])+', '
        GPS_Packet_lat = 'lat:'+str(GPS_Data[3][0])+''+deg.encode("utf8")+''+str(GPS_Data[3][1])+''+apo.encode("utf8")+''+str(GPS_Data[3][2])+', '
        GPS_Packet_lon = 'lon:'+str(GPS_Data[4][0])+''.deg.encode("utf8")+''+str(GPS_Data[4][1])+''+apo.encode("utf8")+''+str(GPS_Data[4][2])+', '
        GPS_Packet_altitude = 'm:'+str(GPS_Data[5])+', '
        GPS_Packet_speed = 'kph:'+str(GPS_Data[6])+''
        GPS_Packet = GPS_Packet_fix + GPS_Packet_lat + GPS_Packet_lon + GPS_Packet_altitude + GPS_Packet_speed
    else:
        GPS_Data = [[0,0,0], 0, 0, [0,0,0], [0,0,0], 0, 0]
        GPS_Packet = ""

    with open(csv_filename, 'a') as csvFile:
         dataLogger = csv.writer(csvFile, delimiter=',', lineterminator='\n')
         dataLogger.writerow([time.strftime('%m/%d/%Y %H:%M:%S%z'),
                            str(MPL3115A2_Data[0]),     # pressure kPa
                            str(MPL3115A2_Data[1]),     # temperature C
                            str(MPL3115A2_Data[2]),     # altitude m
                            str(LIS3DH_Data[0]),        # accel X
                            str(LIS3DH_Data[1]),        # accel Y
                            str(LIS3DH_Data[2]),        # accel Z
                            str(GPS_Data[0][0]),        # fix timestamp hours
                            str(GPS_Data[0][1]),        # fix timestamp minutes
                            str(GPS_Data[0][2]),        # fix timestamp seconds
                            str(GPS_Data[1]),           # fix type integer
                            str(GPS_Data[2]),           # satellites integer
                            str(GPS_Data[3][0]),        # latitude degrees
                            str(GPS_Data[3][1]),        # latitude minutes
                            str(GPS_Data[3][2]),        # latitude string direction (S,N)
                            str(GPS_Data[4][0]),        # longitude degrees
                            str(GPS_Data[4][1]),        # longitude minutes
                            str(GPS_Data[4][2]),        # longitude string direction (W,E)
                            str(GPS_Data[5]),           # altitude m
                            str(GPS_Data[6]),           # speed
                            ])

    serialdata = serialport.readline()
    serialdatacheck = serialdata[ : 2]
    if (serialdatacheck=="XC"):    ## Special Command Mode
        if (serialdata=="XC test"):
            serialport.write("Received Command - Test")
        elif (serialdata == "XC hello"):
            serialport.write("Hello back to you!")
        else:
            serialport.write("Unknown Command")

    Packet = ''+MPL3115A2_Packet+', '+LIS3DH_Packet+', '+GPS_Packet+''
    serialport.write(Packet)
    time.sleep(0.75)
