import pygame as pg

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("Consolas", 32)
        self.message = "Game Scene (stub)"

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((20, 20, 30))
        label = self.font.render(self.message, True, (255,255,255))
        self.screen.blit(label, (100, 100))
