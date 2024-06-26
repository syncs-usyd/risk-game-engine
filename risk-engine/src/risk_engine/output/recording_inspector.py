

from typing import Tuple, Union, cast

from pydantic import RootModel
from risk_engine.output.game_result import GameBanResult, GameCancelledResult, GameCrashedResult, GameSuccessResult
from risk_shared.maps import earth
from risk_shared.models.territory_model import TerritoryModel
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.record_banned import RecordBanned
from risk_shared.records.record_cancelled import RecordCancelled
from risk_shared.records.record_player_eliminated import RecordPlayerEliminated
from risk_shared.records.record_start_game import RecordStartGame
from risk_shared.records.record_winner import RecordWinner
from risk_shared.records.types.record_type import RecordType


class RecordingInspector():

    def __init__(self, recording: list[RecordType]):
        self.recording = recording


    def _get_ranking(self) -> list[int]:
        ranking = []
        for record in self.recording:
            match record:
                case RecordPlayerEliminated() as x:
                    ranking.append(x.player)
                case RecordWinner() as x:
                    ranking.append(x.player)

        return ranking[::-1]


    def get_result(self) -> Union[GameBanResult, GameSuccessResult, GameCancelledResult, GameCrashedResult]:
        match self.recording[-1]:
            case RecordCancelled() as x:
                return GameCancelledResult(reason=x.reason)
            case RecordBanned() as x:
                return GameBanResult(ban_type=x.ban_type, player=x.player, reason=x.reason)
            case RecordWinner() as x:
                return GameSuccessResult(ranking=self._get_ranking())
            case _:
                return GameCrashedResult(reason="Game engine crashed.")
            

    def get_recording_json(self) -> str:
        return RootModel(self.recording).model_dump_json()
    

    def get_visualiser_forwards_backwards_differential_json(self) -> Tuple[str, str]:
        
        earth_map = earth.create_map()
        territories = dict([(x, TerritoryModel(territory_id=x, occupier=None, troops=0)) for x in earth_map.get_vertices()])

        forwards_differential: list[Tuple[int, list[TerritoryModel]]] = []
        backwards_differential: list[Tuple[int, list[TerritoryModel]]] = []


        for i, record in enumerate(self.recording):
            match record:
                case RecordStartGame() as r:
                    backwards_differential.append((i, []))

                case MoveClaimTerritory() as r:
                    territory_old = territories[r.territory].model_copy()
                    territory_new = territory_old.model_copy()

                    territory_new.occupier = r.move_by_player
                    territory_new.troops = 1

                    backwards_differential.append((i, [territory_old]))
                    forwards_differential.append((i, [territory_new]))

                    territories[territory_new.territory_id] = territory_new


                case MoveDistributeTroops() as r:
                    territories_old = [territories[territory].model_copy() for territory in r.distributions.keys()]
                    territories_new = dict([(territory.territory_id, territory.model_copy()) for territory in territories_old])

                    for key, value in r.distributions.items():
                        territories_new[key].troops += value

                    backwards_differential.append((i, territories_old))
                    forwards_differential.append((i, list(territories_new.values())))

                    for territory in territories_new.values():
                        territories[territory.territory_id] = territory


                case MoveFortify() as r:
                    source_territory_old = territories[r.source_territory].model_copy()
                    target_territory_old = territories[r.target_territory].model_copy()
                    source_territory_new = source_territory_old.model_copy()
                    target_territory_new = target_territory_old.model_copy()

                    source_territory_new.troops -= r.troop_count
                    target_territory_new.troops += r.troop_count

                    backwards_differential.append((i, [source_territory_old, target_territory_old]))
                    forwards_differential.append((i, [source_territory_new, target_territory_new]))

                    territories[source_territory_new.territory_id] = source_territory_new
                    territories[target_territory_new.territory_id] = target_territory_new


                case MovePlaceInitialTroop() as r:
                    territory_old = territories[r.territory].model_copy()
                    territory_new = territory_old.model_copy()

                    territory_new.troops += 1

                    backwards_differential.append((i, [territory_old]))
                    forwards_differential.append((i, [territory_new]))

                    territories[territory_new.territory_id] = territory_new


                case MoveTroopsAfterAttack() as r:
                    record_attack = cast(RecordAttack, self.recording[r.record_attack_id])
                    move_attack = cast(MoveAttack, self.recording[record_attack.move_attack_id])

                    attacking_territory_old = territories[move_attack.attacking_territory].model_copy()
                    defending_territory_old = territories[move_attack.defending_territory].model_copy()
                    attacking_territory_new = attacking_territory_old.model_copy()
                    defending_territory_new = defending_territory_old.model_copy()

                    attacking_territory_new.troops -= r.troop_count
                    defending_territory_new.troops += r.troop_count

                    backwards_differential.append((i, [attacking_territory_old, defending_territory_old]))
                    forwards_differential.append((i, [attacking_territory_new, defending_territory_new]))
                    
                    territories[attacking_territory_new.territory_id] = attacking_territory_new
                    territories[defending_territory_new.territory_id] = defending_territory_new


                case RecordAttack() as r:
                    move_attack = cast(MoveAttack, self.recording[r.move_attack_id])

                    attacking_territory_old = territories[move_attack.attacking_territory].model_copy()
                    defending_territory_old = territories[move_attack.defending_territory].model_copy()
                    attacking_territory_new = attacking_territory_old.model_copy()
                    defending_territory_new = defending_territory_old.model_copy()

                    attacking_territory_new.troops -= r.attacking_troops_lost
                    defending_territory_new.troops -= r.defending_troops_lost

                    if r.territory_conquered:
                        defending_territory_new.occupier = move_attack.move_by_player

                    backwards_differential.append((i, [attacking_territory_old, defending_territory_old]))
                    forwards_differential.append((i, [attacking_territory_new, defending_territory_new]))

                    territories[attacking_territory_new.territory_id] = attacking_territory_new
                    territories[defending_territory_new.territory_id] = defending_territory_new


                case RecordBanned() as r:
                    forwards_differential.append((i, []))


                case RecordCancelled() as r:
                    forwards_differential.append((i, []))


                case RecordWinner() as r:
                    forwards_differential.append((i, []))

        
        return (RootModel(forwards_differential).model_dump_json(), RootModel(backwards_differential).model_dump_json())