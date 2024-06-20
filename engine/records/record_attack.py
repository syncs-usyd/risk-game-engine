import random
from typing import Literal, cast, final
from engine.game.state import State
from engine.records.base_record import BaseRecord
from engine.records.moves.move_attack import MoveAttack
from engine.records.moves.move_defend import MoveDefend
from engine.records.record_player_eliminated import RecordPlayerEliminated
from engine.records.record_territory_conquered import RecordTerritoryConquered

@final
class RecordAttack(BaseRecord):
    record_type: Literal["record_attack"] = "record_attack"
    move_attack: int
    move_defend: int
    attacking_troops_lost: int
    defending_troops_lost: int
    territory_conquered: bool
    defender_eliminated: bool

    @classmethod
    def factory(cls, state: State, move_attack: int, move_defend: int) -> 'RecordAttack':

        move_attack_obj = cast(MoveAttack, state.match_history[move_attack])
        if move_attack_obj.move == "pass":
            raise RuntimeError("Tried to record an attack relying on a move attack that was a pass.")

        attacking_troops = move_attack_obj.move.attacking_troops
        
        move_defend_obj = cast(MoveDefend, state.match_history[move_defend])
        defending_troops = move_defend_obj.defending_troops

        def roll():
            return random.randint(1, 6)
        
        attacking_rolls = sorted([roll() for _ in range(attacking_troops)])
        defending_rolls = sorted([roll() for _ in range(defending_troops)])

        battles_won_by_attacker = [attacking_rolls.pop(-1) > defending_rolls.pop(-1) for _ in range(min(attacking_troops, defending_troops))]
        attacking_troops_lost = battles_won_by_attacker.count(False)
        defending_troops_lost = battles_won_by_attacker.count(True)

        defending_territory = state.territories[move_attack_obj.move.defending_territory]
        territory_conquered = defending_troops_lost == defending_territory.troops

        defender_eliminated = territory_conquered and len(list(filter(lambda x: x.occupier == move_defend_obj.move_by_player, state.territories.values()))) == 1

        return cls(move_attack=move_attack, move_defend=move_defend, attacking_troops_lost=attacking_troops_lost, defending_troops_lost=defending_troops_lost, territory_conquered=territory_conquered, defender_eliminated=defender_eliminated)

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        state.match_history.append(self)
        record_attack = len(state.match_history) - 1

        move_attack_obj = cast(MoveAttack, state.match_history[self.move_attack])
        move_defend_obj = cast(MoveDefend, state.match_history[self.move_defend])

        if move_attack_obj.move == "pass":
            raise RuntimeError("Tried to commit record attack for move attack that was a pass.")
        attacking_territory = move_attack_obj.move.attacking_territory
        defending_territory = move_attack_obj.move.defending_territory

        state.territories[attacking_territory].troops -= self.attacking_troops_lost
        state.territories[defending_territory].troops -= self.defending_troops_lost
