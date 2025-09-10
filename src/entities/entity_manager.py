# src/entities/entity_manager.py

class EntityManager:
    def __init__(self):
        self.entities = []
        self.to_add = []
        self.to_remove = set()

    def add(self, entity):
        """Queue an entity to be added on the next update (avoids modifying list during iteration)."""
        self.to_add.append(entity)

    def remove(self, entity):
        """Queue an entity for removal."""
        self.to_remove.add(entity)

    def update(self, dt, game=None):
        # Add and remove entities safely
        for entity in self.to_add:
            self.entities.append(entity)
        self.to_add.clear()

        self.entities = [e for e in self.entities if e not in self.to_remove and e.alive]
        self.to_remove.clear()

        # Update all entities
        for entity in self.entities:
            entity.update(dt, game)

    def draw(self, surf, camera=(0,0)):
        for entity in self.entities:
            entity.draw(surf, camera)

    def get_by_tag(self, tag):
        """Yield all entities with a given tag."""
        return (e for e in self.entities if tag in getattr(e, "tags", set()))

    def clear(self):
        self.entities.clear()
        self.to_add.clear()
        self.to_remove.clear()

    def handle_collisions(self, group1=None, group2=None):
        """
        Check collisions between two groups (by tag).
        If group2 is None, check all-vs-all (not recommended for lots of entities).
        Calls on_collide(other, game) for each collision.
        """
        if group1 is None:
            group1 = self.entities
        else:
            group1 = list(self.get_by_tag(group1))

        if group2 is None:
            group2 = self.entities
        else:
            group2 = list(self.get_by_tag(group2))

        for a in group1:
            for b in group2:
                if a is b:
                    continue
                if hasattr(a, "rect") and hasattr(b, "rect"):
                    if a.rect.colliderect(b.rect):
                        a.on_collide(b)
                        b.on_collide(a)
