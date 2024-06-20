from typing import Literal, final
from pydantic import ValidationInfo, field_validator

from engine.game.state import State
from engine.records.base_move import BaseMove

@final
class MoveDistributeTroops(BaseMove):
    record_type: Literal["move_distribute_troops"] = "move_distribute_troops"
    distributions: dict[int, int] # territory_id, troop_count

    @field_validator("distributions")
    @classmethod
    def _check_troop_distributions(cls, distributions: dict[int, int], info: ValidationInfo):
        state: State = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        for territory in distributions:
            if not territory in state.territories:
                raise ValueError(f"You tried to distribute troops to a nonexistant territory with id {territory}.")
            
            if state.territories[territory].occupier != player:
                raise ValueError(f"You don't occupy the territory with id {territory}.")  
            
        if sum(distributions.values()) != player.troops:
            raise ValueError(f"You must distribute exactly your remaining {player.troops} troops.")
        
        matching_territories = state.players[player].must_place_territory_bonus
        if len(matching_territories) > 0:
            for territory in matching_territories:
                if distributions[territory] >= 2:
                    break
            else:
                raise ValueError(f"You must distribute your matching territory bonus to a matching territory from your previous card redemption, at least 2 troops must be placed on a matching territory.\n Your matching territories are {matching_territories}.")
            
        return distributions

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:

        player = state.players[self.move_by_player]

        # The player must have placed all their troops.
        player.troops_remaining = 0

        # Reset the matching territories.
        player.must_place_territory_bonus = []

        # Distribute the troops.
        for territory, troops in self.distributions.items():
            state.territories[territory].troops += troops

        raise NotImplementedError

        