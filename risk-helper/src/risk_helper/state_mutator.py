from typing import TypeGuard, cast
from risk_helper.client_state import ClientState
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_attack_pass import MoveAttackPass
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_fortify_pass import MoveFortifyPass
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.record_banned import RecordBanned
from risk_shared.records.record_drew_card import PublicRecordDrewCard, RecordDrewCard
from risk_shared.records.record_player_eliminated import PublicRecordPlayerEliminated, RecordPlayerEliminated
from risk_shared.records.record_redeemed_cards import RecordRedeemedCards
from risk_shared.records.record_shuffled_cards import RecordShuffledCards
from risk_shared.records.record_start_game import PublicRecordStartGame, RecordStartGame
from risk_shared.records.record_start_turn import RecordStartTurn
from risk_shared.records.record_territory_conquered import RecordTerritoryConquered
from risk_shared.records.record_winner import RecordWinner
from risk_shared.records.types.record_type import RecordType


class StateMutator():

    def __init__(self, state: ClientState):
        self.state = state


    def commit(self, i: int, record: RecordType):
        if i != len(self.state.recording):
            raise RuntimeError("Please send us a discord message with this error log.")
        self.state.recording.append(record)

        match record:
            case MoveAttack() as r:
                self._commit_move_attack(r)
            case MoveAttackPass() as r:
                self._commit_move_attack_pass(r)
            case MoveClaimTerritory() as r:
                self._commit_move_claim_territory(r)
            case MoveDefend() as r:
                self._commit_move_defend(r)
            case MoveDistributeTroops() as r:
                self._commit_move_distribute_troops(r)
            case MoveFortify() as r:
                self._commit_move_fortify(r)
            case MoveFortifyPass() as r:
                self._commit_move_fortify_pass(r)
            case MovePlaceInitialTroop() as r:
                self._commit_move_place_initial_troop(r)
            case MoveRedeemCards() as r:
                self._commit_move_redeem_cards(r)
            case MoveTroopsAfterAttack() as r:
                self._commit_move_troops_after_attack(r)
            case RecordAttack() as r:
                self._commit_record_attack(r)
            case RecordBanned() as r:
                self._commit_record_banned(r)
            case RecordDrewCard() as r:
                self._commit_record_drew_card(r)
            case PublicRecordDrewCard() as r:
                self._commit_public_record_drew_card(r)
            case RecordPlayerEliminated() as r:
                self._commit_record_player_eliminated(r)
            case PublicRecordPlayerEliminated() as r:
                self._commit_public_record_player_eliminated(r)
            case RecordRedeemedCards() as r:
                self._commit_record_redeemed_cards(r)
            case RecordShuffledCards() as r:
                self._commit_record_shuffled_cards(r)
            case RecordStartGame() as r:
                self._commit_record_start_game(r)
            case PublicRecordStartGame() as r:
                self._commit_public_record_start_game(r)
            case RecordStartTurn() as r:
                self._commit_record_start_turn(r)
            case RecordTerritoryConquered() as r:
                self._commit_record_territory_conquered(r)
            case _:
                raise NotImplementedError
            
        self._update_public_player_model_to_me()

    
    def _update_public_player_model_to_me(self) -> None:
        player_id = self.state.me.player_id
        self.state.me.alive = self.state.players[player_id].alive
        self.state.me.troops_remaining = self.state.players[player_id].troops_remaining
        self.state.me.must_place_territory_bonus = self.state.players[player_id].must_place_territory_bonus
            

    def _commit_move_attack(self, r: MoveAttack) -> None:
        pass


    def _commit_move_attack_pass(self, r: MoveAttackPass) -> None:
        pass


    def _commit_move_claim_territory(self, r: MoveClaimTerritory) -> None:
        player = self.state.players[r.move_by_player]
        
        claimed_territory = self.state.territories[r.territory]
        claimed_territory.occupier = r.move_by_player
        claimed_territory.troops = 1
        player.troops_remaining -= 1


    def _commit_move_defend(self, r: MoveDefend) -> None:
        pass


    def _commit_move_distribute_troops(self, r: MoveDistributeTroops) -> None:
        player = self.state.players[r.move_by_player]

        # The player must have placed all their troops.
        player.troops_remaining = 0

        # Reset the matching territories.
        player.must_place_territory_bonus = []

        # Distribute the troops.
        for territory, troops in r.distributions.items():
            self.state.territories[territory].troops += troops


    def _commit_move_fortify(self, r: MoveFortify) -> None:
        self.state.territories[r.source_territory].troops -= r.troop_count
        self.state.territories[r.target_territory].troops += r.troop_count


    def _commit_move_fortify_pass(self, r: MoveFortifyPass) -> None:
        pass


    def _commit_move_place_initial_troop(self, r: MovePlaceInitialTroop) -> None:
        self.state.territories[r.territory].troops += 1
        self.state.players[r.move_by_player].troops_remaining -= 1


    def _commit_move_redeem_cards(self, r: MoveRedeemCards) -> None:
        def calculate_set_bonus(x: int):
            fixed_values = [4, 6, 8, 10, 12, 15]
            if x < len(fixed_values):
                return fixed_values[x]
            
            return 15 + (x - len(fixed_values) + 1) * 5

        # Give the set bonus for each set redeemed.
        total_set_bonus = 0
        for _ in range(len(r.sets)):
            total_set_bonus += calculate_set_bonus(self.state.card_sets_redeemed)
            self.state.card_sets_redeemed += 1

        # Give the matching territory bonus if applicable.
        all_cards: list[int] = []
        for card_set in r.sets:
            all_cards.extend(card_set)

        def remove_none(x) -> TypeGuard[int]:
            return x != None
        
        matching_territories = set(filter(remove_none, [self.state.cards[card].territory_id for card in all_cards])) & set(map(lambda x: x.territory_id, filter(lambda x: x.occupier == r.move_by_player, self.state.territories.values())))
        matching_territory_bonus = 2 if len(matching_territories) > 0 else 0

        # Modify the player.
        self.state.players[r.move_by_player].troops_remaining += total_set_bonus + matching_territory_bonus
        self.state.players[r.move_by_player].must_place_territory_bonus = list(matching_territories)
        
        if r.move_by_player == self.state.me.player_id:
            self.state.me.cards = list(filter(lambda x: x.card_id not in set(all_cards), self.state.me.cards))
        else:
            self.state.players[r.move_by_player].card_count -= len(all_cards)

        # Place the redeemed cards in the discarded deck.
        self.state.discarded_deck.extend([self.state.cards[i] for i in all_cards])


    def _commit_move_troops_after_attack(self, r: MoveTroopsAfterAttack) -> None:
        record_attack = cast(RecordAttack, self.state.recording[r.record_attack_id])

        move_attack_id = record_attack.move_attack_id
        move_attack = cast(MoveAttack, self.state.recording[move_attack_id])
        
        self.state.territories[move_attack.attacking_territory].troops -= r.troop_count
        self.state.territories[move_attack.defending_territory].troops += r.troop_count


    def _commit_record_attack(self, r: RecordAttack) -> None:
        move_attack = cast(MoveAttack, self.state.recording[r.move_attack_id])

        attacking_territory = move_attack.attacking_territory
        defending_territory = move_attack.defending_territory

        self.state.territories[attacking_territory].troops -= r.attacking_troops_lost
        self.state.territories[defending_territory].troops -= r.defending_troops_lost

        if r.territory_conquered:
            self.state.territories[defending_territory].occupier = move_attack.move_by_player


    def _commit_record_banned(self, r: RecordBanned) -> None:
        pass


    def _commit_record_drew_card(self, r: RecordDrewCard) -> None:
        if r.player != self.state.me.player_id:
            raise RuntimeError("Please send us a discord message with this error log.")
        
        self.state.me.cards.append(r.card)


    def _commit_public_record_drew_card(self, r: PublicRecordDrewCard) -> None:
        if r.player == self.state.me.player_id:
            raise RuntimeError("Please send us a discord message with this error log.")
        
        self.state.players[r.player].card_count += 1
        self.state.deck_card_count -= 1


    def _commit_record_player_eliminated(self, r: RecordPlayerEliminated) -> None:
        # The player is eliminated.
        self.state.players[r.player].alive = False

        # Their cards are surrendered.
        record_attack = cast(RecordAttack, self.state.recording[r.record_attack_id])
        move_attack = cast(MoveAttack, self.state.recording[record_attack.move_attack_id])

        if move_attack.move_by_player != self.state.me.player_id:
            raise RuntimeError("Please send us a discord message with this error log.")
        
        self.state.me.cards.extend(r.cards_surrendered)

    
    def _commit_public_record_player_eliminated(self, r: PublicRecordPlayerEliminated) -> None:
        # The player is eliminated.
        self.state.players[r.player].alive = False

        # Their cards are surrendered.
        record_attack = cast(RecordAttack, self.state.recording[r.record_attack_id])
        move_attack = cast(MoveAttack, self.state.recording[record_attack.move_attack_id])

        if move_attack.move_by_player == self.state.me.player_id:
            raise RuntimeError("Please send us a discord message with this error log.")
        
        self.state.players[move_attack.move_by_player].card_count += r.cards_surrendered_count


    def _commit_record_redeemed_cards(self, r: RecordRedeemedCards) -> None:
        pass


    def _commit_record_shuffled_cards(self, r: RecordShuffledCards) -> None:
        self.state.deck_card_count = len(self.state.discarded_deck)
        self.state.discarded_deck = []


    def _commit_record_start_game(self, r: RecordStartGame) -> None:
        raise RuntimeError("Please send us a discord message with this error log.")
        

    def _commit_public_record_start_game(self, r: PublicRecordStartGame) -> None:
        self.state.turn_order = list(r.turn_order).copy()
        self.state.players = dict([(x.player_id, x) for x in r.players])
        self.state.me = r.you


    def _commit_record_start_turn(self, r: RecordStartTurn) -> None:
        self.state.players[r.player].troops_remaining += r.territory_bonus + r.continent_bonus


    def _commit_record_territory_conquered(self, r: RecordTerritoryConquered) -> None:
        pass
