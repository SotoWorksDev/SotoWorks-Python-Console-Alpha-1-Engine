import pygame as pg
from src.codex import CODEX_ENTRIES

class CodexScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("Consolas", 28)
        self.entry_index = 0

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.entry_index = (self.entry_index + 1) % len(CODEX_ENTRIES)
            if event.key == pg.K_UP:
                self.entry_index = (self.entry_index - 1) % len(CODEX_ENTRIES)

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((0, 0, 30))
        y = 40
        for i, entry in enumerate(CODEX_ENTRIES):
            if entry["unlocked"]:
                col = (180,250,120) if i == self.entry_index else (120,180,120)
                label = self.font.render(f"{entry['title']}", True, col)
                self.screen.blit(label, (40, y))
                y += 36
