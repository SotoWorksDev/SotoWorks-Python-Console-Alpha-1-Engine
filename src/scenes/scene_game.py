import pygame as pg
from engine.player import Player

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("Consolas", 32)
        self.player = Player(100, 100)

    def handle_event(self, event):
        pass  # We’ll use key states in update

    def update(self, dt):
        keys = pg.key.get_pressed()
        self.player.handle_input(keys, dt)

    def draw(self):
        self.screen.fill((20, 20, 30))
        self.player.draw(self.screen)
        label = self.font.render("Use WASD or arrow keys to move!", True, (255,255,255))
        self.screen.blit(label, (50, 30))
