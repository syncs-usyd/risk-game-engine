from typing import final

from engine.models.territory_model import TerritoryModel


@final
class Territory(TerritoryModel):

    @classmethod
    def factory(cls, territory_id: int) -> 'Territory':
        return cls(territory_id=territory_id, occupier=None, troops=0)