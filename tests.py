import sys
from StringIO import StringIO
import unittest

from tictactoe import TicTacToeGame, ComputerPlayer

class TwoComputerPlayerTestCase(unittest.TestCase):
    """ Tests for the TicTacToeGame class. """

    def setUp(self):
        """ Set up a sample game for tests. """
        self.game = TicTacToeGame()

    def test_player_setup(self):
        """ Make sure that the game instance knows how to set up computer players. """
        self.assertTrue(isinstance(self.game.player1, ComputerPlayer))
        self.assertTrue(isinstance(self.game.player2, ComputerPlayer))


    def test_build_board(self):
        """ Make sure build_board() is behaving. Order of tests is important, this test assumes no plays have been made. """
        self.assertEqual(self.game.build_board(), " | | \n-----\n | | \n-----\n | | \nRound: 0\nPlays: 0")
        self.assertEqual(self.game.build_board(echo=True), None)

        # TODO: test echo=True output like debug below

    def test_debug(self):
        """ Make sure debug output is working correctly. Maybe this should live in it's own test case. """
        std_out = sys.stdout
        try:
            sys.stdout = StringIO()
            TicTacToeGame(debug=True)
            self.assertEqual(
                sys.stdout.getvalue().strip(),
                "Computer Player 1 has joined the game!\nComputer Player 2 has joined the game!"
            )
        finally:
            sys.stdout = std_out

if __name__ == "__main__":
    unittest.main()
