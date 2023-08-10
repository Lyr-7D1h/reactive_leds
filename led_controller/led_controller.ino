// Simple led controller program that understands commands
#include <FastLED.h>

#define LED_PIN     7
#define LED_TYPE    WS2812
#define NUM_LEDS    60

CRGB leds[NUM_LEDS];

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  
  FastLED.addLeds<LED_TYPE, LED_PIN, GRB>(leds, NUM_LEDS);
  for (int i = 0; i <= NUM_LEDS - 1; i++) {
    leds[i] = CRGB ( 10, 10, 10);
  }

  // Disable broken leds
  leds[25] = CRGB (0,0,0);
  leds[1] = CRGB (0,0,0);

  FastLED.show();
}

// Thread and use
void error_indicator() {
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(100);                      
  digitalWrite(LED_BUILTIN, LOW);   
}

void loop() {
  if (Serial.available()) {
    byte buff[5];
    size_t n = Serial.readBytes(buff, 5);
    
    if (n != 5) {
      error_indicator();
      return;
    }

    if (buff[0] == 255 || buff[1] == 255) {
      FastLED.show();
      return;
    }

    if (buff[0] > buff[1]) {
      error_indicator();
      return;
    }

    // Serial.print(+buff[0]);
    // Serial.print(" ")
    // Serial.print(+buff[1]);
    // Serial.println();

    for (int i=buff[0]; i < buff[1]; i++) {
      // Serial.println(i);
      if (i == 25 || i == 1) {
        continue;
      }
      leds[i] = CRGB(buff[2],buff[3],buff[4]);
    }
  }
}
