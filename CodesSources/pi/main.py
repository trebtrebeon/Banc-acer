# main.py
import threading
import RPi.GPIO as GPIO
from tkinter import Tk

import FonctionsMain
from IHM import IHM

# Initialisation des capteurs
PINS = {
    "longueur": 16,
    "hauteur": 18,
    "largeur": 22
}
PINSPRESENCE = 21
LOG_REPOSITORY = "/home/pi/Documents/2023 Fonctionnel Acer/pi/logs"

FonctionsMain.reset(PINS)

# Lancement interface
root = Tk()
# Instantiation de l'interface
ihm = IHM(root)

# Lancement de la detection en fond (en passant l'instance IHM)
thread_detection = threading.Thread(target=FonctionsMain.check_presence, args=(ihm, PINS, PINSPRESENCE), daemon=True)
thread_detection.start()

#Suppression des fichiers de logs de plsu de deux mois
FonctionsMain.supprimer_anciens_logs(LOG_REPOSITORY, jours=60)


try:
    root.mainloop()
finally:
    GPIO.cleanup()

