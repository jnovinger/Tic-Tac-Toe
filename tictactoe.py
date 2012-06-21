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
    def __init__(self, game, name, debug=False):
        self.game = game
        self.name = name
        self._debug = debug
        self.debug("%s has joined the game!" % self.name)

    def debug(self, string):
        if self._debug:
            print string

class TicTacToeGame(object):
    def __init__(self, player1=None, player2=None, debug=False):
        self._debug = debug
        self.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.plays = 0
        self.round = 0

        # Any value other than None will be interpreted as the player's name and will be assumed to be a human player
        self.player1 = player1 if player1 is not None else ComputerPlayer(self, 'Computer Player 1', debug)
        self.player2 = player2 if player2 is not None else ComputerPlayer(self, 'Computer Player 2', debug)

    def start(self):
        self.build_board(echo=True)
        while not self.game_is_over():
            # tell players to go
            #self.player1.play()
            self.plays += 1
            #self.player2.play()
            self.plays += 1
            self.round += 1

            # show progress
            self.build_board(echo=True)

    def build_board(self, echo=False):
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

        # check row wins
        for row in board:
            if (row[0] != ' ' and
                row[0] == row[1] and
                row[1] == row[2] and
                row[2] == row[0]):
                return True

        # check column wins, thanks to Peter Norvig -- http://www.norvig.com/python-iaq.html
        for col in zip(*board):
            if (col[0] != ' ' and
                col[0] == col[1] and
                col[1] == col[2] and
                col[2] == col[0]):
                return True

        # check diagonal wins, start in upper left
        if (board[0][0] != ' ' and
            board[0][0] == board[1][1] and
            board[1][1] == board[2][2]):
            return True
        elif (board[0][2] != ' ' and
            board[0][2] == board[1][1] and
            board[1][1] == board[2][0]):
            return True

        return False

if __name__ == "__main__":
    game = TicTacToeGame(debug=True)
    game.start()
