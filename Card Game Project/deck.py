import random
from card import Card


class Deck:
    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        self.cards = []

        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit, rank))

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if len(self.cards) == 0:
            return None

        return self.cards.pop()

    def cards_remaining(self):
        return len(self.cards)

    def restart(self):
        self.build_deck()