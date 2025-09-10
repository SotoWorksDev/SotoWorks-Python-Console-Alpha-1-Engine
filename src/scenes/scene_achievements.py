import pygame as pg
from src.achievements import ACHIEVEMENTS

class AchievementsScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("Consolas", 28)

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((20, 20, 20))
        y = 60
        for ach in ACHIEVEMENTS:
            col = (120,255,120) if ach["unlocked"] else (100,100,100)
            label = self.font.render(f"{ach['desc']}", True, col)
            self.screen.blit(label, (60, y))
            y += 40
