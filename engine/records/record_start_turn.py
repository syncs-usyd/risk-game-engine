from typing import Literal, final
from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordStartTurn(BaseRecord):
    record_type: Literal["record_start_turn"] = "record_start_turn"
    player: int
    continents_held: list[int]
    territories_held: int
    continent_bonus: int
    territory_bonus: int

    @classmethod
    def factory(cls, state: State, player: int) -> 'RecordStartTurn':
        player_territories = [territory_id for territory_id, territory in state.territories.items() if territory.occupier == player]
        territory_bonus = max(3, len(player_territories) // 3)

        continents_held = []
        continent_bonus = 0
        for continent, territories in state.map.get_continents().items():
            if all(territory_id in player_territories for territory_id in territories):
                continents_held.append(continent)
                continent_bonus += state.map.get_continent_bonus(continent)

        return cls(player=player, continents_held=continents_held, territories_held=len(player_territories), continent_bonus=continent_bonus, territory_bonus=territory_bonus)

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        state.match_history.append(self)

        state.players[self.player].troops_remaining += self.territory_bonus + self.continent_bonus
