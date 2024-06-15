from engine.config.gameconfig import NUM_PLAYERS, NUM_STARTING_TROOPS
from engine.game.map import Map
from engine.game.player import Player
from engine.game.territory import Territory
from engine.maps import earth

class State():
    def __init__(self):
        self.map: Map = earth.create_map()
        self.players = dict([(x, Player.factory(player_id=x, initial_troops=NUM_STARTING_TROOPS)) for x in range(NUM_PLAYERS)])
        self.territories: dict[int, Territory] = dict([(x, Territory(territory_id=x, occupier=None, troops=0)) for x in self.map.get_vertices()])
