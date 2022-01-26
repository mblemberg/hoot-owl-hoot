import random

CARDS_PER_HAND = 3
DEFAULT_BOARD = 'ygobprbprygborpygobprgyobprygborpygborp'

SUN = 'S'
YELLOW = 'y'
GREEN = 'g'
ORANGE = 'o'
BLUE = 'b'
PURPLE = 'p'
RED = 'r'
ALL_COLORS = 'ygobpr'


class Board:

    def __init__(self):
        '''Creates a game board.'''

        self.spaces = DEFAULT_BOARD
        self.owl_locations = [0, 1, 2, 3, 4, 5]
        self.sun_location = 0

    def __repr__(self) -> str:
        '''Encodes the board state into a csv string.
        Item 1: Space colors
        Items 2-7: Owl locations, starting from zero
        Item 8: location of the sun marker, 0-13'''

        # Space colors
        ret = self.spaces + ','

        # Owl locations
        for owl in self.owl_locations:
            ret += str(owl) + ','

        # Sun location
        ret += str(self.sun_location)

        return ret


class Deck:

    def __init__(self) -> None:
        '''Create a deck of cards.'''

        self.cards = ''

        for color in ALL_COLORS:
            self.cards += color * 6

        self.cards += SUN * 14

    def shuffle(self) -> None:
        '''Randomly shuffles the deck.'''

        cards_list = list(self.cards)
        random.shuffle(cards_list)
        self.cards = ''.join(cards_list)

    def draw(self, number_of_cards: int = 1) -> str:
        '''Draw cards from the top of the deck, starting at position zero.
        Removes the cards from the deck and returns them.'''

        drawn_cards = self.cards[0: number_of_cards]
        self.cards = self.cards[number_of_cards:]
        return drawn_cards

    def remaining(self) -> dict:
        '''Returns a dictionary of the remaining card cound for each color.
        i.e { 'y' : 6 }'''

        remaining_cards = {}
        for color in ALL_COLORS:
            remaining_cards[color] = self.cards.count(color)

        remaining_cards[SUN] = self.cards.count(SUN)
        remaining_cards['total'] = len(self.cards)

        return remaining_cards


class Game:

    def __init__(self, number_of_hands: int = 2) -> None:
        '''Creates a game.'''

        self.board = Board()

        self.deck = Deck()
        self.deck.shuffle()

        self.hands = []

        for _ in range(number_of_hands):
            hand = self.deck.draw(number_of_cards=CARDS_PER_HAND)
            self.hands.append(hand)
