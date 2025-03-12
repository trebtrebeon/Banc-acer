// Libraire :

#include <SPFD5408_Adafruit_GFX.h>    // Core graphics library
#include <SPFD5408_Adafruit_TFTLCD.h> // Hardware-specific library
#include <SPFD5408_TouchScreen.h>
#include <Wire.h>
#include <VL53L0X.h>
#include <SPI.h>
#include <SD.h>
#include "RTClib.h"

// Déclaration Variables et Constantes :

File fichierSD;
RTC_DS1307 rtc;
VL53L0X sensor;

#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0
#define LCD_RESET A4 // Can alternately just connect to Arduino's reset pin
#define BLACK  0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

unsigned char txbuf[10] = {0};
unsigned char rxbuf[10] = {0};
int i2cWriteBytes2 = 0;
int Longueur = 0;
int Largeur = 0;
int Hauteur = 0;
int but1 = 0;
int but2 = 0;
int but3 = 0;
int presence = 9;
unsigned char i = 0, x = 0;
typedef enum { SLAVEADDR_INDEX = 0, PID_INDEX, VERSION_INDEX, DIST_H_INDEX, DIST_L_INDEX, TEMP_H_INDEX, TEMP_L_INDEX, CFG_INDEX, CMD_INDEX, REG_NUM } regindexTypedef;
#define    MEASURE_MODE_PASSIVE    (0x00)
#define    MEASURE_RANG_150      (0x00)
#define    CMD_DISTANCE_MEASURE    (0x01)

unsigned char addr0 = 0x12;
unsigned char addr1 = 0x13;
unsigned char addr2 = 0x11;
unsigned char n = 0;

void setup() {
  Serial.begin(115200);
  tft.reset();
  tft.begin(0x9341); // SDFP5408
  tft.setRotation(1); // Need for the Mega, please changed for your choice or rotation initial
  //Pour la carte SD=====================
  //Initialisation de la CARTE SD
  if (!SD.begin(53))// Pin 53 pour Arduino Mega ou Pin 10 pour Arduino Uno
  {
    Serial.println("Initialisation impossible !");
    return;
  }
  Serial.println("Initialisation OK");
  //Fin carte SD==========================

  rtc.begin(); // Lancement de l'horloge.
  if (! rtc.isrunning())
  {
    Serial.println("RTC NOK");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  //Fin code pour init Carte SD

  // Début code init Sensor
  Wire.begin();
  sensor.setTimeout(500);
  if (!sensor.init())
  {
    Serial.println("Failed to detect and initialize sensor!");
    while (1) {}
  }
  Serial.println("Initialisation OK Sensor");

#if defined LONG_RANGE
  // lower the return signal rate limit (default is 0.25 MCPS)
  sensor.setSignalRateLimit(0.1);
  // increase laser pulse periods (defaults are 14 and 10 PCLKs)
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
#endif

#if defined HIGH_SPEED
  // reduce timing budget to 20 ms (default is about 33 ms)
  sensor.setMeasurementTimingBudget(20000);
#elif defined HIGH_ACCURACY
  // increase timing budget to 200 ms
  sensor.setMeasurementTimingBudget(200000);
#endif
  //fin presence

  Wire.begin(0x12); // join i2c bus (address optional for master)
  Wire.begin(0x13); // join i2c bus (address optional for master)
  Serial.begin(9600); // join i2c bus (address optional for master)
  txbuf[0] =  (MEASURE_MODE_PASSIVE | MEASURE_RANG_150);//the measurement mode is set to passive mode, measurement range is set to 500CM.
  i2cWriteBytes(addr0, CFG_INDEX , &txbuf[0], 1 );//
  delay(100);
  txbuf[0] =  (MEASURE_MODE_PASSIVE | MEASURE_RANG_150);//the measurement mode is set to passive mode, measurement range is set to 500CM.
  i2cWriteBytes(addr1, CFG_INDEX , &txbuf[0], 1 );//
  delay(100);
  txbuf[0] =  (MEASURE_MODE_PASSIVE | MEASURE_RANG_150);//the measurement mode is set to passive mode, measurement range is set to 500CM.
  i2cWriteBytes(addr2, CFG_INDEX , &txbuf[0], 1 );//
  delay(100);
}


//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//PARTIE CAPTEUR

//premier capteur

void i2cWriteBytes(unsigned char addr_t, unsigned char Reg , unsigned char *pdata, unsigned char datalen )
{
  Wire.beginTransmission(addr_t); // transmit to device #8
  Wire.write(Reg);              // sends one byte

  for (uint8_t i = 0; i < datalen; i++) {
    Wire.write(*pdata);
    pdata++;
  }

  Wire.endTransmission();    // stop transmitting
}

void i2cReadBytes(unsigned char addr_t, unsigned char Reg , unsigned char Num )
{
  unsigned char i = 0;
  Wire.beginTransmission(addr_t); // transmit to device #8
  Wire.write(Reg);              // sends one byte
  Wire.endTransmission();    // stop transmitting
  Wire.requestFrom(addr_t, Num);
  while (Wire.available())   // slave may send less than requested
  {
    rxbuf[i] = Wire.read();
    i++;
  }

}

//deuxième capteurs
void i2cWriteBytes0(unsigned char addr_c, unsigned char Reg , unsigned char *pdata0, unsigned char datalen0 )
{
  Wire.beginTransmission(addr_c); // transmit to device #8
  Wire.write(Reg);              // sends one byte

  for (uint8_t i0 = 0; i0 < datalen0; i0++) {
    Wire.write(*pdata0);
    pdata0++;
  }

  Wire.endTransmission();    // stop transmitting
}

void i2cReadBytes0(unsigned char addr_c, unsigned char Reg , unsigned char Num )
{
  unsigned char i0 = 0;
  Wire.beginTransmission(addr_c); // transmit to device #8
  Wire.write(Reg);              // sends one byte
  Wire.endTransmission();    // stop transmitting
  Wire.requestFrom(addr_c, Num);
  while (Wire.available())   // slave may send less than requested
  {
    rxbuf[i0] = Wire.read();
    i0++;
  }

}

// troisieme
void i2cWriteBytes1(unsigned char addr_p, unsigned char Reg , unsigned char *pdata1, unsigned char datalen1 )
{
  Wire.beginTransmission(addr_p); // transmit to device #8
  Wire.write(Reg);              // sends one byte

  for (uint8_t i1 = 0; i1 < datalen1; i1++) {
    Wire.write(*pdata1);
    pdata1++;
  }

  Wire.endTransmission();    // stop transmitting
}

void i2cReadBytes1(unsigned char addr_p, unsigned char Reg , unsigned char Num )
{
  unsigned char i1 = 0;
  Wire.beginTransmission(addr_p); // transmit to device #8
  Wire.write(Reg);              // sends one byte
  Wire.endTransmission();    // stop transmitting
  Wire.requestFrom(addr_p, Num);
  while (Wire.available())   // slave may send less than requested
  {
    rxbuf[i1] = Wire.read();
    i1++;
  }
  Serial.println("Initialisation OK Setup");
}


void loop()
{

  int16_t  dist, temp;
  txbuf[0] = CMD_DISTANCE_MEASURE;
  i2cWriteBytes(addr0, CMD_INDEX , &txbuf[0], 1 );//write register, send ranging command
  //delay(800);
  i2cReadBytes(addr0, DIST_H_INDEX , 2 );//read distance register
  dist = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];

  Longueur = dist - but1;

  //deuxième
  i2cWriteBytes(addr1, CMD_INDEX , &txbuf[0], 1 );//write register, send ranging command
  //delay(800);
  i2cReadBytes(addr1, DIST_H_INDEX , 2 );//read distance register
  dist = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];

  Largeur = dist - but2;

  //troisième
  i2cWriteBytes(addr2, CMD_INDEX , &txbuf[0], 1 );//write register, send ranging command
  //delay(800);
  i2cReadBytes(addr2, DIST_H_INDEX , 2 );//read distance register
  dist = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];
  i2cReadBytes(addr2, TEMP_H_INDEX , 2 );//read temperature register
  temp = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];

  Hauteur = dist - but3;

  Serial.println("Initialisation OK Attente Loop");
  //presence
  if (sensor.readRangeSingleMillimeters() < 80)
  {
    presence = 1;
    Serial.println("Initialisation OK presence");
    stockage();
  }
  else
  {
    presence = 0;
    Serial.println("Initialisation NOK presence");
  }
  delay(2000);

  Serial.println("Initialisation LANCEMENT OK");

}


/////////////////////////// CODE STOCKAGE
void stockage()
{
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
  text();
}

//Fonction qui écrit la date et l'heure dans le fichierSD
void maintenant()
{
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



////////////PARTIE AFFICHEUR
unsigned long text()
{
  //rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  DateTime now = rtc.now();
  tft.setCursor(100, 25);
  tft.fillScreen(BLACK);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print("Longueur : ");
  tft.print(Longueur);
  tft.println(" cm");
  tft.setCursor(110, 75);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print("Largeur : ");
  tft.print(Largeur);
  tft.println(" cm");
  tft.setCursor(110, 125);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print("Hauteur : ");
  tft.print(Hauteur);
  tft.println(" cm");
  tft.setCursor(90, 200);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print(now.year(), DEC);
  tft.print('/');
  tft.print(now.month(), DEC);
  tft.print('/');
  tft.println(now.day(), DEC);
  tft.setCursor(70, 250);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print(now.hour(), DEC);
  tft.print(':');
  tft.print(now.minute(), DEC);
  tft.print(':');
  tft.println(now.second(), DEC);
}
