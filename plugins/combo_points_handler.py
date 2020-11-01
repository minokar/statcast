from lifxlan import RED
import time
from color import adjust_brightness

# Sets the zones in a multizone light according to how 
# many combo points the player has. Pulses at max 
# combo points.
class ComboPointsHandler():

    # More work necessary to support this being flexible.
    # Perhaps use a fraction instead of an integer.
    MAX_COMBO_POINTS = 5

    current_combo_points = -1

    def __init__(self, light):
        self.light = light
        self.number_of_zones = len(light.get_color_zones())
    
    # How many zones in the multizone light to fill given combo_points points.
    def _get_num_zones_to_fill(self, combo_points):
        return (combo_points * self.number_of_zones) // self.MAX_COMBO_POINTS

    def update(self, pixel_value):
        # The pixel value can go over 5 in edge cases when the user is tabbed out.
        # Cap the value at the max combo points.
        combo_points = min(pixel_value, self.MAX_COMBO_POINTS)
        if (combo_points == self.current_combo_points):
            time.sleep(0.1)
            return

        self.current_combo_points = combo_points
        print("Combo: {}".format(combo_points))

        color = adjust_brightness(RED, combo_points / self.MAX_COMBO_POINTS)
        num_zones_to_fill = self._get_num_zones_to_fill(combo_points)
        if (num_zones_to_fill > 0):
            self.light.set_zone_color(0, num_zones_to_fill - 1, color, rapid = True, apply = False)
        if (combo_points < self.MAX_COMBO_POINTS):
            self.light.set_zone_color(num_zones_to_fill, self.number_of_zones, adjust_brightness(color, 0), rapid = True, apply = True) # Turn off the other lights
        if (combo_points == self.MAX_COMBO_POINTS):
            try:
                self.light.set_color(color)
            except:
                print("Failed to set color. Trying with rapid=True")
                self.light.set_color(color, rapid=True)
            # Max of 20 Hz recommended to LIFX.
            time.sleep(0.05)
            self.light.set_waveform(False, adjust_brightness(color, 0.5), 1000, 100, 1, 1, rapid=True) # period, cycles, duty_cycle, waveform

        time.sleep(0.25)
    
    # When we return to this mode, we want to make sure 
    # we reset the combo points.
    def reset(self):
        self.current_combo_points = -1