from typing import Any
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator


class ResponseFortifyTerritory(BaseModel):
    source_territory_id: int
    target_territory_id: int
    troops: int

    @model_validator(mode='before')
    @classmethod
    def _check_values(cls, data: dict, info: ValidationInfo):
        state = info.context['state'] # type: ignore
        player = info.context['player'] # type: ignore
        fields = ['source_territory_id', 'target_territory_id', 'troops']

        if not all(x in fields for x in data):
            raise ValueError(f"Response does not contain all required fields: {fields}.")

        if not all(isinstance(x, int) for x in data.values()):
            raise ValueError(f"At least one field is not of type int: {data.values()}.")

        return data


    @model_validator(mode='after')
    def _check_troops(self, info: ValidationInfo):
        state = info.context['state'] # type: ignore
        player = info.context['player'] # type: ignore

        if not self.source_territory_id in state.territories:
            raise ValueError(f"No territory exists with territory_id {self.source_territory_id}.")

        if not self.target_territory_id in state.territories:
            raise ValueError(f"No territory exists with territory_id {self.target_territory_id}.")
        
        if state.territories[self.source_territory_id].occupier != player:
            raise ValueError(f"You don't occupy the source territory.")

        if state.territories[self.target_territory_id].occupier != player:
            raise ValueError(f"You don't occupy the target territory.")
        
        if not state.map.is_adjacent(self.source_territory_id, self.target_territory_id):
            raise ValueError(f"Target territory {self.target_territory_id} is not adjacent to source territory {self.source_territory_id}.")
        
        if not self.troops in range(state.territories[self.source_territory_id].troops):
            raise ValueError(f"Invalid number of troops moved {self.troops}.This territory has {state.territories[self.source_territory_id].troops} troops.")
        
        return self




