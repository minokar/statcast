
import time

SLEEP_FOR_UNKNOWN_MODE = 0.5

class StatcastRunner():

    previous_mode = None

    # Plugins is a map from mode to a handler implementation.
    # Each handler must implement an update() and reset() method.
    def __init__(self, light, screen_reader, plugins): 
        self.light = light
        self.screen_reader = screen_reader
        self.plugins = plugins
    
    def run(self):
        while(True):
            current_mode, pixel_value = self.screen_reader.read_values()
            
            if current_mode not in self.plugins.keys():
                time.sleep(SLEEP_FOR_UNKNOWN_MODE)
                continue
            
            plugin = self.plugins[current_mode]
            if current_mode != self.previous_mode:
                plugin.reset()
                self.previous_mode = current_mode
            
            plugin.update(pixel_value)
