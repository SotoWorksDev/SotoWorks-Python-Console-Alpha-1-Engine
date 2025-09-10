# src/entities/player.py

import pygame
from .entity import Entity

class Player(Entity):
    def __init__(self, pos, image=None):
        super().__init__(pos, image, size=(32, 32))
        self.tags.add("player")
        self.speed = 120  # pixels/sec
        self.health = 100

    def update(self, dt, game=None):
        # Example: update position using velocity (set externally by input)
        super().update(dt, game)
        # Clamp to map, handle status, etc. here

    def on_collide(self, other, game=None):
        # Example: take damage, pick up item, etc.
        if hasattr(other, "damage"):
            self.health -= other.damage
            if self.health <= 0:
                self.kill()
