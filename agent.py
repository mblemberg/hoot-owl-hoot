from game import *


class Agent:
    '''Plays the game for all players.'''

    def __init__(
        self,
        n_hands: int = 2,
        description: str = None
    ) -> None:
        self.n_hands = n_hands
        self.game = Game(number_of_hands=n_hands)
        self.description = description

    def make_random_move(self):
        '''Makes a random move from the list of all possible moves.'''

        possible_moves = self.game.possible_moves()
        move_index = random.randint(0, len(possible_moves) - 1)
        self.game.move(possible_moves[move_index])

    def move(self):
        '''The super class just makes random legal moves.'''

        self.make_random_move()

    def play_game(self, show_game: bool = False) -> bool:
        '''Play the game to completion.
        Return True if the game is a win, False otherwise.'''

        if show_game:
            print(self.game.board.spaces)
            print(self.game)

        while self.game.state() == Game.IN_PROGRESS:

            self.move()
            if show_game:
                print(self.game)

        if show_game:
            print(f'Game result: {self.game.state()}')

        return self.game.state() == Game.WIN

    def play_n_games(self, n: int) -> dict:
        '''Play the specified number of games.  Return statistics.'''

        stats = {
            'wins': 0,
            'losses': 0,
        }

        for _ in range(n):
            self.game = Game(number_of_hands=self.n_hands)
            result = self.play_game()
            if result:
                stats['wins'] += 1
            else:
                stats['losses'] += 1

        stats['count'] = stats['wins'] + stats['losses']
        stats['win rate'] = stats['wins'] / stats['count']

        return stats

    def move_nth_owl_randomly(self, n: int) -> None:
        '''If legal, moves the nth owl with a random card from the hand.
        n = 0 means the owl furthest from the nest.
        n = 5 means the owl closest to the nest.

        If the specified owl is already in the nest, move the owl
        closest to the nest with a random card from the hand instaed.'''

        possible_moves = self.game.possible_moves()

        if len(possible_moves) == 1:
            self.game.move(possible_moves[0])
            return

        else:
            for owl in range(n, -1, -1):
                random.shuffle(possible_moves)
                for move in possible_moves:
                    if move.owl_index == owl:
                        self.game.move(move)
                        return
