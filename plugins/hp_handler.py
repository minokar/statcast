from lifxlan import GREEN, YELLOW, RED, BLUE
import time
from color import interpolate, adjust_brightness

# Interpolates the light between red -> yellow -> green
# based on the player's health. Turns blue on death.
class HpHandler():

    current_hp = -1

    def __init__(self, light):
        self.light = light

    def update(self, pixel_value):
        hp_fraction = pixel_value / 255.0
        if (hp_fraction == self.current_hp):
            time.sleep(0.25)
            return
            
        if (hp_fraction > 0.5):
            color = interpolate(YELLOW, GREEN, (hp_fraction - 0.5) / 0.5)
        elif (hp_fraction > 0.001):
            color = interpolate(RED, YELLOW, hp_fraction / 0.5)
            print(color)
        else:
            color = BLUE

        # Experimenting with setting the light three times for
        # reliability.
        for i in range(3):
            self.light.set_color(adjust_brightness(color, 1), rapid=True)

            # Max 20 Hz recommended by LIFX
            time.sleep(0.05)
        print("HP: {:.2f}".format(hp_fraction))
        self.current_hp = hp_fraction
    
    # When we return to this mode, we want to make sure 
    # we reset the HP.
    def reset(self):
        self.current_hp = -1