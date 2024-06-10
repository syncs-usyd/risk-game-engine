
class PlayerState:
    def __init__(self, player_num, state):
        self.player_num = player_num
        self.state = state
        self.terriorties = []
    
    def add_territory(self, territory):
        self.terriorties.append(territory)