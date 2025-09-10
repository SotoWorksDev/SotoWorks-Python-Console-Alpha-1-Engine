import pygame as pg
from src.profiles import list_profiles

class ProfileScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("Consolas", 28)
        self.profiles = list_profiles()
        self.profile_index = 0

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.profile_index = (self.profile_index + 1) % len(self.profiles)
            if event.key == pg.K_UP:
                self.profile_index = (self.profile_index - 1) % len(self.profiles)

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((10, 10, 20))
        y = 60
        for i, p in enumerate(self.profiles):
            col = (255,200,100) if i == self.profile_index else (180,180,180)
            label = self.font.render(p, True, col)
            self.screen.blit(label, (60, y))
            y += 40
