# engine/debug/profiler.py

import pygame as pg

class ProfilerOverlay:
    """
    Draws a simple FPS/time profiler overlay.
    """
    def __init__(self):
        self.fps = 0.0
        self.font = pg.font.SysFont('Consolas', 18)

    def tick(self, dt):
        if dt > 0:
            self.fps = 1.0 / dt

    def draw(self, surface):
        text = f"FPS: {self.fps:.1f}"
        img = self.font.render(text, True, (255,255,0))
        surface.blit(img, (8, 8))
