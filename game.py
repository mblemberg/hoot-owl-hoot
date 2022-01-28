import random
from typing import List

CARDS_PER_HAND = 3
DEFAULT_BOARD = 'ygobprbprygborpygobprgyobprygborpygborpN'
NEST_INDEX = len(DEFAULT_BOARD)

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
        self.owl_positions = [0, 1, 2, 3, 4, 5]
        self.sun_position = 0

    def __repr__(self) -> str:
        '''Encodes the board state into a csv string.
        Item 1: Space colors
        Items 2-7: Owl positions, starting from zero
        Item 8: position of the sun marker, 0-13'''

        # Space colors
        ret = self.spaces + ','

        # Owl positions
        for owl in self.owl_positions:
            ret += str(owl) + ','

        # Sun position
        ret += str(self.sun_position)

        return ret

    def next_empty_space(self, starting_index: int, card_color: str) -> int:
        '''From the specified starting index, return the next empty space of the specified color.
        If none exist, the nest is returned, index NEST_INDEX.'''
        for index, space_color in enumerate(self.spaces[starting_index + 1:], starting_index + 1):
            if space_color == card_color and index not in self.owl_positions:
                return index
        else:
            return NEST_INDEX

    def sort_owls(self) -> None:
        '''Sort the owls in order from closest to furthest from the nest.
        index 0 is the owl furthest from the nest.
        index 5 is the owl closest to the nest.'''

        self.owl_positions.sort()


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


class Move:

    def __init__(
        self,
        card_color: str,
        owl_index: int = None
    ):
        self.card_color = card_color
        self.owl_index = owl_index


class Game:

    WIN = 'Win'
    LOSS = 'Loss'
    IN_PROGRESS = 'In Progress'

    def __init__(self, number_of_hands: int = 2) -> None:
        '''Creates a game.'''

        self.board = Board()

        self.deck = Deck()
        self.deck.shuffle()

        self.number_of_hands = number_of_hands
        self.hands = []
        self.turn = 0

        for _ in range(number_of_hands):
            hand = self.deck.draw(number_of_cards=CARDS_PER_HAND)
            self.hands.append(hand)

    def __repr__(self):
        '''Returns a csv string representation of the game.'''

        ret_val = self.board.__repr__() + ','
        ret_val += self.deck.cards + ','
        ret_val += ','.join(self.hands) + ','
        ret_val += str(self.turn)

        return ret_val

    def __str__(self):
        '''Returns a string representation of the game state.'''

        ret_val = ''

        for position in range(len(self.board.spaces)):
            if position in self.board.owl_positions:
                ret_val += '*'
            else:
                ret_val += ' '

        ret_val += '|'

        for hand in self.hands:
            ret_val += ' ' + hand

        ret_val += f' | Sun: {self.board.sun_position}'



        return ret_val

    def move_owl(self, color: str, owl_index: int) -> None:
        '''Moves the specified owl to the next empty space of the specified color.'''

        owl_position = self.board.owl_positions[owl_index]
        move_to_position = self.board.next_empty_space(owl_position, color)
        self.board.owl_positions[owl_index] = move_to_position
        self.board.sort_owls()

    def move_sun(self):
        '''Moves the sun forward one position.'''

        self.board.sun_position += 1

    def state(self) -> str:
        '''Returns "WON", "LOST", or "IN PROGRESS".'''

        if self.board.sun_position == 13:
            return Game.LOSS
        elif self.board.owl_positions.count(NEST_INDEX) == 6:
            return Game.WIN
        else:
            return Game.IN_PROGRESS

    def possible_moves(self) -> List[Move]:
        '''Returns a list of possible moves.'''

        moves = []

        # If the hand contains a sun card, it must be played.
        if SUN in self.hands[self.turn]:
            moves.append(Move(SUN))
            return moves

        for card in self.hands[self.turn]:
            for owl_index, owl_position in enumerate(self.board.owl_positions):
                if owl_position != NEST_INDEX:
                    moves.append(Move(card, owl_index=owl_index))

        return moves

    def move(self, move: Move) -> None:
        '''Makes a move.'''

        if move.card_color == SUN:
            self.move_sun()
        else:
            self.move_owl(move.card_color, move.owl_index)

        self.hands[self.turn] = self.hands[self.turn].replace(
            move.card_color, '', 1)
        self.hands[self.turn] += self.deck.draw()

        self.turn = (self.turn + 1) % self.number_of_hands
