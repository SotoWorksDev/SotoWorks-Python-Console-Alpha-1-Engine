# src/scene_basic.py

import pygame as pg

class BasicScene:
    """
    A simple example scene for Sotoworks Alpha 1.
    Override handle_event, update, and draw for your game logic.
    """
    def __init__(self):
        self.bg_color = (30, 30, 40)
        self.message = "Hello, Sotoworks!"
        self.font = pg.font.SysFont('Consolas', 32)

    def handle_event(self, event):
        # Example: Exit on Escape key
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            import sys
            sys.exit()

    def update(self, dt):
        # Update logic (animations, timers, etc)
        pass

    def draw(self, surface):
        surface.fill(self.bg_color)
        text = self.font.render(self.message, True, (180, 220, 255))
        rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, rect)
