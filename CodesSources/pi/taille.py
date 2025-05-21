#Import des librairies GPIO et time (temps et conversion)#
import RPi.GPIO as GPIO 
import time

#Module GPIO: BOARD ou BCM (numerotation comme la serigraphie de la carte ou comme le chip)# 
GPIO.setmode(GPIO.BCM)

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000  
    


def measure(pin):
    """
    Mesure la distance via un capteur ultrason branché sur le pin donné.
    Déclenche une exception en cas de timeout sur la réponse.

    :param pin: Numéro BCM du GPIO connecté au capteur.
    :return: Distance en centimètres (float)
    :raises TimeoutError: si le capteur ne répond pas à temps.
    """
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
        time.sleep(0.000002)  # 2 µs
        GPIO.output(pin, True)
        time.sleep(0.00001)   # 10 µs
        GPIO.output(pin, False)

        GPIO.setup(pin, GPIO.IN)

        start = time.perf_counter()
        timeout = start + (_TIMEOUT1 / 1_000_000)
        while GPIO.input(pin) == 0:
            if time.perf_counter() > timeout:
                raise TimeoutError(f"Timeout front montant (pin {pin})")

        pulse_start = time.perf_counter()
        timeout = pulse_start + (_TIMEOUT2 / 1_000_000)
        while GPIO.input(pin) == 1:
            if time.perf_counter() > timeout:
                raise TimeoutError(f"Timeout front descendant (pin {pin})")

        pulse_end = time.perf_counter()
        pulse_duration = pulse_end - pulse_start

        distance = (pulse_duration * 1_000_000) / 29 / 2  # en cm
        return distance

    except TimeoutError as e:
        # Si log_erreur() est défini dans le contexte
        try:
            log_erreur(str(e))
        except NameError:
            pass  # log_erreur() n'est pas disponible dans ce module
        raise  # on relaie l'exception pour qu'elle soit gérée en amont



def initialisation_taille(pin_long, pin_larg, pin_haut):
    global haut_def
    global long_def
    global larg_def
    
    long_def = measure(pin_long)
    larg_def = measure(pin_larg)
    haut_def = measure(pin_haut)
    
"""
def check_pres(pin_long, pin_larg, pin_haut):
    global long_def, larg_def, haut_def
    start_time = time.time()

    while time.time() - start_time < 1.5:
        long_actuel = measure(pin_long)
        larg_actuel = measure(pin_larg)
        haut_actuel = measure(pin_haut)

        # Si la distance de l'un des capteurs change significativement (>2cm ici), on détecte une presence
        if haut_actuel < haut_def - 2:
            return 1  # Présence détectée

        time.sleep(0.1)

    return 0  # Aucune présence détectée après 3 secondes
"""
def get_hauteur(pin_haut):
    hauteur = measure(pin_haut)
    hauteur_finale = haut_def - hauteur
    return hauteur_finale

def get_longueur(pin_long):    
    longueur = measure(pin_long)
    longueur_finale = long_def - longueur
    return longueur_finale

def get_largeur(pin_larg):
    largeur = measure(pin_larg)
    largeur_finale = larg_def - largeur
    return largeur_finale


