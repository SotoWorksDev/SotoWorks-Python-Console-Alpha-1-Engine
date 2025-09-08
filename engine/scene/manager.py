# engine/scene/manager.py

class SceneManager:
    """
    Manages the stack of scenes (screens, states) in the game.
    Handles event dispatch, update, and drawing.
    """
    def __init__(self):
        self.scenes = []

    def push(self, scene):
        self.scenes.append(scene)

    def pop(self):
        if self.scenes:
            return self.scenes.pop()
        return None

    def handle_event(self, event):
        if self.scenes:
            self.scenes[-1].handle_event(event)

    def update(self, dt):
        if self.scenes:
            self.scenes[-1].update(dt)

    def draw(self, surface):
        if self.scenes:
            self.scenes[-1].draw(surface)
