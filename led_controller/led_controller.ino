#include <FastLED.h>

#define LED_PIN     7
#define LED_TYPE    WS2812
#define NUM_LEDS    60

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  
  FastLED.addLeds<LED_TYPE, LED_PIN, GRB>(leds, NUM_LEDS);
  for (int i = 0; i <= NUM_LEDS - 1; i++) {
    leds[i] = CRGB ( 10, 10, 10);
  }

  // Disable broken leds
  leds[25] = CRGB (0,0,0);
  FastLED.show();
}

void loop() {
  if (Serial.available()) {
    byte buff[4];
    size_t n = Serial.readBytes(buff, 4);

    if (buff[0] == 25) {
      return;
    }
    
    if (buff[0] == 255) {
      FastLED.show();
      return;
    }

    leds[buff[0]] = CRGB(buff[1],buff[2],buff[3]);
  }
}
