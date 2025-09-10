import pygame as pg
from src.player_stats import PLAYER_STATS
from src.levels import LEVELS
from src.master_unlock_grid import MASTER_UNLOCK_GRID

class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.SysFont("Consolas", 32)
        self.level_index = 0
        self.message = ""

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                self.level_index = (self.level_index + 1) % len(LEVELS)
            if event.key == pg.K_UP:
                self.level_index = (self.level_index - 1) % len(LEVELS)
            if event.key == pg.K_RETURN:
                self.message = f"Selected {LEVELS[self.level_index]['name']}"

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((30, 30, 40))
        y = 50
        stats_text = " | ".join([f"{k}: {v}" for k, v in PLAYER_STATS.items()])
        self.screen.blit(self.font.render(stats_text, True, (180,220,180)), (20, y))
        y += 60
        self.screen.blit(self.font.render("Levels:", True, (200,200,220)), (20, y))
        y += 40
        for i, lvl in enumerate(LEVELS):
            col = (255,220,120) if i == self.level_index else (200,200,200)
            label = self.font.render(f"{lvl['id']} - {lvl['name']}", True, col)
            self.screen.blit(label, (40, y))
            y += 40
        y += 40
        self.screen.blit(self.font.render("Unlocked Features:", True, (200,220,200)), (20, y))
        y += 40
        for unlock in MASTER_UNLOCK_GRID:
            if unlock.get("unlocked"):
                label = self.font.render(f"{unlock['unlock']} - {unlock['reward']}", True, (160,255,160))
                self.screen.blit(label, (40, y))
                y += 36
        if self.message:
            msg_label = self.font.render(self.message, True, (255,100,100))
            self.screen.blit(msg_label, (20, self.screen.get_height()-60))
