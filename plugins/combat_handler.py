from lifxlan import RED
import time
from color import adjust_brightness

# Indicates when the player is in combat by flashing a red light.
class CombatHandler():

    is_in_combat_prev = None

    def __init__(self, light):
        self.light = light

    def update(self, pixel_value):
        is_in_combat = pixel_value == 1
        print("In Combat: {}".format(is_in_combat))
        if (self.is_in_combat_prev == is_in_combat):
            time.sleep(0.1)
            return

        if (is_in_combat):
            self.light.set_color(adjust_brightness(RED, 0.35), rapid=True)
            time.sleep(0.05)
            self.light.set_waveform(False, adjust_brightness(RED, 0.5), 2000, 100, 1, 1, rapid=True) # period, cycles, duty_cycle, waveform
        else:
            self.light.set_color(adjust_brightness(RED, 0), rapid = True, duration=1000)
    
        self.is_in_combat_prev = is_in_combat
        time.sleep(0.5)
        
    
    def reset(self):
        self.is_in_combat_prev = None