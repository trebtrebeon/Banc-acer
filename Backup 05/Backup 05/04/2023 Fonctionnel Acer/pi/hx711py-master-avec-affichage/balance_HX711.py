#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Utilisation d'une balance avec HX711 et Raspberry Pi
Nécessite la bibliothèque: https://github.com/tatobari/hx711py
Plus d'infos:
https://electroniqueamateur.blogspot.com/2020/10/balance-base-de-raspberry-pi.html
'''

import time
import RPi.GPIO as GPIO
from hx711 import HX711

brocheDT = 5   # DT du HX711 branché à GPIO5
brocheSCK = 6  # SCK du HX711 branché à GPIO6

hx = HX711(brocheDT, brocheSCK) 

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(382.6) #calibration: le nombre dépend de votre balance
hx.reset()
hx.tare()
print("La balance est prete a etre utilisee")

while True:

    val = hx.get_weight(5)
    print(round(val,2))
    time.sleep(0.5)