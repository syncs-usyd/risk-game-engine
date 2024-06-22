from collections import deque
import itertools
import random
from typing import Tuple, cast
from risk_helper.game import Game
from risk_shared.models.card_model import CardModel
from risk_shared.queries.query_attack import QueryAttack
from risk_shared.queries.query_claim_territory import QueryClaimTerritory
from risk_shared.queries.query_defend import QueryDefend
from risk_shared.queries.query_distribute_troops import QueryDistributeTroops
from risk_shared.queries.query_fortify import QueryFortify
from risk_shared.queries.query_place_initial_troop import QueryPlaceInitialTroop
from risk_shared.queries.query_redeem_cards import QueryRedeemCards
from risk_shared.queries.query_troops_after_attack import QueryTroopsAfterAttack
from risk_shared.queries.query_type import QueryType
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.types.move_type import MoveType


def main():
    
    # Get the game object, which will connect you to the engine and
    # track the state of the game.
    game = Game()
   
    # Respond to the engine's queries with your moves.
    while True:

        # Get the engine's query (this will block until you receive a query).
        query = game.get_next_query()

        # Based on the type of query, respond with the correct move.
        def choose_move(query: QueryType) -> MoveType:
            match query:
                case QueryClaimTerritory() as q:
                    return move_claim_territory(game, q)

                case QueryPlaceInitialTroop() as q:
                    return move_place_initial_troop(game, q)

                case QueryRedeemCards() as q:
                    return move_redeem_cards(game, q)

                case QueryDistributeTroops() as q:
                    return move_distribute_troops(game, q)

                case QueryAttack() as q:
                    return move_attack(game, q)

                case QueryTroopsAfterAttack() as q:
                    return move_troops_after_attack(game, q)

                case QueryDefend() as q:
                    return move_defend(game, q)

                case QueryFortify() as q:
                    return move_fortify(game, q)
        
        # Send the move to the engine.
        game.send_move(choose_move(query))
                

def move_claim_territory(game: Game, query: QueryClaimTerritory) -> MoveClaimTerritory:
    """At the start of the game, you can claim a single unclaimed territory every turn 
    until all the territories have been claimed by players."""

    unclaimed_territories = game.state.get_territories_owned_by(None)
    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)

    # We will try to always pick new territories that are next to ones that we own,
    # or a random one if that isn't possible.
    adjacent_territories = game.state.get_all_adjacent_territories(my_territories)

    # We can only pick from territories that are unclaimed and adjacent to us.
    available = list(set(unclaimed_territories) & set(adjacent_territories))
    if len(available) == 0:
        selected_territory = random.sample(unclaimed_territories, 1)[0]
    
    # Or if there are no such territories, we will pick just an unclaimed one.
    else:
        selected_territory = random.sample(unclaimed_territories, 1)[0]

    return game.move_claim_territory(query, selected_territory)


def move_place_initial_troop(game: Game, query: QueryPlaceInitialTroop) -> MovePlaceInitialTroop:
    """After all the territories have been claimed, you can place a single troop on one
    of your territories each turn until each player runs out of troops."""
    
    # We will place troops along the territories on our border.
    border_territories = game.state.get_all_border_territories(
        game.state.get_territories_owned_by(game.state.me.player_id)
    )

    # We will place a troop in the border territory with the least troops currently
    # on it. This should give us close to an equal distribution.
    border_territory_models = [game.state.territories[x] for x in border_territories]
    min_troops_territory = min(border_territory_models, key=lambda x: x.troops)

    return game.move_place_initial_troop(query, min_troops_territory.territory_id)


def move_redeem_cards(game: Game, query: QueryRedeemCards) -> MoveRedeemCards:
    """After the claiming and placing initial troops phases are over, you can redeem any
    cards you have at the start of each turn, or after killing another player."""

    # We will always redeem the minimum card sets we can (to increase the card set bonus
    # over the whole game). We could improve this by trying to redeem sets that give us
    # the matching territory bonus, or by reducing our usage of wildcards or matching
    # territory cards after we have already received the bonus for this turn.

    # We always have to redeem enough cards to reduce our card count below five.
    card_sets: list[Tuple[CardModel, CardModel, CardModel]] = []
    cards_remaining = game.state.me.cards

    while len(cards_remaining) >= 5:
        card_set = game.state.get_card_set(cards_remaining)

        # According to the pigeonhole principle, we should always be able to make a set
        # of cards if we have at least 5 cards.
        assert card_set != None
        card_sets.append(card_set)

        cards_remaining = [card for card in cards_remaining if card not in card_set]
    
    return game.move_redeem_cards(query, [(x[0].card_id, x[1].card_id, x[2].card_id) for x in card_sets])


def move_distribute_troops(game: Game, query: QueryDistributeTroops) -> MoveDistributeTroops:
    """After you redeem cards (you may have chosen to not redeem any), you need to distribute
    all the troops you have available across your territories. This can happen at the start of
    your turn or after killing another player.
    """

    # We will distribute troops equally across our border territories.
    border_territories = game.state.get_all_border_territories(
        game.state.get_territories_owned_by(game.state.me.player_id)
    )

    total_troops = game.state.me.troops_remaining
    troops_per_territory = total_troops // len(border_territories)
    leftover_troops = total_troops % len(border_territories)
    distributions = {}
    for territory in border_territories:
        distributions[territory] = troops_per_territory

    # The leftover troops will be put some territory (we don't care)
    distributions[border_territories[0]] += leftover_troops

    return game.move_distribute_troops(query, distributions)


def move_attack(game: Game, query: QueryAttack) -> MoveAttack:
    """After the troop phase of your turn, you may attack any number of times until you decide to
    stop attacking (by passing). After a successful attack, you may move troops into the conquered
    territory. If you eliminated a player you will get a move to redeem cards and then distribute troops."""
    
    # We are pacifists rn.
    return game.move_attack(query, "pass")


def move_troops_after_attack(game: Game, query: QueryTroopsAfterAttack) -> MoveTroopsAfterAttack:
    """After conquering a territory in an attack, you must move troops to the new territory."""
    
    # First we need to get the record that describes the attack, and then the move that specifies
    # which territory was the attacking territory.
    record_attack = cast(RecordAttack, game.state.recording[query.record_attack_id])
    move_attack = cast(MoveAttack, game.state.recording[record_attack.move_attack_id])
    assert move_attack.move != "pass"

    # We will always move the maximum number of troops we can.
    return game.move_troops_after_attack(query, min(0, game.state.territories[move_attack.move.attacking_territory].troops - 1))


def move_defend(game: Game, query: QueryDefend) -> MoveDefend:
    """If you are being attacked by another player, you must choose how many troops to defend with."""

    # We will always defend with the most troops that we can.

    # First we need to get the record that describes the attack we are defending against.
    move_attack = cast(MoveAttack, game.state.recording[query.move_attack_id])
    assert move_attack.move != "pass" # Since we are defending against this attack, it can't be a pass.
    defending_territory = move_attack.move.defending_territory
    
    # We can only defend with up to 2 troops, and no more than we have stationed on the defending
    # territory.
    defending_troops = min(game.state.territories[defending_territory].troops, 2)
    return game.move_defend(query, defending_troops)


def move_fortify(game: Game, query: QueryFortify) -> MoveFortify:
    """At the end of your turn, after you have finished attacking, you may move a number of troops between
    any two of your territories (they must be adjacent)."""

    my_territories = game.state.get_territories_owned_by(game.state.me.player_id)

    # We will always fortify towards the most powerful player (player with most troops on the map).
    total_troops_per_player = {}
    for player in game.state.players.values():
        total_troops_per_player[player.player_id] = sum([game.state.territories[x].troops for x in game.state.get_territories_owned_by(player.player_id)])

    most_powerful_player = max(total_troops_per_player.items(), key=lambda x: x[1])[0]

    # If we are the most powerful, we will pass our turn by moving zero troops from one of our territories to itself.
    if most_powerful_player == game.state.me.player_id:
        territory = my_territories[0]
        return game.move_fortify(query, territory, territory, 0)
    
    # Otherwise we will find the shortest path between our non-border territory with the most troops
    # and any of the most powerful player's territories and fortify along that path.
    candidate_territories = list(set(my_territories) - set(game.state.get_all_border_territories(my_territories)))
    most_troops_territory = max(candidate_territories, key=lambda x: game.state.territories[x].troops)

    # To find the shortest path, we will use a custom function.
    shortest_path = find_shortest_path_from_vertex_to_set(game, most_troops_territory, set(game.state.get_territories_owned_by(most_powerful_player)))

    # We will move our troops along this path (we can only move one step, and we have to leave one troop behind).
    # We have to check that we can move any troops though, if we can't then we will pass our turn.
    if game.state.territories[most_troops_territory].troops > 1:
        return game.move_fortify(query, shortest_path[0], shortest_path[1], game.state.territories[most_troops_territory].troops - 1)
    else:
        # Pass our turn.
        territory = my_territories[0]
        return game.move_fortify(query, territory, territory, 0)


def find_shortest_path_from_vertex_to_set(game: Game, source: int, target_set: set[int]) -> list[int]:
    """Used in move_fortify()."""

    # We perform a BFS search from our source vertex, stopping at the first member of the target_set we find.
    queue = deque()
    queue.appendleft(source)

    parent = {}
    seen = {}

    while len(queue) != 0:
        current = queue.pop()

        if current in target_set:
            break

        for neighbour in game.state.map.get_adjacent_to(current):
            if neighbour not in seen:
                seen[neighbour] = True
                parent[neighbour] = current
                queue.appendleft(neighbour)

    path = []
    while current in parent:
        path.append(current)
        current = parent[current]

    return path[::-1]

if __name__ == "__main__":
    main()