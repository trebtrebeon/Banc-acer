import os
import time
from tkinter import Label, Button, Canvas, Frame, PhotoImage, Toplevel
import tkinter.font as tkFont
import pesee

class IHM:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='#2C3E50')
        

        self.labels = {}

        self.font_large = tkFont.Font(family='Helvetica', size=50, weight='bold')
        self.font_medium = tkFont.Font(family='Helvetica', size=40, weight='bold')
        self.font_small = tkFont.Font(family='Helvetica', size=20, weight='bold')

        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

        # === Determine le chemin absolu des images ===
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_haut_path = os.path.join(base_dir, "ACER.png")
        logo_bas_path = os.path.join(base_dir, "SALS.png")

        # === LOGO haut gauche avec reduction native ===
        try:
            self.logo_haut_img = PhotoImage(file=logo_haut_path).subsample(3, 3)
            self.logo_haut_label = Label(self.root, image=self.logo_haut_img, bg="#2C3E50")
            self.logo_haut_label.grid(column=0, row=0, sticky='nw', padx=10, pady=10)
        except Exception as e:
            print(f"Erreur chargement image haut: {e}")

        # === Titre centre ===
        self.label_titre = Label(self.root, text='MESURES DU CARTON', font=self.font_large,
                                 background="#2C3E50", foreground="white", pady=40)
        self.label_titre.grid(column=0, row=0, columnspan=4, sticky='n')

        # === Détecteur de survol en haut à droite ===
        self.zone_quitter = Frame(self.root, bg="#2C3E50", width=120, height=100)
        self.zone_quitter.grid(column=3, row=0, sticky='ne', padx=20, pady=20)

        # Bouton quitter créé et placé dans la zone_quitter
        self.butt_quitter = Button(
            self.zone_quitter,
            text="Quitter",
            font=self.font_small,
            command=self.root.quit,
            bg="#E74C3C", fg="white",
            activebackground="#E74C3C",
            activeforeground="white",
            relief="flat", padx=20, pady=10,
            bd=0, highlightthickness=0
        )
        self.butt_quitter.pack_forget()

        # Bouton calibrage créé et placé sous quitter dans la zone_quitter
        self.butt_calibrage = Button(
            self.zone_quitter,
            text="Calibrage",
            font=self.font_small,
            command=self.ouvrir_modal_calibrage,
            bg="#2980B9", fg="white",
            activebackground="#2980B9",
            activeforeground="white",
            relief="flat", padx=20, pady=10,
            bd=0, highlightthickness=0
        )
        self.butt_calibrage.pack_forget()

        # Bind les événements Enter et Leave sur la zone complète
        self.zone_quitter.bind("<Enter>", self._afficher_boutons)
        self.zone_quitter.bind("<Leave>", self._cacher_boutons)

        # === Indicateur de detection ===
        self.frame_detection = Frame(self.root, bg="#2C3E50")
        self.frame_detection.grid(column=3, row=3, pady=20, sticky='nsew')

        self.labels["carton"] = Label(self.frame_detection, font=self.font_medium,
                                      background="#2C3E50", foreground="white")
        self.labels["carton"].pack(side="right", padx=10)

        self.indicateur_canvas = Canvas(self.frame_detection, width=85, height=85, bg="#2C3E50", highlightthickness=0)
        self.indicateur_canvas.pack(side="left")

        # === Labels des mesures ===
        self._creer_label("HAUTEUR", "hauteur", 2)
        self._creer_label("LONGUEUR", "longueur", 3)
        self._creer_label("LARGEUR", "largeur", 4)
        self._creer_label("MASSE", "masse", 5)

        # === LOGO bas droite avec reduction native ===
        try:
            self.logo_bas_img = PhotoImage(file=logo_bas_path).subsample(3, 3)
            self.logo_bas_label = Label(self.root, image=self.logo_bas_img, bg="#2C3E50")
            self.logo_bas_label.grid(column=3, row=5, sticky='se', padx=10, pady=10)
        except Exception as e:
            print(f"Erreur chargement image bas: {e}")

        self.update_label("carton", "Non détecté")
        self.activer_fullscreen_apres_affichage()

    def _afficher_boutons(self, event=None):
        self.butt_quitter.pack(fill='x', pady=2)
        self.butt_calibrage.pack(fill='x', pady=2)

    def _cacher_boutons(self, event=None):
        self.butt_quitter.pack_forget()
        self.butt_calibrage.pack_forget()

    def ouvrir_modal_calibrage(self):
        modal = Toplevel(self.root)
        modal.title("Calibrage")
        modal.configure(bg="#34495E")
    
        modal.overrideredirect(True)  # Supprime la bordure et la barre de titre
        modal.geometry(f"{modal.winfo_screenwidth()}x{modal.winfo_screenheight()}+0+0")  # Taille écran
        
        modal.focus_force()
        modal.transient(self.root)
        modal.grab_set()
    
        self.label_calibrage = Label(modal, text="Calibrage", font=self.font_medium, bg="#34495E", fg="white")
        self.label_calibrage.pack(pady=20)
        
        Button(modal, text="Lancer calibrage", command=self.lancer_calibrage, bg="#2980B9", fg="white", relief="flat", padx=15, pady=10).pack(pady=10)

        Button(modal, text="Fermer", command=modal.destroy, bg="#E74C3C", fg="white", relief="flat", padx=15, pady=10).pack(pady=10)
    
        # Sauvegarder la référence au modal pour y accéder dans la méthode de calibration
        self.modal_calibrage = modal
    
    
    def _creer_label(self, texte, cle, ligne):
        frame = Frame(self.root, bg="#2C3E50")
        frame.grid(column=0, row=ligne, padx=10, pady=10, sticky="ew")
        self.root.grid_rowconfigure(ligne, weight=1)

        Label(frame, text=f"{texte} =", font=self.font_medium, background="#2C3E50", foreground="white")\
            .pack(side="left")

        self.labels[cle] = Label(frame, text="0", font=self.font_medium, background="#2C3E50", foreground="white")
        self.labels[cle].pack(side="right")

    def update_label(self, cle, valeur):
        if cle in self.labels:
            self.labels[cle]["text"] = valeur
            if cle == "carton":
                if valeur == "Mesures terminées":
                    self._mettre_a_jour_indicateur("green")
                elif valeur == "Non détecté":
                    self._mettre_a_jour_indicateur("red")
                elif valeur == "Mesures en cours":
                    self._mettre_a_jour_indicateur("yellow")

    def _mettre_a_jour_indicateur(self, couleur):
        self.indicateur_canvas.delete("all")
        couleurs = {"yellow": "#F39C12", "green": "green", "red": "red"}
        if couleur in couleurs:
            self.indicateur_canvas.create_oval(5, 5, 75, 75, fill=couleurs[couleur], outline=couleurs[couleur])

    def activer_fullscreen_apres_affichage(self):
        if self.root.winfo_ismapped():
            self.root.attributes("-fullscreen", True)
        else:
            self.root.after(500, self.activer_fullscreen_apres_affichage)
            
            
            
    def lancer_calibrage(self):
        # Affiche un message de début dans le label du modal
        self.label_calibrage["text"] = "Début calibration automatique...\n"
    
        # Petit délai pour laisser l'utilisateur placer la masse
        self.root.after(2000, self._etape_tare)
        
    
    def _etape_tare(self):
        try:
            pesee.initialisation_poids()
            pesee.tare()
            self.label_calibrage["text"] = "Capteur taré.\nPlacer la masse de 20 kg, la mesure commence dans 15 secondes"
            self.root.after(15000, self._etape_mesure)
        except Exception as e:
            self.label_calibrage["text"] = f"Erreur initialisation : {e}"
    
    def _etape_mesure(self):
        try:
            self.label_calibrage["text"] = "Lecture de la masse..."
            self.root.after(100, self._mesure_finale)
        except Exception as e:
            self.label_calibrage["text"] = f"Erreur mesure : {e}"
    
    def _mesure_finale(self):
        try:
            poids_brut = pesee.get_fast_weight()
            MASSE_REFERENCE = 20000000
            if poids_brut is None:
                self.label_calibrage["text"] = "Erreur lecture masse."
                return
            reference_unit = poids_brut / MASSE_REFERENCE
            pesee.set_reference_unit(reference_unit)
            self.label_calibrage["text"] = "Calibration terminée !\nRetirer toute masse, tare dans 15 secondes..."
            self.root.after(15000, self._faire_tare)
        except Exception as e:
            self.label_calibrage["text"] = f"Erreur finale : {e}"

    def _faire_tare(self):
        try:
            pesee.tare()
            self.label_calibrage["text"] = "Capteur taré. Vous pouvez quitter"
        except Exception as e:
            self.label_calibrage["text"] = f"Erreur tare : {e}"



