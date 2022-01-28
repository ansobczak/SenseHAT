#ReadSensors - there is alias rs on Pi
from pisense import SenseHAT
from time import sleep, time
hat=SenseHAT()

print("")
while 1:
	print("temp    %2.2f  press   %2.2f  humid   %2.2f" % (hat.environ.temperature, hat.environ.pressure, hat.environ.humidity),end="\r")
	sleep(1)


