from engine.config.gameconfig import NUM_PLAYERS
from engine.state.playerstate import PlayerState

class GameState:
    def __init__(self):
        self.players = [PlayerState(i, self) for i in range(NUM_PLAYERS)]
        self.curr_player = 0
        self.map = init_map(players)

    def start_new_round(self):
        self.players[self.curr_player].start_new_round()
        self.curr_player = (self.curr_player + 1) % NUM_PLAYERS
    
