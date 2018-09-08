from picamera import PiCamera
import subprocess
import time

cmd = "raspistill -o photo"+time.strftime('%mm%dd%yy_%Hh%Mm%Ss')+"%05d.jpg -t 0 -tl 5000"
subprocess.call(cmd, shell=True)
		

