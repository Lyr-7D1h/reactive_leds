import random
from config import Config
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
        self.heat = [0] * 255
        self.cooling = 25

    def update(self):
        # Step 1.  Cool down every cell a little
        for i in range(0, self.config.amount_leds):
            self.heat[i] -= random.randint(
                0, int(((self.cooling * 10) / self.config.amount_leds) + 2)
            )
        # Step 2.  Heat from each cell drifts 'up' and diffuses a little
        for k in range(self.config.amount_leds - 1, 2, -1):
            self.heat[k] = int(
                (self.heat[k - 1] + self.heat[k - 2] + self.heat[k - 2]) / 3
            )
        # Step 3.  Randomly ignite new 'sparks' of heat near the bottom
        # if( random8() < SPARKING ) {
        #   int y = random8(7);
        #   heat[y] = qadd8( heat[y], random8(160,255) );
        # }
        if random.randint(0, 256):
            y = random.randint(0, 7)
            self.heat[y] += random.randint(160, 255)

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
        for j in range(0, self.config.amount_leds):
            color = heatcolor(self.heat[j])
            self.connection.set(j, j + 1, color)
        self.connection.show()
