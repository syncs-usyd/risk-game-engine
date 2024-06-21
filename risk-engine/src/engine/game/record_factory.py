


import random
from typing import cast
from engine.exceptions import BrokenPipeException, CumulativeTimeoutException, InvalidResponseException, PlayerException, TimeoutException
from engine.game.state import State
from risk_shared.output.ban_type import BanType
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.record_banned import RecordBanned
from risk_shared.records.record_player_eliminated import RecordPlayerEliminated
from risk_shared.records.record_start_turn import RecordStartTurn


def record_attack_factory(state: State, move_attack_id: int, move_defend_id: int) -> 'RecordAttack':
    move_attack_obj = cast(MoveAttack, state.recording[move_attack_id])
    if move_attack_obj.move == "pass":
        raise RuntimeError("Tried to record an attack relying on a move attack that was a pass.")

    attacking_troops = move_attack_obj.move.attacking_troops
    
    move_defend_obj = cast(MoveDefend, state.recording[move_defend_id])
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

    return RecordAttack(move_attack_id=move_attack_id, move_defend_id=move_defend_id, attacking_troops_lost=attacking_troops_lost, defending_troops_lost=defending_troops_lost, territory_conquered=territory_conquered, defender_eliminated=defender_eliminated)


def record_banned_factory(e: PlayerException) -> 'RecordBanned':
    ban_type: BanType
    match e:
        case TimeoutException():
            ban_type = "TIMEOUT"
        case CumulativeTimeoutException():
            ban_type = "CUMULATIVE_TIMEOUT"
        case BrokenPipeException():
            ban_type = "BROKEN_PIPE"
        case InvalidResponseException():
            ban_type = "INVALID_MOVE"

        case _:
            raise RuntimeError("An unspecified PlayerException was raised.")

    return RecordBanned(player=e.player_id, reason=e.error_message, ban_type=ban_type)


def record_player_eliminated_factory(state: State, record_attack_id: int, player: int) -> 'RecordPlayerEliminated':
    cards_surrendered = list(state.players[player].cards).copy()
    return RecordPlayerEliminated(player=player, record_attack_id=record_attack_id, cards_surrendered=cards_surrendered)


def record_start_turn_factory(state: State, player: int) -> 'RecordStartTurn':
    player_territories = [territory_id for territory_id, territory in state.territories.items() if territory.occupier == player]
    territory_bonus = max(3, len(player_territories) // 3)

    continents_held = []
    continent_bonus = 0
    for continent, territories in state.map.get_continents().items():
        if all(territory_id in player_territories for territory_id in territories):
            continents_held.append(continent)
            continent_bonus += state.map.get_continent_bonus(continent)

    return RecordStartTurn(player=player, continents_held=continents_held, territories_held=len(player_territories), continent_bonus=continent_bonus, territory_bonus=territory_bonus)
