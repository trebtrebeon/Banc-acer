///////////////////////////////////////////////////////////////////////////////////////////
#include <SPFD5408_Adafruit_GFX.h>    // Core graphics library
#include <SPFD5408_Adafruit_TFTLCD.h> // Hardware-specific library
#include <SPFD5408_TouchScreen.h>
#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0
#define LCD_RESET A4 // Can alternately just connect to Arduino's reset pin
#define  BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);
///////////////////////////////////////////////////////////////////////////////////////////
#include <Wire.h>
unsigned char txbuf[10] = {0};
unsigned char rxbuf[10] = {0};
int i2cWriteBytes2 = 0;
int toto1 = 0;
int toto2 = 0;
int toto3 = 0;
unsigned char i = 0, x = 0;
typedef enum
{
  SLAVEADDR_INDEX = 0,
  PID_INDEX,
  VERSION_INDEX ,
  DIST_H_INDEX,
  DIST_L_INDEX,
  TEMP_H_INDEX,
  TEMP_L_INDEX,
  CFG_INDEX,
  CMD_INDEX,
  REG_NUM
} regindexTypedef;
#define    MEASURE_MODE_PASSIVE    (0x00)
#define    MEASURE_RANG_150      (0x00)
#define    CMD_DISTANCE_MEASURE    (0x01)

unsigned char addr0 = 0x12;
unsigned char addr1 = 0x13;
unsigned char addr2 = 0x11;
unsigned char n = 0;
///////////////////////////////////////////////////////////////////////////////////////////

void setup()
{
  Serial.begin(9600);
  tft.reset();
  tft.begin(0x9341); // SDFP5408
  tft.setRotation(0); // Need for the Mega, please changed for your choice or rotation initial

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

}

void loop()
{
  int16_t  dist, temp;
  txbuf[0] = CMD_DISTANCE_MEASURE;
  i2cWriteBytes(addr0, CMD_INDEX , &txbuf[0], 1 );//write register, send ranging command
  //delay(800);
  i2cReadBytes(addr0, DIST_H_INDEX , 2 );//read distance register
  dist = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];

  toto1 = dist;
  //Serial.print(toto1, DEC);
  //Serial.print("cm premier");
  //Serial.println();

  //deuxième
  i2cWriteBytes(addr1, CMD_INDEX , &txbuf[0], 1 );//write register, send ranging command
  //delay(800);
  i2cReadBytes(addr1, DIST_H_INDEX , 2 );//read distance register
  dist = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];

  toto2 = dist;
  //Serial.print(toto2, DEC);
  //Serial.print("cm deuxième");
  //Serial.println();

  //troisième
  i2cWriteBytes(addr2, CMD_INDEX , &txbuf[0], 1 );//write register, send ranging command
  //delay(800);
  i2cReadBytes(addr2, DIST_H_INDEX , 2 );//read distance register
  dist = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];
  i2cReadBytes(addr2, TEMP_H_INDEX , 2 );//read temperature register
  temp = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];

  toto3 = dist;
  if (toto3 > 38 and toto3 < 60)
  {
    toto3 = toto3 + 0;
  }
  //Serial.print(toto1, DEC);
  //Serial.print("cm troisième");
  //Serial.println();

  delay(2000);

  tft.setRotation(1);
  text();
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//PARTIE AFFICHEUR
unsigned long text()
{
  tft.setCursor(100, 25);
  tft.fillScreen(BLACK);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print("Longueur : ");
  tft.print(toto1);
  tft.println(" cm");
  tft.setCursor(110, 75);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print("Largeur : ");
  tft.print(toto2);
  tft.println(" cm");
  tft.setCursor(110, 125);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.print("Hauteur : ");
  tft.print(toto3);
  tft.println(" cm");
  tft.setCursor(90, 200);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.println("Date : 14/01/2000");
  tft.setCursor(70, 250);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.println("Heure : 11 h 00 min");
}
