import sys
from StringIO import StringIO
import unittest

from tictactoe import TicTacToeGame, ComputerPlayer

class ComputerPlayerTestCase(unittest.TestCase):

    def setUp(self):
        self.game = TicTacToeGame()
        self.player1 = self.game.player1
        self.player2 = self.game.player2

    def test_can_find_wins(self):
        self.game.board = [['x',' ','x'],[' ',' ',' '],[' ',' ',' ']]
        self.assertTrue(self.player1._find_wins())
        self.assertFalse(self.player1._find_wins(me=False))

    def test_strategy_one(self):
        """ Go for the kill. """
        self.game.board = [['x',' ','x'],[' ','o',' '],['o',' ',' ']]
        self.assertEqual((0, 1), self.player1.play())

    def test_strategy_two(self):
        """ Block any possible wins for the opponent. """
        self.game.board = [['x',' ','x'],[' ','x',' '],[' ','o','o']]
        self.assertEqual((2, 0), self.player2.play())

    def test_strategy_three(Self):
        """ """
        pass

    def test_strategy_four(self):
        pass

    def test_strategy_five(self):
        """ If strategies 1-4 fail, play the center if possible. """
        self.game.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.assertEqual((1, 1), self.player1.play())

    def test_strategy_six(self):
        """ If strategies 1-5 fail, find a corner from the opponent and play that. """
        self.game.board = [['o',' ',' '],[' ','x',' '],[' ',' ',' ']]
        self.assertEqual((2, 2), self.player1.play())

    def test_strategy_seven(self):
        """ If strategies 1-6 fail, find an empty corner and play that. """
        self.game.board = [[' ',' ',' '],[' ','x',' '],[' ',' ',' ']]
        self.assertEqual((0, 0), self.player2.play())

    def test_strategy_eight(self):
        """ This one is tricky, it's hard to get in situation where you'd ever want to play a side. """
        self.game.board = [['x','o','x'],[' ','o',' '],['o','x','x']]
        self.assertEqual((1, 2), self.player2.play())


class TwoComputerPlayerTestCase(unittest.TestCase):
    """ Tests for the TicTacToeGame class. """

    def setUp(self):
        """ Set up a sample game for tests and intercept stdout. """
        self.std_out = sys.stdout
        sys.stdout = StringIO()

        self.game = TicTacToeGame()

    def tearDown(self):
        """ Set the world right. """
        sys.stdout = self.std_out

    def test_player_setup(self):
        """ Make sure that the game instance knows how to set up computer players. """
        self.assertTrue(isinstance(self.game.player1, ComputerPlayer))
        self.assertTrue(isinstance(self.game.player2, ComputerPlayer))

    def test_build_board(self):
        """ Make sure build_board() is behaving. Order of tests is important, this test assumes no plays have been made. """
        self.assertEqual(self.game.build_board(), " | | \n-----\n | | \n-----\n | | \nPlays: 0\n")
        self.assertEqual(self.game.build_board(echo=True), None)
        self.assertEqual(sys.stdout.getvalue().rstrip(), " | | \n-----\n | | \n-----\n | | \nPlays: 0")

        # TODO: test echo=True output like debug below

    def test_debug(self):
        """ Make sure debug output is working correctly. Maybe this should live in it's own test case. """
        TicTacToeGame(debug=True)
        self.assertEqual(
            sys.stdout.getvalue().strip(),
            "Computer Player 1 has joined the game!\nComputer Player 2 has joined the game!"
        )

    def test_game_is_over(self):
        """ Make sure that we can recognize when a game is over. """

        # test non-wins
        self.game.board = [[' ',' ',' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.assertFalse(self.game.game_is_over())
        self.game.board = [['x','o','x'], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.assertFalse(self.game.game_is_over())
        self.game.board = [['x',' ','x'], [' ', 'o', ' '], [' ', ' ', ' ']]
        self.assertFalse(self.game.game_is_over())

        # test row wins
        self.game.board = [['x','x','x'], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.assertTrue(self.game.game_is_over())
        self.game.board = [[' ', ' ', ' '], ['x','x','x'], [' ', ' ', ' ']]
        self.assertTrue(self.game.game_is_over())
        self.game.board = [[' ', ' ', ' '], [' ', ' ', ' '], ['x','x','x']]
        self.assertTrue(self.game.game_is_over())

        # test col wins
        self.game.board = [['x',' ',' '], ['x', ' ', ' '], ['x', ' ', ' ']]
        self.assertTrue(self.game.game_is_over())
        self.game.board = [[' ', 'x', ' '], [' ','x',' '], [' ', 'x', ' ']]
        self.assertTrue(self.game.game_is_over())
        self.game.board = [[' ', ' ', 'x'], [' ', ' ', 'x'], [' ',' ','x']]
        self.assertTrue(self.game.game_is_over())

        # test diagonal wins
        self.game.board = [['x', ' ', ' '], [' ','x',' '], [' ', ' ', 'x']]
        self.assertTrue(self.game.game_is_over())
        self.game.board = [[' ', ' ', 'x'], [' ', 'x', ' '], ['x',' ',' ']]
        self.assertTrue(self.game.game_is_over())


if __name__ == "__main__":
    unittest.main()
