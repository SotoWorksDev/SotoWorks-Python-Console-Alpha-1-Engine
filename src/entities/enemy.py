# src/entities/enemy.py

import pygame
from .entity import Entity

class Enemy(Entity):
    def __init__(self, pos, image=None):
        super().__init__(pos, image, size=(32, 32))
        self.tags.add("enemy")
        self.speed = 80
        self.health = 50
        self.damage = 10  # if collides with player

    def update(self, dt, game=None):
        # Example: simple AI to move toward player
        if game and hasattr(game, "player"):
            to_player = game.player.pos - self.pos
            dist = to_player.length()
            if dist > 1:
                self.vel = to_player.normalize() * self.speed
            else:
                self.vel = pygame.Vector2()
        super().update(dt, game)

    def on_collide(self, other, game=None):
        # Example: die on bullet, hurt player, etc.
        if getattr(other, "tags", None) and "player" in other.tags:
            other.health -= self.damage
        if getattr(other, "tags", None) and "bullet" in other.tags:
            self.health -= other.damage
            if self.health <= 0:
                self.kill()
