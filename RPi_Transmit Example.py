import Time
import serial

serialport = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

message = "This is a test message. My name is Giorgino and I like pizza and pasta. I wear a red hat and I jump on bricks."
serialport.write(message)
time.sleep(2)
message2 = "Another one. Also, my name is Guyeguye and I am missing in action."
serialport.write(message2)
time.sleep(2)
serialport.close
