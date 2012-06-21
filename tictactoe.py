"""
Jason Novinger

According to the fine folks over at [Wikipedia](http://en.wikipedia.org/wiki/Tic-tac-toe), the "perfect game" strategy for Tic Tac Toe uses the following algorithm
    A player can play perfect tic-tac-toe (win or draw) given they move according to the highest possible move from the following table.[7]
    1) Win: If the player has two in a row, play the third to get three in a row.
    2) Block: If the [opponent] has two in a row, play the third to block them.
    3) Fork: Create an opportunity where you can win in two ways.
    4) Block opponent's Fork:
        Option 1: Create two in a row to force the opponent into defending, as long as it doesn't result in them creating a fork or winning. For example, if "X" has a corner, "O" has the center, and "X" has the opposite corner as well, "O" must not play a corner in order to win. (Playing a corner in this scenario creates a fork for "X" to win.)
        Option 2: If there is a configuration where the opponent can fork, block that fork.
    5) Center: Play the center. (If it is the first move of the game, playing on a corner gives "O" more opportunities to make a mistake and may therefore be the better choice; however, it makes no difference between perfect players.)
    6) Opposite corner: If the opponent is in the corner, play the opposite corner.
    7) Empty corner: Play in a corner square.
    8) Empty side: Play in a middle square on any of the 4 sides.
"""

from copy import deepcopy


class HumanPlayer(object):
    def __init__(self, game, name, marks):
        self.game = game
        self.my_mark = marks[0]
        self.their_mark = marks[1]

        self.name = raw_input("What's your name? ") or name
        print "Thanks %s!\n" % self.name

    def play(self):
        play = None
        while not play:
            if play is not None:
                print "Sorry, please make a valid move."
            play = raw_input("%s, please enter your next play in \"x y\" form: " % self.name)

            play = [int(x) for x in play.split(' ')]

            if self.game.board[play[0]][play[1]] == ' ':
                return play
            else:
                play = ''

class ComputerPlayer(object):
    def __init__(self, game, name, marks, debug=False):
        self.game = game
        self.name = name
        self.my_mark = marks[0]
        self.their_mark = marks[1]
        self._debug = debug
        self.debug("%s has joined the game!" % self.name)


    def _find_wins(self, me=True):
        """ Find any winning plays, for me if ``me`` is True, else for the other player. """
        wins = []

        mark = self.my_mark if me else self.their_mark

        # make a local copy to mess with
        for i, row in enumerate(self.game.board):
            for j, col in enumerate(row):
                board = deepcopy(self.game.board)
                if col == ' ':
                    board[i][j] = mark
                    if self.game.game_is_over(board=board):
                        wins.append((i, j))

        return wins

    def _find_forks(self, me=True):
        """ Find any plays that will result in a fork. Find for me if ``me`` is True, else for the other player. """
        forks = []
        return forks

    def play(self):
        """
        Inspect the board and make a move, using the alogrithm above.

        Returns an (x, y) tuple with the zero-based coordinates of where to play.
        """
        board = self.game.board
        my_mark = self.my_mark
        their_mark = self.their_mark

        # 1) find any winning moves and play them
        my_wins = self._find_wins()
        for win in my_wins:
            return win

        # 2) else, block the other player's win
        their_wins = self._find_wins(me=False)
        for win in their_wins:
            return win

        # 3) else, fork
        my_forks = self._find_forks()
        if my_forks:
            pass

        # 4) else, block other player's fork
        their_forks = self._find_forks(me=False)
        if their_forks:
            # a
            pass
            # b
            pass

        # 5) else, play the center
        if board[1][1] == ' ':
            return (1, 1)

        # 6) else, play an opposite corner
        corners = [(0, 0), (0, 2), (2, 2), (2, 0)]
        # here comes the ugly
        for i, corner in enumerate(corners):
            other_corner = corners[(i - 2) % len(corners)]
            if (board[corner[0]][corner[1]] == their_mark and
                board[other_corner[0]][other_corner[1]] == ' '):
                return other_corner

        # 7) else, play an empty corner
        for corner in corners:
            if board[corner[0]][corner[1]] == ' ':
                return corner

        # 8) else, play an empty side
        sides = [(0, 1), (1, 2), (2, 1), (1, 0)]
        for side in sides:
            if board[side[0]][side[1]] == ' ':
                return side

    def debug(self, string):
        if self._debug:
            print string


class TicTacToeGame(object):
    def __init__(self, player1=None, player2=None, debug=False):
        self._debug = debug
        self.board = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.plays = 0

        # Any value other than None will be interpreted as the player's name and will be assumed to be a human player

        if player1 is None:
            self.player1 = ComputerPlayer(game=self, name='Computer Player #1', marks=('x', 'o'), debug=debug)
        else:
            self.player1 = HumanPlayer(game=self, name=player1, marks=('x', 'o'))

        if player2 is None:
            self.player2 = ComputerPlayer(game=self, name='Computer Player #2', marks=('o', 'x'), debug=debug)
        else:
            self.player2 = ComputerPlayer(game=self, name=player2, marks=('o', 'x'))


    def play(self, player):
        """ Aggregates common play actions. """
        spot = player.play()
        self.board[spot[0]][spot[1]] = player.my_mark
        self.plays += 1
        self.build_board(echo=True)

        winner = self.game_is_over()
        if winner:
            if winner == player.my_mark:
                return player
            if winner == 'draw':
                return winner
        return False

    def start(self):
        """ The main game loop. """
        self.build_board(echo=True)
        player = None
        winner = False
        while not winner:
            # switch and play
            player = self.player1 if player is not self.player1 else self.player2
            winner = self.play(player)

        if winner in [self.player1, self.player2]:
            print "Yay, %s won!" % winner.name
        else:
            print "Sorry, guess nobody wins."

    def build_board(self, echo=False):
        """ Build the board, either for display or internal use. """
        board = ""
        for i, row in enumerate(self.board):
            board += "%s|%s|%s\n" % tuple(row)
            if i < 2:
                board += "-----\n"
        board += "Plays: %s\n" % self.plays

        if echo:
            print board
        else:
            return board

    def game_is_over(self, board=None):
        """
        Accepts:
            ``board``::
                optional, default: self.board
                useful for AI players to check their moves

        Returns:
            - the winning mark, if a winning move has been made;
            - False, if no winning move has been made and the board is not full;
            - 'draw' if there no winning move has been made and the board is full.
        """
        board = board or self.board

        def check_line(line):
            if (' ' != line[0] == line[1] == line[2]):
                return True

        # check diagonal wins, start in upper left
        if (check_line([board[0][0], board[1][1], board[2][2]]) or
            check_line([board[0][2], board[1][1], board[2][0]])):
            return board[1][1]

        # check row wins
        for row in board:
            if check_line(row):
                return row[0]

        # check column wins, thanks to Peter Norvig -- http://www.norvig.com/python-iaq.html
        for col in zip(*board):
            if check_line(col):
                return col[0]

        # if the board is full
        if self.plays > 8:
            return 'draw'

        # no wins
        return False

if __name__ == "__main__":
    game = TicTacToeGame(player1='human', debug=True)
    game.start()
