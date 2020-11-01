# Reads the screen and returns relevant data.

import pyautogui
import Quartz.CoreGraphics as CG
import Quartz
from PIL import Image
from enum import Enum
from mode import Mode

class ScreenReader():

    _, screen_height = pyautogui.size()

    def __init__(self, pixel_value_to_mode_dict):
        self.pixel_value_to_mode_dict = pixel_value_to_mode_dict

    def _extract_mode(self, mode_pixel_val):
        if mode_pixel_val in self.pixel_value_to_mode_dict.keys():
            return self.pixel_value_to_mode_dict[mode_pixel_val]

        return Mode.UNKNOWN
        
    # Returns (mode, pixel_value) tuple.
    def read_values(self):
        # We capture a vertical slice of the left-hand side of the screen.
        # This allows us to capture both the top-left and bottom-left pixels
        cgimg = CG.CGWindowListCreateImage(
                CG.CGRectMake(0, 0, 1, self.screen_height),
                CG.kCGWindowListOptionOnScreenOnly,
                CG.kCGNullWindowID,
                CG.kCGWindowImageDefault)
        width = Quartz.CGImageGetWidth(cgimg)
        height = Quartz.CGImageGetHeight(cgimg)
        pixeldata = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(cgimg))
        bpr = Quartz.CGImageGetBytesPerRow(cgimg)
        pilimage = Image.frombuffer("RGBA", (width, height), pixeldata, "raw", "BGRA", bpr, 1)
        return self._extract_mode(pilimage.getpixel((0,0))[0]), pilimage.getpixel((0, pilimage.size[1] - 1))[0]
        