# Maglogday by Marc Segura
#This program logs two geomagnetic readings per minute. It is used in conjunction with the FLC 100 magnetometer,
#the DHT11 temperature and humidity sensor and the ADS1115 analogue-to-digital converter.

import RPi.GPIO as GPIO
import dht11
import Adafruit_ADS1x15
import time
import datetime
import csv

from time import strftime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin=13)

def blink(): #This blinking pattern will allow us to verify that the program is running without needing a monitor
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(17,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(17,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(17,GPIO.LOW)



adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2



while True:

        dt = datetime.datetime.now()

        today = datetime.datetime.now().day
        logfile = '/home/pi/Magnetometer/data/mag-%s.csv' % (strftime("%d%m%Y")) #A new csv file is written evvery day
        while(datetime.datetime.now().day == today): # The name of the csv file will be mag-DDMMYYYY

            with open(logfile,"a") as log:    

                GPIO.setup(17,GPIO.OUT)
                result = instance.read()
                A0 = adc.read_adc(0, gain=GAIN)
                #A1 = adc.read_adc(1, gain=GAIN) #Uncomment these two lines if you are using 2 or 3 magnetometers
                #A2 = adc.read_adc(2, gain=GAIN) #Uncomment the lines bellow as well if you are using 2 or 3 magnetometers
                print("Temperature: %d C" % result.temperature)
                print("Humidity: %d %%" % result.humidity)
                print("A0: %d" % A0)
	        log.write("{0},{1},{2},{3}\n".format(strftime("%H:%M"),str(result.temperature),str(result.humidity),str(A0)))
                #log.write("{0},{1},{2},{3},{4}\n".format(strftime("%H:%M"),str(result.temperature),str(result.humidity),str(A0),str(A1)))
                #log.write("{0},{1},{2},{3},{4},{5}\n".format(strftime("%H:%M"),str(result.temperature),str(result.humidity),str(A0),str(A1),str(A2)))
                blink()
                time.sleep(27.5) #30 seconds between readings (accounting for the 2.5 seconds lost to the blinking function) 

