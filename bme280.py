import time
from datetime import datetime

counterfile = open("bme280counter.txt","r")
cur = counterfile.read()
newcur = int(cur)+1
newcounterfile = open("bme280counter.txt","w")
newcounterfile.write(str(newcur))


#Initialization
for x in range(0,3):
    try:
        from Adafruit_BME280 import *
        str_error = None
    except Exception as str_error:
        print 'BME280: Fail to import Adafruit_BME280 Library'
        pass

    if str_error:
        sleep(1)
    else:
        break

for x in range(0,3):
    try:
        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
        str_error = None
    except Exception as str_error:
        print 'Sensor initialization failed'
        pass

    if str_error:
        sleep(1)
    else:
        break

loopcounter = 0
DataName = "BME280"+str(cur)
DataFile = open(str(DataName).csv, "a")
DataFile.write("Time,Iteration,Temperature,Pressure,Humidity,Altitude")

#Loop Receive Data
while True:
    for x in range(0, 3):
        try:
            sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
            str_error = None
        except Exception as str_error:
            print 'Sensor Initialization Failed'
            pass

        if str_error:
            sleep(1)
        else:
            break


    for x in range(0, 3):
        try:
            degrees = sensor.read_temperature()
            str_error = None
        except Exception as str_error:
            print 'BME280 Read Temperature Failed'
            degrees = 0000
            pass

        if str_error:
            sleep(1)
        else:
            break

    for x in range(0, 3):
        try:
            pascals = sensor.read_pressure()
            hectopascals = pascals / 100
            str_error = None
        except Exception as str_error:
            print 'BME280 Read Pressure Failed'
            pascals = 0000
            degrees = 0000
            pass

        if str_error:
            sleep(1)
        else:
            break

    for x in range(0, 3):
        try:
            humidity = sensor.read_humidity()
            str_error = None
        except Exception as str_error:
            print 'BME280 Read Humidity Failed'
            humidity = 0000
            pass

        if str_error:
            sleep(1)
        else:
            break

    loopcounter = loopcounter+1;
    timestr = str(datetime.now())
    loopcounterstr = str(loopcounter)
    tempstr = str(degrees)
    presstr = str(hectopascals)
    humstr = str(humidity)

    DataFile.write(','.join([timestr,loopcounterstr,tempstr,presstr,humstr]))
    sleep(2)
