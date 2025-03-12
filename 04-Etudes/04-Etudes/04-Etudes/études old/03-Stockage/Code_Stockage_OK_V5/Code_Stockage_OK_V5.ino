#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include "RTClib.h"

File fichierSD;
RTC_DS1307 rtc;


void setup () {
  Serial.begin(115200);
  //Pour la carte SD=====================
  //Initialisation de la CARTE SD
  if (!SD.begin(53))// Pin 53 pour Arduino Mega
  {
    Serial.println(F("Initialisation impossible !"));
    return;
  }
  Serial.println(F("Initialisation OK"));
  //Fin carte SD==========================

  rtc.begin(); // Lancement de l'horloge.
  if (! rtc.isrunning())
  {
    Serial.println("RTC NOK");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop() {

  DateTime now = rtc.now();

  //On envoie dans le moniteur série l'info écrite
  Serial.print(now.year(), DEC);
  Serial.print('/');
  Serial.print(now.month(), DEC);
  Serial.print('/');
  Serial.print(now.day(), DEC);
  Serial.print(' ');
  Serial.print(now.hour(), DEC);
  Serial.print(':');
  Serial.print(now.minute(), DEC);
  Serial.print(':');
  Serial.print(now.second(), DEC);
  Serial.print(";");
  Serial.println("Valeur");
  delay(1000);

  //On nomme le fichier selon la date, donc toutes les donnees prises le meme jour dans un seul fichier==========
  char datafile[13]; //tableau de 13 espaces pour le nom
  int jour = now.day();
  int mois = now.month();
  int annee = now.year();
  sprintf(datafile, "%02d%02d%04d.csv", jour, mois, annee); // %d pour un int
  datafile[13] = '\0'; //à mettre pour fermer convenablement le fichier
  //Fin nommer fichier==================

  //Ouverture du fichier==========================
  fichierSD = SD.open(datafile, FILE_WRITE);

  //Test pour écriture
  if (fichierSD) {
    Serial.println(F("Ecriture en cours"));
    //Ecriture
    maintenant();
    fichierSD.print(";");
    fichierSD.print(";");
    fichierSD.print("Longueur : ");
    fichierSD.print("XXX");
    fichierSD.print(' ');
    fichierSD.print("cm");
    fichierSD.print(";");
    fichierSD.print(";");
    fichierSD.print("Largeur : ");
    fichierSD.print("XXX");
    fichierSD.print(' ');
    fichierSD.print("cm");
    fichierSD.print(";");
    fichierSD.print(";");
    fichierSD.print("Hauteur : ");
    fichierSD.print("XXX");
    fichierSD.print(' ');
    fichierSD.print("cm");
    fichierSD.println(";");
    fichierSD.close();
  }
  //Fermeture du fichier avec une ligne de plus============
  delay(1000);//durée en ms entre les mesures
}

//Fonction qui écrit la date et l'heure dans le fichierSD
void maintenant() {
  DateTime now = rtc.now();

  fichierSD.print(now.year(), DEC);
  fichierSD.print('/');
  fichierSD.print(now.month(), DEC);
  fichierSD.print('/');
  fichierSD.print(now.day(), DEC);
  fichierSD.print(";");
  fichierSD.print(now.hour(), DEC);
  fichierSD.print(':');
  fichierSD.print(now.minute(), DEC);
  fichierSD.print(':');
  fichierSD.print(now.second(), DEC);
  delay(2000);
}
