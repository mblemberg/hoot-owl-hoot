import random

CARDS_PER_HAND = 3
DEFAULT_BOARD = 'ygobprbprygborpygobprgyobprygborpygborp'
NEST_INDEX = 39

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

    def next_empty_space(self, starting_index: int, card_color: str) -> int:
        '''From the specified starting index, return the next empty space of the specified color.
        If none exist, the nest is returned, index 39.'''
        for index, space_color in enumerate(self.spaces[starting_index + 1:], starting_index + 1):
            if space_color == card_color and index not in self.owl_locations:
                return index
        else:
            return NEST_INDEX


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

    def move_owl(self, color: str, owl_index: int) -> None:
        '''Moves the specified owl to the next empty space of the specified color.'''

        owl_location = self.board.owl_locations[owl_index]
        move_to_location = self.board.next_empty_space(owl_location, color)
        self.board.owl_locations[owl_index] = move_to_location

    def move_sun(self):
        '''Moves the sun forward one position.'''

        self.board.sun_location += 1

    def state(self) -> str:
        '''Returns "WON", "LOST", or "IN PROGRESS".'''

        if self.board.sun_location == 13:
            return 'LOST'
        elif self.board.owl_locations.count(NEST_INDEX) == 6:
            return 'WON'
        else:
            return 'IN PROGRESS'

    def possible_moves(self) -> list:
        '''Returns a list of possible moves.  Each move is represented as a list of two elements;
        First, the color of the card as a single character.
        Second, the index of the owl to be moved.  If a sun card is played,
        the index of the owl can be ignored, but it will be set to 0.'''

        moves = []

        # If the hand contains a sun card, it must be played.
        if SUN in self.hands[self.turn]:
            moves.append([SUN, 0])
            return moves

        for card in self.hands[self.turn]:
            for owl_index, owl_location in enumerate(self.board.owl_locations):
                if owl_location != NEST_INDEX:
                    moves.append([card, owl_index])

        return moves

    def move(self, move: list) -> None:
        '''Makes a move.  Each move is represented as a list of two elements;
        First, the color of the card as a single character.
        Second, the index of the owl to be moved.  If a sun card is played,
        the index of the owl can be ignored, but it will be set to 0.'''

        if move[0] == 'S':
            self.move_sun()
        else:
            self.move_owl(move[0], move[1])

        self.hands[self.turn] = self.hands[self.turn].replace(move[0], '', 1)
        self.hands[self.turn] += self.deck.draw()

        self.turn = (self.turn + 1) % self.number_of_hands


g = Game()
print(g)
print(g.state())
print(g.possible_moves())

won = False
while not won:
    g = Game()
    print(g)
    while g.state() == 'IN PROGRESS':
        possible_moves = g.possible_moves()
        move_index = random.randint(0, len(possible_moves)-1)
        g.move(g.possible_moves()[move_index])
        print(g)
    if g.state() == 'WON':
        won = True
