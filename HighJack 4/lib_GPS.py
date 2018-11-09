#   Hafidh Satyanto
#   Library for Adafruit Ultimate GPS sensor

from micropyGPS import MicropyGPS
import time
import serial
#import threading

timezone_offset = -6

gps = MicropyGPS(timezone_offset)

srl = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    )

#def Update_Data():
#    while True:
#        srlline = srl.readline()
#        print(srlline)
#        for iter in srlline:
#            gps.update(iter)
#        time.sleep(1)

def Get_Data():
    try:
        srlline = srl.readline()
        for iter in srlline:
            gps.update(iter)

        latitude = gps.latitude             # degrees, minutes, string direction (S,N)
        longitude = gps.longitude           # degrees, minutes, string direction (W,E)
        altitude = gps.altitude             # meters
        speed = gps.speed[2]                # knots, miles per hour, kilometers per hour
        timestamp = gps.timestamp           # hours, minutes, seconds
        satellites = gps.satellites_in_use  # integer number
        fixtype = gps.fix_type              # 1 = no fix,  2 = 2D fix,  3 = 3D fix,

        return timestamp, fixtype, satellites, latitude, longitude, altitude, speed
        print(timestamp)
        print(latitude)
    except IOError:
        print('GPS Connection Error')
        return [0,0,0], 0, 0, [0,0,0], [0,0,0], 0, 0

if __name__ == "__main__":
    Get_Data()
    #counter = 0

    #thread = threading.Thread(target=Update_Data)
    #thread.start()
