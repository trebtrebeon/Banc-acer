#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Utilisation d'une balance avec HX711 et Raspberry Pi
(version avec interface graphique)
Nécessite la bibliothèque: https://github.com/tatobari/hx711py

Plus d'infos:
https://electroniqueamateur.blogspot.com/2020/10/balance-base-de-raspberry-pi.html

'''

import time
import RPi.GPIO as GPIO
from hx711 import HX711
from tkinter import *
brocheDT = 5   # DT du HX711 branché à GPIO5
brocheSCK = 6  # SCK du HX711 branché à GPIO6

hx = HX711(brocheDT, brocheSCK) 

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(22.5) #calibration: le nombre dépend de votre balance
hx.reset()
hx.tare()

fenetre = Tk()    # création d'une fenêtre
fenetre.geometry("300x100+150+150")   # taille de la fenêtre et position initiale sur l'écran
fenetre.title("Balance")   # titre de la fenêtre

label = Label(fenetre, text=" ")  # ligne vide
label.pack()

label1 = Label(fenetre, fg="red", text="Masse mesurée:")
label1.pack()

label = Label(fenetre, text=" ")  # ligne vide
label.pack()

label2 = Label(fenetre, text=" ")  # contiendra la mesure totale
label2.pack()

def Majvaleur():
    label2['text'] = "{0:0.1f}".format(hx.get_weight(5)) + " grammes"
    fenetre.after(1000, Majvaleur) # on recommence dans 1 seconde

fenetre.after(1000, Majvaleur)

fenetre.mainloop()

