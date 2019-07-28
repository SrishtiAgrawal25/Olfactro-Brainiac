import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
class A: 
# read data using pin 14
   def demo(self):
	instance = dht11.DHT11(pin=8)

	while True:
	     	result = instance.read()
    		if result.is_valid():
        		#print("Last valid input: " + str(datetime.datetime.now()))
        		#print("Temperature: %d C" % result.temperature)
        		#print("Humidity: %d %%" % result.humidity)
			arr=[]
   			a = result.temperature
                        arr.append(a)
			b = result.humidity
                        arr.append(b)
			return arr
    		time.sleep(1)
