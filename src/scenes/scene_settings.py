import pygame as pg
from src.settings import SETTINGS

class SettingsScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("Consolas", 28)
        self.message = "Settings (stub)"

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((20, 25, 35))
        label = self.font.render(self.message, True, (200,200,255))
        self.screen.blit(label, (100, 100))
