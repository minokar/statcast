# Reads the screen and returns relevant data.

import pyautogui
from PIL import Image
from enum import Enum
from mode import Mode

class ScreenReader():

    _, screen_height = pyautogui.size()

    def __init__(self, pixel_value_to_mode_dict, mss):
        self.pixel_value_to_mode_dict = pixel_value_to_mode_dict
        self.mss = mss


    def _extract_mode(self, mode_pixel_val):
        if mode_pixel_val in self.pixel_value_to_mode_dict.keys():
            return self.pixel_value_to_mode_dict[mode_pixel_val]

        return Mode.UNKNOWN
        
    # Returns (mode, pixel_value) tuple.
    def read_values(self):
        # We capture a vertical slice of the left-hand side of the screen.
        # This allows us to capture both the top-left and bottom-left pixels
        rect = {"left": 0, "top": 0, "width": 1, "height": self.screen_height}

        screenshot = self.mss.grab(rect)
        mode, stat_value = self._extract_mode(screenshot.pixel(0,0)[0]), screenshot.pixel(0, screenshot.height - 1)[0]
        return mode, stat_value
        
