from random import shuffle
from typing import List, Tuple


def play_game(n_hands: int = 4) -> Tuple[int]:
    """
    Simulates a lost game and returns the number of cards removed from the
    deck and the number of cards played.

    return value = (cards_removed, cards_played)
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
    cards_played: int = 0
    suns_played: int = 0
    player_turn: int = 0
    while (suns_played < 13):

        if True in hands[player_turn]:
            hands[player_turn].remove(True)
            cards_played += 1
            suns_played += 1
        else:
            hands[player_turn].pop()
            cards_played += 1

        if suns_played < 13 and len(deck) > 0:
            hands[player_turn].append(deck.pop(0))

        player_turn += 1
        if player_turn >= n_hands:
            player_turn = 0

    return (50 - len(deck), cards_played)


def avg_cards(n_hands: int = 4, n_games: int = 1000) -> Tuple[float]:
    """
    Simulates n_games games with n_hands hands and returns the average number
    of cards removed from the deck and the average number of cards played.

    return value = (avg_removed, avg_played)
    """

    removed_sum: int = 0
    played_sum: int = 0
    for _ in range(n_games):
        result = play_game(n_hands=n_hands)
        removed_sum += result[0]
        played_sum += result[1]

    return (removed_sum / n_games, played_sum / n_games)


def simulate_games():
    """Simulate a million games and print the average number of cards
    removed from the deck and the average number of cards played."""

    n_games: int = int(1E6)
    print(f"Simulating {n_games:,} games per configuration.")

    for n_hands in range(1, 5):
        results = avg_cards(n_hands=n_hands, n_games=n_games)
        print(
            f"n_hands: {n_hands}\t"
            f"avg_cards_removed: {results[0]:.4f}\t "
            f"avg_cards_played: {results[1]:.4f}"
        )


def main() -> None:
    """Runs code for this module."""
    simulate_games()


if __name__ == "__main__":
    main()
