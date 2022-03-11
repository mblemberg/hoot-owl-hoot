from random import shuffle
from typing import List


def play_game(n_hands: int = 4) -> int:
    """
    Simulates a lost game and returns the number of cards removed from the deck.
    """

    """
    Create and shuffle a deck.
    
    Each boolean represents a card.
    True = Sun card
    False = Color card
    """
    deck: List[bool] = [True] * 14
    deck += [False] * 36
    shuffle(deck)

    # Deal the hands from the deck.
    hands: List[List[bool]] = []
    for _ in range(n_hands):
        hand: List[bool] = deck[:3]
        del deck[:3]
        hands.append(hand)

    # Play the game.
    suns_played: int = 0
    player_turn: int = 0
    while (suns_played < 13):

        if True in hands[player_turn]:
            hands[player_turn].remove(True)
            suns_played += 1
        else:
            hands[player_turn].pop()

        if suns_played < 13 and len(deck) > 0:
            hands[player_turn].append(deck.pop(0))

        player_turn += 1
        if player_turn >= n_hands:
            player_turn = 0

    return 50 - len(deck)


def avg_cards_removed(n_hands: int = 4, n_games: int = 1000) -> float:
    """
    Simulates n_games games with n_hands hands and returns the average number
    of cards removed from the deck.
    """

    sum: int = 0
    for _ in range(n_games):
        sum += play_game(n_hands=n_hands)

    return sum / n_games


def main() -> None:
    """Runs code for this module."""

    n_games: int = int(1E9)
    print(f"Simulating {n_games:,} games per configuration.")

    for n_hands in range(1, 11):
        print(
            "Average cards removed from the deck in a "
            f"{n_hands} player game = "
            f"{avg_cards_removed(n_hands=n_hands, n_games=1_000_000):.4f}"
        )


if __name__ == "__main__":
    main()
