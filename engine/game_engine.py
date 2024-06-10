

class GameEngine:
    def __init__(self):
        self.state = GameState()
        self.log   = GameLog(self.state)