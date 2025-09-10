# src/entities/npc.py

from .entity import Entity

class NPC(Entity):
    def __init__(self, pos, image=None, dialog=None):
        super().__init__(pos, image, size=(32, 32))
        self.tags.add("npc")
        self.dialog = dialog or []

    def on_interact(self, game=None):
        # Placeholder for dialog or quest logic
        if self.dialog:
            print("NPC says:", self.dialog[0])
