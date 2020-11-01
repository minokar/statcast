from lifxlan import YELLOW
import time
from color import adjust_brightness

# Sets the color to yellow and adjusts the brightness
# based on the player's energy.
class EnergyHandler():

    current_energy = -1

    def __init__(self, light):
        self.light = light

    def update(self, pixel_value):
        energy_fraction = pixel_value / 255.0
        print("Energy: {:.2f}".format(energy_fraction))
        if (energy_fraction != self.current_energy):
            self.light.set_color(adjust_brightness(YELLOW, energy_fraction), rapid = True)
            self.current_energy = energy_fraction
        time.sleep(0.1)
    
    def reset(self):
        self.current_energy = -1