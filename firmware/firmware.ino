// Simple led controller program that understands commands over serial
#include <FastLED.h>

#define LED_PIN     18
#define LED_TYPE    WS2812

int num_leds=0;

void setup() {
  Serial.begin(115200);
}

// Thread and use
void error(String message) {
  Serial.println(message);
  delay(100);                      
}

void init_leds(int num_leds) {
  CRGB leds[num_leds];
  FastLED.addLeds<LED_TYPE, LED_PIN, GRB>(leds, num_leds);
  for (int i = 0; i < num_leds; i++) {
    leds[i] = CRGB ( 10,10,10 );
  }
  Serial.write(0x1)
  FastLED.show();
  // TODO response okay
}

bool initialized = false;
void loop() {
  if (Serial.available() > 0) {
    byte command = Serial.read();
    Serial.println(command);

    if (command & 1<<8) {
      Serial.println("INIT");
      int num_leds = command << 7;
      num_leds |= Serial.read();
      Serial.println(+num_leds);
      init_leds(num_leds);
      initialized = true;
      return;
    }

    // byte buff[num_leds * 3];

    // size_t n = Serial.readBytes(buff, NUM_LEDS * 3);
    
    // if (n != NUM_LEDS * 3) {
    //   error("Read incorrect amount of bytes");
    //   return;
    // }

    // for (int i=0; i < NUM_LEDS; i++) {
    //   bool found = false;

    //   if (!found) {
    //     leds[i] = CRGB(buff[i*3],buff[i*3 + 1],buff[i*3 + 2]);
    //   }
    // }

    // FastLED.show();
  }
}
