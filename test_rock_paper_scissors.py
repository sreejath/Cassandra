import unittest
from unittest.mock import patch, call
from io import StringIO
import random
from rock_paper_scissors import (
    get_computer_choice,
    determine_winner,
    play_round,
    main
)


class TestGetComputerChoice(unittest.TestCase):
    """Tests for the computer choice function."""

    def test_computer_choice_is_valid(self):
        """Computer choice should always be one of the three valid options."""
        valid_choices = ['rock', 'paper', 'scissors']
        for _ in range(20):
            choice = get_computer_choice()
            self.assertIn(choice, valid_choices)

    def test_computer_choice_randomness(self):
        """Computer should produce different choices (statistically)."""
        choices = [get_computer_choice() for _ in range(100)]
        unique_choices = set(choices)
        # Should have at least 2 different choices in 100 attempts
        self.assertGreaterEqual(len(unique_choices), 2)


class TestDetermineWinner(unittest.TestCase):
    """Tests for the winner determination logic."""

    def test_human_wins_rock_beats_scissors(self):
        """Rock should beat scissors."""
        result = determine_winner('rock', 'scissors')
        self.assertEqual(result, 1)

    def test_human_wins_paper_beats_rock(self):
        """Paper should beat rock."""
        result = determine_winner('paper', 'rock')
        self.assertEqual(result, 1)

    def test_human_wins_scissors_beats_paper(self):
        """Scissors should beat paper."""
        result = determine_winner('scissors', 'paper')
        self.assertEqual(result, 1)

    def test_computer_wins_rock_beats_scissors(self):
        """Rock should beat scissors (computer perspective)."""
        result = determine_winner('scissors', 'rock')
        self.assertEqual(result, -1)

    def test_computer_wins_paper_beats_rock(self):
        """Paper should beat rock (computer perspective)."""
        result = determine_winner('rock', 'paper')
        self.assertEqual(result, -1)

    def test_computer_wins_scissors_beats_paper(self):
        """Scissors should beat paper (computer perspective)."""
        result = determine_winner('paper', 'scissors')
        self.assertEqual(result, -1)

    def test_tie_rock_vs_rock(self):
        """Same choices should result in a tie."""
        result = determine_winner('rock', 'rock')
        self.assertEqual(result, 0)

    def test_tie_paper_vs_paper(self):
        """Same choices should result in a tie."""
        result = determine_winner('paper', 'paper')
        self.assertEqual(result, 0)

    def test_tie_scissors_vs_scissors(self):
        """Same choices should result in a tie."""
        result = determine_winner('scissors', 'scissors')
        self.assertEqual(result, 0)

    def test_all_possible_outcomes(self):
        """Test all 9 possible combinations."""
        choices = ['rock', 'paper', 'scissors']
        expected_results = {
            ('rock', 'rock'): 0,
            ('rock', 'paper'): -1,
            ('rock', 'scissors'): 1,
            ('paper', 'rock'): 1,
            ('paper', 'paper'): 0,
            ('paper', 'scissors'): -1,
            ('scissors', 'rock'): -1,
            ('scissors', 'paper'): 1,
            ('scissors', 'scissors'): 0,
        }

        for (human, computer), expected in expected_results.items():
            with self.subTest(human=human, computer=computer):
                result = determine_winner(human, computer)
                self.assertEqual(result, expected)


class TestPlayRound(unittest.TestCase):
    """Tests for the play_round function."""

    @patch('builtins.print')
    def test_play_round_human_win(self, mock_print):
        """Test play_round displays correct output for human win."""
        result = play_round('rock', 'scissors')
        self.assertEqual(result, 1)
        # Check that output messages were printed
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('rock', output.lower())
        self.assertIn('scissors', output.lower())
        self.assertIn('win', output.lower())

    @patch('builtins.print')
    def test_play_round_computer_win(self, mock_print):
        """Test play_round displays correct output for computer win."""
        result = play_round('rock', 'paper')
        self.assertEqual(result, -1)
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('computer', output.lower())

    @patch('builtins.print')
    def test_play_round_tie(self, mock_print):
        """Test play_round displays correct output for tie."""
        result = play_round('rock', 'rock')
        self.assertEqual(result, 0)
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('tie', output.lower())

    @patch('builtins.print')
    def test_play_round_returns_correct_value(self, mock_print):
        """Play round should return result from determine_winner."""
        test_cases = [
            ('rock', 'scissors', 1),
            ('rock', 'paper', -1),
            ('paper', 'paper', 0),
        ]
        for human, computer, expected in test_cases:
            with self.subTest(human=human, computer=computer):
                result = play_round(human, computer)
                self.assertEqual(result, expected)


class TestMainGameFlow(unittest.TestCase):
    """Tests for the main game loop."""

    @patch('rock_paper_scissors.get_computer_choice')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_human_wins_match(self, mock_print, mock_input, mock_computer_choice):
        """Test game ends when human reaches 5 wins."""
        # Simulate human winning 5 times
        mock_input.side_effect = ['rock', 'rock', 'rock', 'rock', 'rock']
        mock_computer_choice.side_effect = ['scissors', 'scissors', 'scissors', 'scissors', 'scissors']

        main()

        # Check that congratulations message was printed
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('congratulations', output.lower())

    @patch('rock_paper_scissors.get_computer_choice')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_computer_wins_match(self, mock_print, mock_input, mock_computer_choice):
        """Test game ends when computer reaches 5 wins."""
        # Simulate computer winning 5 times
        mock_input.side_effect = ['rock', 'rock', 'rock', 'rock', 'rock']
        mock_computer_choice.side_effect = ['paper', 'paper', 'paper', 'paper', 'paper']

        main()

        # Check that computer win message was printed
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('computer wins', output.lower())

    @patch('rock_paper_scissors.get_computer_choice')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_game_with_ties(self, mock_print, mock_input, mock_computer_choice):
        """Test that ties don't affect the win counter."""
        # Mix ties and wins
        mock_input.side_effect = [
            'rock', 'rock', 'rock',  # tie, win, win
            'rock', 'rock', 'rock', 'rock', 'rock'  # tie, win, win, win, win
        ]
        mock_computer_choice.side_effect = [
            'rock', 'scissors', 'scissors',  # tie, human wins, human wins
            'rock', 'scissors', 'scissors', 'scissors', 'scissors'  # tie, then 4 more human wins
        ]

        main()

        # Human should reach 5 wins (with 2 ties in between)
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('congratulations', output.lower())

    @patch('rock_paper_scissors.get_computer_choice')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_input_validation(self, mock_print, mock_input, mock_computer_choice):
        """Test that invalid input is rejected and re-prompted."""
        # Invalid input followed by valid input (enough to finish game)
        mock_input.side_effect = [
            'invalid', 'ROCK', 'rock', 'rock', 'rock', 'rock', 'rock'
        ]
        mock_computer_choice.side_effect = ['scissors'] * 6

        main()

        # Check that "Invalid choice" message was printed
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('invalid', output.lower())

    @patch('rock_paper_scissors.get_computer_choice')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_case_insensitive_input(self, mock_print, mock_input, mock_computer_choice):
        """Test that input is case-insensitive."""
        # Provide uppercase, mixed case, and lowercase inputs
        mock_input.side_effect = ['ROCK', 'PaPeR', 'sCiSSoRS', 'ROCK', 'rock', 'SCISSORS']
        mock_computer_choice.side_effect = ['scissors', 'rock', 'paper', 'scissors', 'scissors', 'rock']

        main()

        # Game should complete successfully (human should win with paper, scissors, rock, scissors, scissors)
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        # Check game ended - either congratulations or computer wins
        self.assertTrue('game over' in output.lower() or 'congratulations' in output.lower() or 'computer wins' in output.lower())

    @patch('rock_paper_scissors.get_computer_choice')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_score_tracking(self, mock_print, mock_input, mock_computer_choice):
        """Test that scores are tracked correctly throughout the game."""
        # Alternate wins: human, computer, human, computer, human, computer, human, human, human, human
        mock_input.side_effect = ['rock', 'rock', 'rock', 'rock', 'rock', 'rock', 'rock', 'rock', 'rock', 'rock']
        mock_computer_choice.side_effect = [
            'scissors',  # human wins (1-0)
            'rock',      # computer wins (1-1)
            'scissors',  # human wins (2-1)
            'rock',      # computer wins (2-2)
            'scissors',  # human wins (3-2)
            'rock',      # computer wins (3-3)
            'scissors',  # human wins (4-3)
            'scissors',  # human wins (5-3)
            'scissors',  # human wins (would be 6-3)
            'scissors',  # human wins (would be 7-3)
        ]

        main()

        # Game should end when human reaches 5 wins
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('congratulations', output.lower())


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""

    def test_determine_winner_with_all_choices(self):
        """Ensure all choice combinations are valid."""
        valid_choices = ['rock', 'paper', 'scissors']
        for human in valid_choices:
            for computer in valid_choices:
                result = determine_winner(human, computer)
                self.assertIn(result, [-1, 0, 1])

    @patch('rock_paper_scissors.get_computer_choice')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_exact_5_win_boundary(self, mock_print, mock_input, mock_computer_choice):
        """Test that game ends exactly at 5 wins, not before or after."""
        mock_input.side_effect = ['rock'] * 5
        mock_computer_choice.side_effect = ['scissors'] * 5

        main()

        # Should end exactly at 5-0
        calls = mock_print.call_args_list
        output = ' '.join([str(call) for call in calls])
        self.assertIn('5', output)
        self.assertIn('0', output)


if __name__ == '__main__':
    unittest.main()
