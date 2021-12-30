from enum import Enum, unique
import random


@unique
class Color(Enum):
    '''Board space color constants.'''
    YELLOW = 'y'
    GREEN = 'g'
    ORANGE = 'o'
    BLUE = 'b'
    PURPLE = 'p'
    RED = 'r'
    SUN = 'S'


class Board:

    default_board = 'ygobprbprygborpygobprgyobprygborpygborp000102030405'

    def __init__(self):
        self.spaces = []
        for color in Board.default_board[:39]:
            self.spaces.append(Space(color))

        self.owl_locations = []
        for position in range(39, 51, 2):
            owl_location = Board.default_board[position:position+2]
            if owl_location != 'XX':
                self.owl_locations.append(int(owl_location))

        self.sun_location = 0

    def __str__(self) -> str:
        '''Encodes the board state into a string.
        Characters 0-38: space colors from start to finish.
        Characters 39-51: two characters each for the owl locations.
            Examples: 00 is starting square 1.
                      39 is the nest.
                      XX indicates that owl does not exist.
        Characters 52-53: location of the sun marker, 00-13.'''

        ret = ''

        # Space colors
        for s in self.spaces:
            ret += s.color

        # Owl locations
        for o in self.owl_locations:
            ret += f'{o:02d}'

        # Sun location
        ret += f'{self.sun_location:02d}'

        return ret


class Space:

    def __init__(self, color, occupied=False):
        self.color = color
        self.occupied = occupied


class Card:

    def __init__(self, color):
        self.color = color


class Deck:

    def __init__(self):

        self.cards = []

        for color in list(Color):
            for i in range(6):
                self.cards.append(Card(color.value))

        for i in range(14):
            self.cards.append(Card(Color.SUN.value))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        ret_val = ''
        for card in self.cards:
            ret_val += card.color

        return ret_val


class Hand:
    pass


class Player:
    pass


class Game:
    pass
