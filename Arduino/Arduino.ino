/*
 * LCD
 */
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{
    Serial.begin(115200);
    lcd.begin();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Braille Arduino");
    lcd.setCursor(0, 1);
    lcd.print("kysth0707");
    delay(1000);
    lcd.clear();
}

void loop()
{
    if(Serial.available() >= 40)
    {
        int Datas[16];
        for(int ii = 0; ii < 2; ii++)
        {
            while(Serial.available() < 40)
            {
                delay(1);
            }
            for(int i = 0; i < 8; i++)
            {
                int Num10000 = Serial.read() - '0';
                int Num1000 = Serial.read() - '0';
                int Num100 = Serial.read() - '0';
                int Num10 = Serial.read() - '0';
                int Num1 = Serial.read() - '0';
                
                int Num = Num10000 * 10000 + Num1000 * 1000 + Num100 * 100 + Num10 * 10 + Num1;
                Datas[ii * 8 + i] = Num;
                //Datas[ii * 8 + i + 1] = Num % 256;
            }
        }
        lcd.setCursor(0, 1);
        lcd.print(Datas[0]);

//        if(Datas[y] & (1 << x))
        byte Dots[8] = {0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000};
        for(int y = 0; y < 8; y++)
        {
            for(int x = 0; x < 5; x++)
            {
                if((Datas[y] & 256) & (1 << x))
                {
                    Dots[y] = Dots[y] | (1 << x);
                }
            }
        }
        lcd.createChar(1, Dots);
        lcd.setCursor(0, 0);
        lcd.write(1);
    }
    delay(50);
    
    /*
    if(Serial.available() >= 40)  //최대가 64임
    {
        int Datas[16][16];
        
        for(int y = 0; y < 16; y++)
        {
            for(int x = 0; x < 16; x++)
            {
                Datas[x][y] = Serial.read() - '0';
            }
        }
        
        
        byte a[8] = {0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000,0b00000};
        for(int y = 0; y < 8; y++)
        {
            for(int x = 0; x < 5; x++)
            {
                if(Datas[x][y] == 1)
                {
                    a[y] = a[y] | (1 << x);
                }
            }
        }
        DrawDot(a, 0, 0);
    }
    delay(50);
    */
}
/*
void DrawDot(byte Datas[8], int cursorX, int cursorY)
{
    lcd.createChar(0, Datas);
    lcd.setCursor(cursorX, cursorY);
    lcd.write(0);
}*/



/*
 * RGB Led Matrix
//남땜 떨어져서 진행 불가

#include <Adafruit_NeoPixel.h>

#define Pin 7
#define PixelNum 60
#define Bright 50
//0~255

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(PixelNum, Pin, NEO_GRB + NEO_KHZ800);

int LedPos[PixelNum];
//지그재그로 설정해놔서 새 리스트 생성

void setup(){
    Serial.begin(115200);
    pixels.setBrightness(Bright);
    pixels.begin();
    pixels.show();
    int i = 0;
    for(int y = 0; y < 7; y++)
    {
        for(int x = 0; x < 7; x++)
        {
            if(y % 2 == 0)
            {
                LedPos[i] = (y * 7) + (6 - x);
            }
            else
            {
                LedPos[i] = (y * 7) + x;
            }
            i += 1;
        }
    }
}

void loop(){
//    pixels.setPixelColor(0, 255, 0, 0);
//    pixels.setPixelColor(1, 0, 255, 0);
//    pixels.setPixelColor(2, 0, 0, 255);
    FillAll(pixels.Color(255, 0, 0));
    delay(1000);
    FillAllSlow(pixels.Color(255, 255, 255));
    pixels.show();
    pixels.show();
//    두 번 호출해야 정상 작동
    Serial.println("SHOW");
    delay(1000);
}

void FillAll(uint32_t c)
{
    pixels.clear();
    for(int i = 0; i < PixelNum; i++)
    {
        pixels.setPixelColor(i, c);
    }
    pixels.show();
    pixels.show();
}


void FillAllSlow(uint32_t c)
{
    pixels.clear();
    for(int i = 0; i < PixelNum; i++)
    {
        pixels.setPixelColor(LedPos[i], c);
        pixels.show();
        pixels.show();
        delay(200);
    }
}
*/
