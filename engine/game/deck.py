import random
from engine.game.card import Card

class Deck:
    def __init__(self, cards):
        self._cards: list[Card] = [Card.factory(**item) for item in cards]

    def shuffle_deck(self):
        card_list = list(self._cards)
        random.shuffle(card_list)
        self._cards = card_list
        for card in self._cards:
            print(card)

    def draw_card(self):
        return self._cards.pop(0)
    
    def add_cards(self, card_list):
        self._cards.extend(card_list)
        self.shuffle_deck()