from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


class ResponseAttackTerritory(BaseModel):
    source_territory_id: int
    target_territory_id: int
    attacking_troops: int

    @model_validator(mode='after')
    def _check_territory_attackable(self: 'ResponseAttackTerritory', info: ValidationInfo) -> 'ResponseAttackTerritory':
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        source_territory_id = self.source_territory_id
        target_territory_id = self.target_territory_id
        attacking_troops = self.attacking_troops

        if not source_territory_id in state.territories:
            raise ValueError(f"No territory exists with territory_id {source_territory_id}.")
        if not target_territory_id in state.territories:
            raise ValueError(f"No territory exists with territory_id {target_territory_id}.")
        if state.territories[source_territory_id].occupier != player:
            raise ValueError(f"You don't occupy this territory.")
        if state.territories[target_territory_id] == player:
            raise ValueError(f"You are attacking your own territory.")
        if not state.territories[target_territory_id].is_adjacent(state.territories[source_territory_id]):
            raise ValueError(f"{target_territory_id} is not adjacent to {source_territory_id}.")
        if attacking_troops < 1:
            raise ValueError(f"You must commit at least 2 troops for the attack.")
        if attacking_troops > 3:
            raise ValueError(f"You cannot commit more than 3 troops for the attack.")
        if state.territores[source_territory_id].troops < attacking_troops \
            or state.territores[source_territory_id].troops - attacking_troops < 1:
            raise ValueError(f"You do not have enough troops to make this attack.")
        
        return self