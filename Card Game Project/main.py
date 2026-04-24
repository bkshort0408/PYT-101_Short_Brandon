from manager import Manager


def main():
    game = Manager()
    playing = True

    while playing:
        game.start_game()

        choice = input("\nPlay again? (yes/no): ").lower().strip()

        if choice != "yes" and choice != "y":
            playing = False
            print("Thanks for playing Shadow Poker!")


main()