# fonctions.py
import time
import taille, pesee
import RPi.GPIO as GPIO
import os
from datetime import datetime



GPIO.setmode(GPIO.BCM)

def check_pres(PINSPRESENCE):
    GPIO.setup(21,GPIO.IN)
    return GPIO.input(PINSPRESENCE)

def miseajour(ihm, pins):
    try:
        longueur_val = taille.get_longueur(pins["longueur"])
        largeur_val = taille.get_largeur(pins["largeur"])
        hauteur_val = taille.get_hauteur(pins["hauteur"])

        ihm.update_label("longueur", f"{longueur_val:.0f} cm")
        ihm.update_label("largeur", f"{largeur_val:.0f} cm")
        ihm.update_label("hauteur", f"{hauteur_val:.0f} cm")
    except Exception as e:
        log_erreur(f"Erreur lecture dimensions : {e}")
        ihm.update_label("longueur", "Erreur")
        ihm.update_label("largeur", "Erreur")
        ihm.update_label("hauteur", "Erreur")
        return  # On arrête ici car les mesures ne sont pas fiables

    masse_val = pesee.get_poids()
    if masse_val is not None:
        ihm.update_label("masse", f"{masse_val:.2f} kg")
    else:
        ihm.update_label("masse", "Erreur mesure, recommencer")
        log_erreur("Erreur de lecture du poids (retour None)")

    log_mesure(longueur_val, largeur_val, hauteur_val, masse_val)



def check_presence(ihm, pins, pinsPresence, carton_present=False):
    while True:
        try:
            if check_pres(pinsPresence):
                if not carton_present:
                    carton_present = True
                    ihm.update_label("carton", "Carton détecté")
                    time.sleep(1)
                    ihm.update_label("carton", "Mesures en cours")
                    miseajour(ihm, pins)                
                    ihm.update_label("carton", "Mesures terminées")
            else:
                carton_present = False
                ihm.update_label("carton", "Non détecté")
                ihm.update_label("longueur", "0 cm")
                ihm.update_label("largeur", "0 cm")
                ihm.update_label("hauteur", "0 cm")
                ihm.update_label("masse", "0 kg")
            time.sleep(0.5)
        except Exception as e:
            log_erreur(f"Erreur dans check_presence : {e}")
            time.sleep(1)


def reset(pins):
    try:
        pesee.initialisation_poids()
        taille.initialisation_taille(
            pins["longueur"],
            pins["largeur"],
            pins["hauteur"]
        )
    except TimeoutError as e:
        print(f"[ERREUR INIT] {e}")
        log_erreur(f"Échec à l'initialisation des capteurs : {e}")


def log_mesure(longueur, largeur, hauteur, masse, dossier_log="/home/pi/Documents/2023 Fonctionnel Acer/pi/logs"):
    """
    Enregistre une mesure de dimensions et de masse dans un fichier .log quotidien.
    
    :param longueur: Longueur en cm
    :param largeur: Largeur en cm
    :param hauteur: Hauteur en cm
    :param masse: Masse en g
    :param dossier_log: Dossier où enregistrer les fichiers de log
    """
    os.makedirs(dossier_log, exist_ok=True)

    # Format : log_2025-05-19.log
    nom_fichier = os.path.join(dossier_log, f"log_{datetime.now().date()}.log")

    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = (
        f"[{horodatage}] Carton - Longueur: {longueur:.2f} cm, "
        f"Largeur: {largeur:.2f} cm, Hauteur: {hauteur:.2f} cm, "
        f"Masse: {masse:.2f} kg\n"
    )

    with open(nom_fichier, mode='a') as f:
        f.write(ligne)
    
    # Nettoyage des anciens fichiers
    incremente_compteur(dossier_log)

def log_erreur(message, dossier_log='logs'):
    """
    Enregistre un message d'erreur dans le fichier .log quotidien.

    :param message: Message d'erreur à consigner
    :param dossier_log: Répertoire où stocker les logs
    """
    os.makedirs(dossier_log, exist_ok=True)
    nom_fichier = os.path.join(dossier_log, f"log_{datetime.now().date()}.log")

    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = f"[{horodatage}] ERREUR - {message}\n"

    with open(nom_fichier, mode='a', encoding='utf-8') as f:
        f.write(ligne)



def supprimer_anciens_logs(dossier, jours=60):
    """
    Supprime les fichiers .log plus vieux que 'jours' jours dans le dossier spécifié.
    """
    maintenant = datetime.now()
    for nom in os.listdir(dossier):
        if nom.startswith("log_") and nom.endswith(".log"):
            try:
                date_str = nom[4:-4]  # extrait la date entre "log_" et ".log"
                date_log = datetime.strptime(date_str, "%Y-%m-%d")
                if (maintenant - date_log).days > jours:
                    chemin = os.path.join(dossier, nom)
                    os.remove(chemin)
                    print(f"[INFO] Fichier supprimé : {chemin}")
            except ValueError:
                # Nom de fichier inattendu, on ignore
                continue

def incremente_compteur(dossier_log):
    chemin_compteur = os.path.join(dossier_log, "counter.txt")

    # Lire compteur existant
    try:
        with open(chemin_compteur, 'r') as f:
            compteur = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        compteur = 0

    # Incrémenter et sauvegarder
    compteur += 1
    with open(chemin_compteur, 'w') as f:
        f.write(f"{compteur}\n")

