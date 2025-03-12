from tkinter import *
import time, sys
from hx711 import HX711
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

hx = HX711(5, 6)
referenceUnit = 1

def initialisation_poids():
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(21.4)
    hx.reset()
    hx.tare()

def get_poids():
    poids = hx.get_weight(5)
    hx.power_down()
    hx.power_up()
    return poids

#initialisation_poids()
#while(1):
    #val = get_poids()
    #time.sleep(1)
    #print(val)