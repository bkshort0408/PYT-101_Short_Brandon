import random
from deck import Deck
from card import Card
from players import HmnPlayer, CmpPlayer


class Manager:
    def __init__(self):
        self.deck = Deck()
        self.human = HmnPlayer("Player")
        self.computer = CmpPlayer("Computer Dealer")
        self.round_number = 1
        self.max_rounds = 5

    def explain_rules(self):
        print("\n===== SHADOW POKER =====")
        print("You are playing a 5-card draw poker game.")
        print("Each round, both players receive 5 cards.")
        print("You may discard up to 3 cards and draw replacements.")
        print("Best poker hand wins the round.")
        print("Win the most rounds after 5 rounds to win the game.")
        print("\nThree comands may give you a theiving chance, however you may get caught!")
        print("\nYou might PEEK a ROYAL flush or SWAP a round with the computer")
        print("When you are caught the computer will the round automatically.\n")

    def reset_game(self):
        self.deck.restart()
        self.human.rounds_won = 0
        self.computer.rounds_won = 0
        self.human.caught_cheating = 0
        self.round_number = 1

    def deal_hands(self):
        self.human.clear_hand()
        self.computer.clear_hand()

        self.human.draw_cards(self.deck, 5)
        self.computer.draw_cards(self.deck, 5)

    def display_status(self):
        print("\n-----------------------------")
        print(f"Round {self.round_number} of {self.max_rounds}")
        print(f"Your rounds won: {self.human.rounds_won}")
        print(f"Computer rounds won: {self.computer.rounds_won}")
        print(f"Cards left in deck: {self.deck.cards_remaining()}")
        print("-----------------------------")

    def check_cheat_detection(self):
        caught_chance = random.randint(1, 100)

        if caught_chance <= 75:
            self.human.caught_cheating += 1
            print("\nThe dealer noticed something suspicious!")
            print("You were caught cheating and lose this round.")
            return True

        print("\nYou got away with it... this time.")
        return False

    def handle_cheat(self, cheat_code):
        if self.check_cheat_detection():
            return True

        if cheat_code == "CHEAT_ROYAL":
            self.human.hand = [
                Card("Spades", "10"),
                Card("Spades", "J"),
                Card("Spades", "Q"),
                Card("Spades", "K"),
                Card("Spades", "A")
            ]
            print("Your hand somehow becomes a Royal Flush.")

        elif cheat_code == "CHEAT_PEEK":
            print("\nComputer's hand:")
            self.computer.show_hand()

        elif cheat_code == "CHEAT_SWAP":
            best_card = self.computer.hand[0]
            worst_card = self.human.hand[0]

            for card in self.computer.hand:
                if card.value > best_card.value:
                    best_card = card

            for card in self.human.hand:
                if card.value < worst_card.value:
                    worst_card = card

            self.computer.hand.remove(best_card)
            self.human.hand.remove(worst_card)

            self.human.hand.append(best_card)
            self.computer.hand.append(worst_card)

            print("You covertly swapped your worst card for the computer's best card.")

        return False

    def replace_discards(self, player, discard_positions):
        discard_positions.sort(reverse=True)

        for position in discard_positions:
            player.hand.pop(position)

        player.draw_cards(self.deck, len(discard_positions))

    def evaluate_hand(self, hand):
        values = sorted([card.value for card in hand], reverse=True)
        suits = [card.suit for card in hand]

        counts = {}

        for value in values:
            if value not in counts:
                counts[value] = 0
            counts[value] += 1

        count_values = sorted(counts.values(), reverse=True)

        is_flush = len(set(suits)) == 1
        is_straight = values == list(range(values[0], values[0] - 5, -1))

        if values == [14, 5, 4, 3, 2]:
            is_straight = True
            values = [5, 4, 3, 2, 14]

        if is_straight and is_flush:
            return (8, values, "Straight Flush")

        if 4 in count_values:
            return (7, values, "Four of a Kind")

        if count_values == [3, 2]:
            return (6, values, "Full House")

        if is_flush:
            return (5, values, "Flush")

        if is_straight:
            return (4, values, "Straight")

        if 3 in count_values:
            return (3, values, "Three of a Kind")

        if count_values == [2, 2, 1]:
            return (2, values, "Two Pair")

        if 2 in count_values:
            return (1, values, "One Pair")

        return (0, values, "High Card")

    def play_round(self):
        if self.deck.cards_remaining() < 15:
            print("\nDeck is low, reshuffling a new deck.")
            self.deck.restart()

        self.display_status()
        self.deal_hands()

        discard_choice = self.human.choose_discards()

        if discard_choice == "CHEAT_ROYAL" or discard_choice == "CHEAT_PEEK" or discard_choice == "CHEAT_SWAP":
            caught = self.handle_cheat(discard_choice)

            if caught:
                self.computer.rounds_won += 1
                self.round_number += 1
                return
        else:
            self.replace_discards(self.human, discard_choice)

        self.computer.discard_and_draw(self.deck)

        human_result = self.evaluate_hand(self.human.hand)
        computer_result = self.evaluate_hand(self.computer.hand)

        print("\nYour final hand:")
        self.human.show_hand()
        print(f"Your hand type: {human_result[2]}")

        print("\nComputer final hand:")
        self.computer.show_hand()
        print(f"Computer hand type: {computer_result[2]}")

        if human_result > computer_result:
            print("\nYou win this round!")
            self.human.rounds_won += 1

        elif computer_result > human_result:
            print("\nComputer wins this round.")
            self.computer.rounds_won += 1

        else:
            print("\nThis round is a tie.")

        self.round_number += 1

    def game_over(self):
        return self.round_number > self.max_rounds

    def display_winner(self):
        print("\n===== FINAL RESULTS =====")
        print(f"Your rounds won: {self.human.rounds_won}")
        print(f"Computer rounds won: {self.computer.rounds_won}")
        print(f"Times caught cheating: {self.human.caught_cheating}")

        if self.human.rounds_won > self.computer.rounds_won:
            print("\nYou won the poker game!")

        elif self.computer.rounds_won > self.human.rounds_won:
            print("\nThe computer won the poker game.")

        else:
            print("\nThe game ended in a tie.")

    def start_game(self):
        self.reset_game()
        self.explain_rules()

        while not self.game_over():
            self.play_round()

        self.display_winner()