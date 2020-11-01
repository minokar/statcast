from lifxlan import RED
import time
from color import adjust_brightness

# Sets the color to red and adjusts the brightness
# based on the player's rage.
class RageHandler():

    current_rage = -1

    def __init__(self, light):
        self.light = light

    def update(self, pixel_value):
        rage_fraction = pixel_value / 255.0
        print("Rage: {:.2f}".format(rage_fraction))

        if (rage_fraction != self.current_rage):
            # Experimenting with setting the light three times for
            # reliability.
            for i in range(3):
                self.light.set_color(adjust_brightness(RED, rage_fraction), rapid = True)
                # Max 20 Hz recommended by LIFX
                time.sleep(0.05)

            self.current_rage = rage_fraction

        time.sleep(0.1)

    
    def reset(self):
        self.current_rage = -1