#   Hafidh Satyanto
#   Didn't want to rewrite the driver, so I just made this simple Get_Data() function for consistency between this and the MPL3115A2


#   Recommended time.sleep(2)

#   Connect Vin to 3.3V    (NOT 5V)
#   GND to GND
#   SDA to SDA
#   SCL to SCL

from LIS3DH import LIS3DH

sensor = LIS3DH(debug=True)
sensor.setRange(LIS3DH.RANGE_8G)
x = [0, 0, 0]
y = [0, 0, 0]
z = [0, 0, 0]

def Get_Data():
    try:
        sensorx = sensor.getX()
        sensory = sensor.getY()
        sensorz = sensor.getZ() - 0.96
        x[0] = x[1]
        x[1] = x[2]
        x[2] = sensorx
        x_val = (x[0]+x[1]+x[2])/3
        y[0] = y[1]
        y[1] = y[2]
        y[2] = sensory
        y_val = (y[0]+y[1]+y[2])/3
        z[0] = z[1]
        z[1] = z[2]
        z[2] = sensorz
        z_val = (z[0]+z[1]+z[2])/3

        return x_val,y_val,z_val
    except IOError:
        print('LIS3DH Connection Error')
        return 0,0,0

if __name__ == "__main__":
    Get_Data()
