import random


class CmpPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.rounds_won = 0
        self.caught_cheating = 0

    def clear_hand(self):
        self.hand = []

    def draw_cards(self, deck, amount):
        for _ in range(amount):
            card = deck.draw_card()

            if card is not None:
                self.hand.append(card)

    def show_hand(self):
        for index, card in enumerate(self.hand):
            print(f"{index + 1}. {card}")

    def choose_discards(self):
        discard_positions = []

        for index, card in enumerate(self.hand):
            if card.value < 9:
                discard_positions.append(index)

        if len(discard_positions) > 3:
            discard_positions = discard_positions[:3]

        return discard_positions

    def discard_and_draw(self, deck):
        discard_positions = self.choose_discards()
        discard_positions.sort(reverse=True)

        for position in discard_positions:
            self.hand.pop(position)

        self.draw_cards(deck, len(discard_positions))


class HmnPlayer(CmpPlayer):
    def choose_discards(self):
        print("\nYour hand:")
        self.show_hand()

        print("\nEnter card numbers to discard, separated by spaces.")
        print("Example: 1 3 5")
        print("Press Enter to keep your hand.")

        user_input = input("Discard cards: ").lower().strip()

        if user_input == "royal":
            return "CHEAT_ROYAL"

        if user_input == "peek":
            return "CHEAT_PEEK"

        if user_input == "swap":
            return "CHEAT_SWAP"

        if user_input == "":
            return []

        discard_positions = []

        parts = user_input.split()

        for part in parts:
            if part.isdigit():
                number = int(part)

                if number >= 1 and number <= len(self.hand):
                    discard_positions.append(number - 1)

        discard_positions = list(set(discard_positions))

        if len(discard_positions) > 3:
            print("You can only discard up to 3 cards.")
            discard_positions = discard_positions[:3]

        return discard_positions