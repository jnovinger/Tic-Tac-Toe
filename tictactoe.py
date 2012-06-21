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
        return tuple()

    def _find_forks(self, me=True):
        """ Find any plays that will result in a fork. Find for me if ``me`` is True, else for the other player. """
        return tuple()

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
        if my_wins:
            pass

        # 2) else, block the other player's win
        their_wins = self._find_wins(me=False)
        if their_wins:
            pass

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
        self.round = 0

        # Any value other than None will be interpreted as the player's name and will be assumed to be a human player
        self.player1 = player1 if player1 is not None else ComputerPlayer(
            game=self,
            name='Computer Player 1',
            marks=('x', 'o'),
            debug=debug
        )

        self.player2 = player2 if player2 is not None else ComputerPlayer(
            game=self,
            name='Computer Player 2',
            marks=('o', 'x'),
            debug=debug
        )

    def play(self, player):
        """ Aggregates common play actions. """
        spot = player.play()
        self.board[spot[0]][spot[1]] = player.my_mark
        self.plays += 1
        self.build_board(echo=True)

    def start(self):
        """ The main game loop. """
        self.build_board(echo=True)
        while not self.game_is_over():
            # tell players to go
            self.play(self.player1)
            self.play(self.player2)
            self.round += 1

    def build_board(self, echo=False):
        """ Build the board, either for display or internal use. """
        board = ""
        for i, row in enumerate(self.board):
            board += "%s|%s|%s\n" % tuple(row)
            if i < 2:
                board += "-----\n"
        board += "Round: %s\nPlays: %s" % (self.round, self.plays)

        if echo:
            print board
        else:
            return board

    def game_is_over(self):
        """ Returns true if a winning move has been made. """
        board = self.board

        def check_line(line):
            if (' ' != line[0] == line[1] == line[2]):
                return True

        # check diagonal wins, start in upper left
        if (check_line([board[0][0], board[1][1], board[2][2]]) or
            check_line([board[0][2], board[1][1], board[2][0]])):
            return True

        # check row wins
        for row in board:
            if check_line(row):
                return True

        # check column wins, thanks to Peter Norvig -- http://www.norvig.com/python-iaq.html
        for col in zip(*board):
            if check_line(col):
                return True

        # no wins
        return False

if __name__ == "__main__":
    game = TicTacToeGame(debug=True)
    game.start()
