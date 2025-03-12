import os
from functools import partial
from tkinter import *
from PIL import Image, ImageTk as itk
import RPi.GPIO as GPIO
import taille, time, board, busio, adafruit_vl53l0x, pesee
from datetime import datetime

fileSavePath = "/home/pi/Projet_Acer/Fichier_resultat"
pin_longueur = 16
pin_hauteur = 18
pin_largeur = 22

def checkpresence():
    distance = vl53.range#le capteur mesure une distance de 28mm quand on se trouve juste devant
    if distance < 50:
        carton['text'] = "Carton détecté"
        miseajour()
    else :
        carton['text'] = "Carton pas détecté"
        
def button_callback(channel):  #fonction qui permet la détection du changement d'état du bouton 
    if GPIO.input(12) == GPIO.LOW:
        checkpresence()
        
#def poweroff():
#os.system("sudo shutdown now")

def miseajour():
    hauteur_val = taille.get_hauteur(pin_hauteur)
    longueur_val = taille.get_longueur(pin_longueur)
    largeur_val = taille.get_largeur(pin_largeur)
    poids_val = pesee.get_poids()/1000
    
    hauteur['text'] = f"{hauteur_val:.0f} cm" #fait appel à la fonction get distance du programme taille sur la pin 4
    longueur['text'] = f"{longueur_val:.0f} cm" #fait appel à la fonction get distance du programme taille sur la pin 17
    largeur['text'] = f"{largeur_val:.0f} cm" #fait appel à la fonction get distance du programme taille sur la pin 4
    poids['text'] = f"{poids_val:.1f} kg"
    
    fichier = open(fileSavePath, "a")
    fichier.write('Date/Heure : '+(datetime.now()).strftime('%d/%m/%Y, %H:%M:%S')+'\nLongueur = '+str(longueur_val)+' cm / Largeur = '+str(largeur_val)+' cm / Hauteur = ' + str(hauteur_val) + ' cm /Poids = ' + str(poids_val) + ' kg\n-----------------------------------------\n')


def window1():#fenetre du menu parametre
    menu = Toplevel(ihm)
    #définir la taille de la fenêtre
    menu.attributes('-full',1)
    #définir la couleur de la fenêtre
    menu.configure(bg='white')
    
    Label(menu, text='Paramètres :', font=('Helvetica bold',20), background="#FFFFFF").grid(row=0, column=0)
    Button(menu, text='Quitter IHM', font=('Helvetica bold',20), command = ihm.destroy,padx="200", pady="70").grid(row=1, column=0)
    #Button(menu, text='Éteindre le banc', font=('Helvetica bold',20), command = poweroff()).grid(row=2, column=0)    

def Reset():
    # Initialisation des mesures
    pesee.initialisation_poids()
    taille.initialisation_taille(pin_longueur, pin_largeur, pin_hauteur)

    
GPIO.setmode(GPIO.BCM)

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
vl53.measurement_timing_budget = 200000

#interruption avec le bouton 'mesure' physique sur la pin 12
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(12, GPIO.BOTH, callback=button_callback)#bouncetime=2000

Reset()

ihm = Tk()
#Définition de la taille de la fenêtre
ihm.attributes('-full',1)
#Définition de la couleur de la fenêtre
ihm.configure(bg='white')
#Récupération de la taille de la fenêtre
#ihm.update()
width=ihm.winfo_width()
height=ihm.winfo_height()

#Placement = Frame(ihm, width=ihm.winfo_width(), height=ihm.winfo_height(), bg="#7698A6")
#Placement.pack(expand=True)

#column_size=width/3

#Label(ihm, text='', background="#FF0000", padx=column_size, pady="20").grid(column=0,row=0)
#Label(ihm, text='', background="#00FF00", padx=column_size, pady="20").grid(column=1,row=0)
#Label(ihm, text='', background="#0000FF", padx=column_size, pady="20").grid(column=2,row=0)

#affichage de l'image pour le bouton paramètre
parametreimg = Image.open("parametre.jpg")
parametreimg = parametreimg.resize((100,100))
parametreimg = itk.PhotoImage(parametreimg)

titre = Label(ihm, text='MESURES DU CARTON', font=('Helvetica bold',60), background="#FFFFFF", padx="300", pady="60")

butt_para = Button(ihm, image = parametreimg, command = window1)

Label(ihm, text='HAUTEUR = ', font=('Helvetica bold',40), background="#FFFFFF").grid(column=0, row=4)
hauteur = Label(ihm, text="0.0 cm", font=('Helvetica bold',40), background="#FFFFFF")

Label(ihm, text='LONGUEUR = ', font=('Helvetica bold',40), background="#FFFFFF").grid(column=0, row=5)
longueur = Label(ihm, text="0.0 cm", font=('Helvetica bold',40), background="#FFFFFF")

Label(ihm, text='LARGEUR = ', font=('Helvetica bold',40), background="#FFFFFF").grid(column=0, row=6)
largeur = Label(ihm, text="0.0 cm", font=('Helvetica bold',40), background="#FFFFFF")

Label(ihm, text='POIDS = ', font=('Helvetica bold',40), background="#FFFFFF").grid(column=0, row=7)
poids = Label(ihm, text="0.00 kg", font=('Helvetica bold',40), background="#FFFFFF")

butt_meas = Button(ihm, text='Mesure', font=('Helvetica bold',40), background="#FF0000", command = checkpresence,padx="100", pady="70")#bouton 'mesure' qui lance la fonction checkpresence

carton = Label(ihm, text="", background="#FFFFFF")

titre.grid(column=0, row=3)
butt_para.grid(column=2, row=0)

hauteur.grid(column=1, row=4)
longueur.grid(column=1, row=5)
largeur.grid(column=1, row=6)
poids.grid(column=1, row=7)

butt_meas.grid(column=0, row=8)
#butt_res.grid(column=0, row=9)
carton.grid(column=0, row=10)

ihm.mainloop()