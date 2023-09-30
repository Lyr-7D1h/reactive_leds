// Simple led controller program that understands commands
#include <FastLED.h>

#define LED_PIN     7
#define LED_TYPE    WS2812
#define NUM_LEDS    60

CRGB leds[NUM_LEDS];

// int broken_leds[8] = {0, 1, 8, 12, 14, 15, 20, 25};

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(250000);
  
  FastLED.addLeds<LED_TYPE, LED_PIN, GRB>(leds, NUM_LEDS);
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB ( 0,0,0 );
  }

  FastLED.show();
}

// Thread and use
void error(String message) {
  Serial.println(message);
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(100);                      
  digitalWrite(LED_BUILTIN, LOW);   
}


void loop() {
  // if (Serial.available() > 0) {
  //   byte buff[NUM_LEDS * 3];
  //   // byte buff[5];
  //   // size_t n = Serial.readBytes(buff, 5);
  //   size_t n = Serial.readBytes(buff, NUM_LEDS * 3);
    
  //   Serial.println(+n);
  //   if (n != NUM_LEDS * 3) {
  //     error("Read incorrect amount of bytes");
  //     return;
  //   }


  //   for (int i=0; i < NUM_LEDS; i++) {
  //     bool found = false;

  //     Serial.print(+buff[i*3] );
  //     Serial.print(",");
  //     Serial.print(+buff[i*3 + 1] );
  //     Serial.print(",");
  //     Serial.print(+buff[i*3 +2] );

  //     if (!found) {
  //       leds[i] = CRGB(buff[i*3],buff[i*3 + 1],buff[i*3 + 2]);
  //     }
  //   }
  //   // Serial.println();
  //   // Serial.println();
  //   FastLED.show();
    
    

  //   // if (buff[0] == 255 || buff[1] == 255) {
  //   //   FastLED.show();
  //   //   return;
  //   // }

  //   // Serial.print(+buff[0]);
  //   // Serial.print(" ");
  //   // Serial.print(+buff[1]);
  //   // Serial.println();

  //   // if (buff[0] > buff[1]) {
  //   //   error("Start of led range can't be bigger than end");
  //   //   return;
  //   // }

  //   // for (int i=buff[0]; i < buff[1]; i++) {
  //   //   bool found = false;
  //   //   // TODO optimize
  //   //   for (int led: broken_leds) {
  //   //     if (i == led) {
  //   //       found = true;
  //   //       break;
  //   //     }
  //   //   }

  //   //   if (!found) {
  //   //     leds[i] = CRGB(buff[2],buff[3],buff[4]);
  //   //   }
  //   // }


  // }
}
