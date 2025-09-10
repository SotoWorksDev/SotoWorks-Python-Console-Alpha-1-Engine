class GameState:
    def __init__(self):
        self.running = True
        self.score = 0
        self.level = 1
        # Add more global game variables here

    def reset(self):
        self.score = 0
        self.level = 1
        # Reset any other state here
