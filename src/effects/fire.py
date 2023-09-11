import random
import time
from effects.base import BaseEffect


def scale_video(i: int, min: int, max: int, nmin: int, nmax: int) -> int:
    return (int((i - min) / max - min) * (nmin - nmax)) + nmin


def heatcolor(temperature: int) -> tuple[int, int, int]:
    heatcolor = (0, 0, 0)

    t192 = scale_video(temperature, 0, 255, 1, 191)
    heatramp = t192 & 0x3F
    heatramp <<= 2

    if t192 & 0x80:
        heatcolor = (255, 255, heatramp)
    elif t192 & 0x40:
        heatcolor = (255, heatramp, 0)
    else:
        heatcolor = (heatramp, 0, 0)
    return heatcolor


"""https://fastled.io/docs/_fire2012_8ino-example.html"""


class Fire(BaseEffect):
    def init(self):
        self.heat_map = [0] * self.config.amount_leds
        self.cooling = 25

    def update(self):
        time.sleep(0.1)
        # Step 1.  Cool down every cell a little
        for i in range(0, self.config.amount_leds):
            self.heat_map[i] -= random.randint(
                0, int(((self.cooling * 10) / self.config.amount_leds) + 2)
            )
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(self.config.amount_leds - 1, 2, -1):
            self.heat_map[k] = int(
                (self.heat_map[k - 1] + self.heat_map[k - 2] + self.heat_map[k - 2]) / 3
            )
        # Step 3.  Randomly ignite new 'sparks' of heat near the bottom
        # if( random8() < SPARKING ) {
        #   int y = random8(7);
        #   heat[y] = qadd8( heat[y], random8(160,255) );
        # }
        if random.randint(0, 256):
            y = random.randint(0, 7)
            self.heat_map[y] += random.randint(160, 255)

        # Step 4.  Map from heat cells to LED colors
        # for( int j = 0; j < NUM_LEDS; j++) {
        #   CRGB color = HeatColor( heat[j]);
        #   int pixelnumber;
        #   if( gReverseDirection ) {
        #     pixelnumber = (NUM_LEDS-1) - j;
        #   } else {
        #     pixelnumber = j;
        #   }
        #   leds[pixelnumber] = color;
        # }
        color_data = [
            heatcolor(self.heat_map[j]) for j in range(0, self.config.amount_leds)
        ]
        self.connection.write(color_data)
