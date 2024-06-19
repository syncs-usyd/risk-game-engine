import numpy as np

class AttackHelper:
    @staticmethod
    def can_player_attack(player, state):
        for t in list(filter(lambda x: x.occupier == player, state.territories.values())):
            if t.troops > 1 and len(list(filter(lambda x: x.occupier != player, state.map.get_adjacent_to(t)))) > 0:
                return True
        return False

    @staticmethod
    def roll(num_attacking, num_defending):
        return np.sort(np.random.randint(1, 6, size=num_attacking))[:num_defending] \
            > np.sort(np.random.randint(1, 6, size=num_defending))

    @staticmethod
    def 