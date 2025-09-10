import pygame as pg

class Player:
    def __init__(self, x, y, speed=200):
        self.x = x
        self.y = y
        self.speed = speed  # pixels per second
        self.size = 40  # player square size

    def handle_input(self, keys, dt):
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.y -= self.speed * dt
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            self.y += self.speed * dt
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.x -= self.speed * dt
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.x += self.speed * dt

    def draw(self, screen):
        rect = pg.Rect(int(self.x), int(self.y), self.size, self.size)
        pg.draw.rect(screen, (80, 200, 255), rect)
