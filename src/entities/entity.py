# src/entities/entity.py

import pygame

class Entity:
    def __init__(self, pos, image=None, size=(32, 32)):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.size = size
        self.image = image  # pygame.Surface or None
        self.rect = pygame.Rect(self.pos.x, self.pos.y, *self.size)
        self.alive = True
        self.tags = set()

    def update(self, dt, game=None):
        """Update entity logic. dt = delta time, game = game state/context."""
        self.pos += self.vel * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, surf, camera=(0,0)):
        """Draw the entity. camera = (x, y) offset for scrolling."""
        if self.image:
            surf.blit(self.image, (self.pos.x - camera[0], self.pos.y - camera[1]))
        else:
            pygame.draw.rect(
                surf, (200, 100, 100),
                self.rect.move(-camera[0], -camera[1]), 2
            )

    def on_collide(self, other, game=None):
        """Handle collision with another entity."""
        pass

    def kill(self):
        self.alive = False
