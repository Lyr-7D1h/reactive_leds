import random
from config import Config
from effects.base import BaseEffect


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
        # Step 4.  Map from heat cells to LED colors
