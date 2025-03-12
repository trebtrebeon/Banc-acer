#include <SPFD5408_Adafruit_GFX.h>
#include <SPFD5408_Adafruit_TFTLCD.h>
#include <SPFD5408_TouchScreen.h>

#define LCD_CS A3
#define LCD_CD A2
#define LCD_WR A1
#define LCD_RD A0

#define LCD_RESET A4

#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

void setup() 
{
  Serial.begin(9600);
  tft.reset();
  tft.begin(0x9341);
  tft.setRotation(0);
}

void loop() 
{
  tft.setRotation(1);
  text();
  delay(9000000);
}

unsigned long text()
{
  tft.setCursor(50, 25);
  tft.fillScreen(BLACK);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.println("Longueur : ");
  tft.println(toto1);
  tft.println(" cm");
  tft.setCursor(60, 75);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.println("Largeur : ");
  tft.println(toto2);
  tft.println(" cm");
  tft.setCursor(60, 125);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.println("Hauteur : xxx,xx cm");
  tft.println(toto3);
  tft.println(" cm");
  tft.setCursor(70, 200);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.println("Date : 14/01/2000");
  tft.setCursor(60, 250);
  tft.setTextSize(3);
  tft.setTextColor(WHITE);
  tft.println("Heure : 11 h 00 min");
}
