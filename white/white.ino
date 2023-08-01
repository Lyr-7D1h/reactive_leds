#include <FastLED.h>

#define LED_PIN     7
#define LED_TYPE    WS2812
#define NUM_LEDS    60

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, LED_PIN, GRB>(leds, NUM_LEDS);

  for (int i = 0; i <= NUM_LEDS - 1; i++) {
    leds[i] = CRGB (20,20,20);
  }

  // Disable broken leds
  leds[25] = CRGB (0,0,0);

  FastLED.show();
}

void loop() {
}
