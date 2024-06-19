from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


class MoveAttack(BaseModel):
    attacking_territory: int
    defending_territory: int
    attacking_troops: int

    @model_validator(mode='after')
    def _check_valid_attack(self: 'MoveAttack', info: ValidationInfo) -> 'MoveAttack':
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        attacking_territory = self.attacking_territory
        defending_territory = self.defending_territory
        attacking_troops = self.attacking_troops

        if not attacking_territory in state.territories:
            raise ValueError(f"No territory exists with territory_id {attacking_territory}.")
        
        if not defending_territory in state.territories:
            raise ValueError(f"No territory exists with territory_id {defending_territory}.")
        
        if state.territories[attacking_territory].occupier != player:
            raise ValueError(f"You don't occupy this territory.")
        
        if state.territories[defending_territory] == player:
            raise ValueError(f"You are attacking your own territory.")
        
        if not state.territories[defending_territory].is_adjacent(state.territories[attacking_territory]):
            raise ValueError(f"{defending_territory} is not adjacent to {attacking_territory}.")
        
        if not 1 <= attacking_troops <= 3:
            raise ValueError(f"You must commit between 1 and 3 troops for the attack, you committed {attacking_troops}.")
        
        if attacking_troops > state.territories[attacking_territory].troops - 1:
            raise ValueError(f"You do not have enough troops, you tried to commit {attacking_territory} troops but only have {state.territories[attacking_territory].troops}. Remember 1 troop must remain on the attacking territory.")
        
        return self