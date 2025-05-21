import numpy as np
from hx711 import HX711
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)

# Fichier de sauvegarde pour la référence
FICHIER_REF_UNIT = "reference_unit.txt"

# Valeur par défaut si aucun fichier trouvé
REFERENCE_UNIT_PAR_DEFAUT = 21.378655

hx = HX711(5, 6)

def sauvegarder_reference_unit(value, filename=FICHIER_REF_UNIT):
    try:
        with open(filename, "w") as f:
            f.write(str(value))
    except Exception as e:
        print(f"[ERREUR] Impossible de sauvegarder reference_unit : {e}")

def charger_reference_unit(filename=FICHIER_REF_UNIT):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r") as f:
            value = float(f.read())
        return value
    except Exception as e:
        print(f"[ERREUR] Impossible de charger reference_unit : {e}")
        return None

def initialisation_poids():
    ref = charger_reference_unit()
    if ref is None:
        ref = REFERENCE_UNIT_PAR_DEFAUT

    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(ref)
    hx.reset()
    hx.tare()

def get_poids(samples=10):
    try:
        valeurs = np.array([hx.get_weight(5) for _ in range(samples)])
        valeurs = np.sort(valeurs)
        keep = valeurs[int(0.1 * samples): int(0.9 * samples)]
        moyenne = np.mean(keep) / 1000  # kg

        if moyenne < 0 or np.isnan(moyenne):
            raise ValueError("Valeur de poids invalide")

        return moyenne
    except Exception as e:
        print(f"[ERREUR] Lecture du poids échouée : {e}")
        return None
    
    
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
    

def tare():
    try:
        hx.reset()
        hx.tare()
    except Exception as e:
        print(f"[ERREUR] Impossible d'effectuer la tare : {e}")

def set_reference_unit(value):
    hx.set_reference_unit(value)
    sauvegarder_reference_unit(value)  # Sauvegarde à chaque calibration
