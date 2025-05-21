# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 08:16:26 2025

@author:  V.henry
"""

import time
import numpy as np
from hx711 import HX711
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

# Initialisation du capteur HX711
hx = HX711(5,6)
hx.set_reading_format("MSB", "MSB")
hx.reset()

def get_fast_weight(samples=20):
    """ Capture rapide (~1s), élimine les erreurs et renvoie un poids precis """
    values = np.zeros(samples)

    # Lire plusieurs valeurs en rafale
    for i in range(samples):
        values[i] = hx.get_weight(3)  # Lecture rapide (3 échantillons)
    
    # Trier les valeurs pour eliminer les extremes
    values = np.sort(values)
    filtered_values = values[int(0.1 * samples): int(0.9 * samples)]  # Garde 80% des meilleures

    return np.mean(filtered_values)  # Retourne la moyenne filtree

# Étape 1 : Mise à zero du capteur
hx.tare()
print("Capteur taré. Place un poids connu.")

# Mesure sans charge
valeur_sans_charge = get_fast_weight()

# Mesure avec charge
input("Place une charge connue et tape Entrée...")
time.sleep(1)  # Stabilisation

valeur_avec_charge = get_fast_weight()

# Demande du poids reel
poids_reel = float(input("Entrer le poids réel (g) : "))

# Calcul du facteur de calibration
REFERENCE_UNIT = (valeur_avec_charge - valeur_sans_charge) / poids_reel
hx.set_reference_unit(REFERENCE_UNIT)

input("Place une charge connue et tape Entrée...")
time.sleep(1)  # Stabilisation
hx.tare()

print(f"Calibration terminée ! Facteur : {REFERENCE_UNIT:.6f}")

# Mesures en boucle avec temps <2s
while True:
    poids = get_fast_weight() / 1000  # Conversion en kg
    print(f"Poids mesuré : {poids:.2f} kg")
