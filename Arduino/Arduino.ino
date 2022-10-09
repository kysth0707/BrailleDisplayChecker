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

