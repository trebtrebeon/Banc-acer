import RPi.GPIO as GPIO
import tkinter
from tkinter import *
from tkinter import PhotoImage, Tk, Canvas
import time
#import VL53L0X
from hx711 import HX711
from datetime import datetime
from math import *

GPIO.setwarnings(False)

#tof = VL53L0X.VL53L0X()
#tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

def checkdistance():
    distance = tof.get_distance()
    if distance/10 < 20:
    # quand il y a quelque chose devant le capteur
        return(True)
    else: # quand il y a rien devant le capteur
        return(False)

Echo = 21
Trig = 20

Echo2 = 24
Trig2 = 23

Echo3 = 17
Trig3 = 27

bouton = 16

brocheDT = 5   # DT du HX711 branché à GPIO5
brocheSCK = 6  # SCK du HX711 branché à GPIO6

hx = HX711(brocheDT, brocheSCK)

GPIO.setmode(GPIO.BCM)

GPIO.setup(Echo, GPIO.IN)
GPIO.setup(Trig, GPIO.OUT)

GPIO.setup(Echo2, GPIO.IN)
GPIO.setup(Trig2, GPIO.OUT)

GPIO.setup(Echo3, GPIO.IN)
GPIO.setup(Trig3, GPIO.OUT)

GPIO.setup(bouton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(Trig, GPIO.LOW)

GPIO.output(Trig2, GPIO.LOW)

GPIO.output(Trig3, GPIO.LOW)

#tout ce qu'il y a avant concerne les déclarations, si besoin info, taper sur internet la ligne de code

def button_callback(channel):  #fonction qui permet la détection du changement d'état du bouton 
    if GPIO.input(bouton) == GPIO.LOW:
        print("Button was pushed!")
        Measures()

GPIO.add_event_detect(bouton,GPIO.RISING,callback=button_callback) 	


global dist_largeur			#variables globales 
global dist_longueur
global dist_hauteur
global Mesures

def Measures(): #fonction qui gère la prise de mesures
    dist_largeur = 0.0
    dist_longueur = 0.0
    dist_hauteur = 0.0
    ok = False
    
    #distance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]		#les 3 tableaux permettent une moyenne de 20mesures
    #distance2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    #distance3 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    pulse_start = time.time()			#gestion du premier ultrason, on envoie une onde, on check la durée avant de recevoir l'onde, on a donc un temps, on connait la vitesse de l'onde.
    time.sleep(0.005)				# on peut donc calculer la distance v = d / t 
    GPIO.output(Trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trig, GPIO.LOW)
    
    while GPIO.input(Echo)==0:
        pulse_start = time.time()
        
    while GPIO.input(Echo)==1:
        pulse_end = time.time()
    
    delta_T = pulse_end - pulse_start

    distance = (delta_T * 340 * 100 / 2)				#calcul expliqué dessus, on cherche la distance 
															#  je précise que la température est négligeable pour la vitesse de l'ultrason
    dist_largeur = int(round(97.5 - distance))			# le 98 correspond à la distance une fois installer, pour faire des tests sans être sur la table ACER, enlever le "98 - "
    dist_largeur = str(dist_largeur)				#conversion de la distance en string pour faciliter l'affichage dans le fichier résultat


    pulse_start2 = time.time()  				#même chose que précédemment mais pour le deuxième ultrason
    time.sleep(0.005)
    GPIO.output(Trig2, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trig2, GPIO.LOW)

    while GPIO.input(Echo2)==0:
        pulse_start2 = time.time()

    while GPIO.input(Echo2)==1:
        pulse_end2 = time.time()
    
    delta_T = pulse_end2 - pulse_start2

    distance2 = (delta_T * 340 * 100 / 2)
    dist_longueur =  int(round(97.5 - distance2)) 			#pensez à enlever le "98 - " pour tests hors de la table ACER
    dist_longueur = str(dist_longueur)
    
    
    pulse_start3 = time.time()  				#même chose que précédemment mais pour le troisième ultrason
    time.sleep(0.005)
    GPIO.output(Trig3, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trig3, GPIO.LOW)

    while GPIO.input(Echo3)==0:
        pulse_start3 = time.time()

    while GPIO.input(Echo3)==1:
        pulse_end3 = time.time()
    
    delta_T = pulse_end3 - pulse_start3

    distance3 = (delta_T * 340 * 100 / 2)
    
    dist_hauteur = int(round(110 - distance3)) 			#pensez à enlever le "110 - " pour tests hors de la table ACER
    dist_hauteur = str(dist_hauteur)
    
    
    hx.set_reading_format("MSB", "MSB")                 #mesure du poids
    hx.set_reference_unit(382.6)                        #calibration: le nombre dépend de votre balance
    hx.reset()
    hx.tare()
    
    while True:

        poids = hx.get_weight(5)
        time.sleep(0.5)
    
    
    if(checkdistance()):
        time.sleep(0.1)
        print('longueur :', dist_largeur)
        print('largeur :', dist_longueur)
        print('hauteur :', dist_hauteur)
        print('poids :', poids)
        C.itemconfigure(texte, text='Longueur = ' + dist_largeur +' cm \n\nLargeur = ' + dist_longueur +'cm \n\nHauteur = ' + dist_hauteur + ' cm \n\nPoids = ' + poids + ' kg', font=('helvetica', 30))
        fichier = open("/home/pi/Documents/Projet Acer Capteur Ultrasons/ultrasonic/Fichier_resultat", "a")
        fichier.write('Date/Heure : '+(datetime.now()).strftime('%d/%m/%Y, %H:%M:%S')+'\nLongueur = '+dist_largeur+' cm / Largeur = '+dist_longueur+' cm / Hauteur = ' + dist_hauteur + ' cm /Poids = ' + poids + ' kg\n-----------------------------------------\n')
        ok = True
    if(ok == False):
        print("Mettez un carton devant le capteur")
        C.itemconfigure(texte, text='Longueur = 00 cm \n\nLargeur = 00 cm \n\nHauteur = 00 cm \n\nPoids = 00 kg', font=('helvetica', 30))
    																		#les lignes 112 à 119 gère l'écriture du fichier résultat, fichier qui doit être dans le même dossier
    
Mesures = tkinter.Tk()					#gestion de l'ihm, version très basique pour le moment (voir librairie Tkinter pour + d'infos)
Mesures.title('Mesures')
Mesures.attributes('-fullscreen',True)

#img = PhotoImage(file='/home/pi/Documents/ultrasonic/acer.png', master=Mesures)
C = Canvas(Mesures, width=1280, height=1024)
#C.create_image(500,385, image=img)
C.create_text(500,50, text= 'Cliquer sur le bouton pour voir les dimensions.', font = ('helvetica',35))
texte = C.create_text(500,300, text='Longueur = 00 cm \n\n\nLargeur = 00 cm \n\n\nHauteur = 00 cm', font=('helvetica', 30))
C.pack()
mes_btn = Button(Mesures, text='Mesurer', command=dist, font='helvetica')
mes_btn = C.create_window(500, 600, window=mes_btn)

Mesures.mainloop()					#on execute en boucle "Mesures", "Mesures" qui est la fenêtre Tkinter (voir ligne 122)
   								#l'appui sur le bouton virtuel ou physique lance l'execution de la fonction Measures()

