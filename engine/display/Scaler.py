# engine/display/scaler.py

import pygame as pg

class Scaler:
    """
    Handles display scaling and window management.
    Converts logical game coordinates to window coordinates and vice versa.
    """
    def __init__(self, config_path):
        # Load scaling settings from config (stub)
        self.logical_width = 480
        self.logical_height = 320
        self.window = None

    def create_window(self):
        self.window = pg.display.set_mode((self.logical_width, self.logical_height), pg.RESIZABLE)
        return self.window

    def on_resize(self, w, h):
        # Handle window resize (stub)
        self.window = pg.display.set_mode((w, h), pg.RESIZABLE)

    def begin(self):
        # Return the surface to draw on
        return self.window

    def end(self):
        # Flip/update the display
        pg.display.flip()

    def window_to_logical(self, pos):
        # Convert window coordinates to logical game coordinates (stub)
        x, y = pos
        # Simple passthrough for now
        return (x, y)
