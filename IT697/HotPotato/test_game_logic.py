from decimal import Decimal
import random
import unittest

from game_logic import (
    DROPPED,
    ELIMINATED,
    REMOVED,
    create_game,
    mark_player,
    update_settings,
    validate_percentages,
)


class HotPotatoTests(unittest.TestCase):
    def test_numbers_are_unique_and_retained(self):
        game = create_game(["A", "B", "C"], 100, 25, 5, 10, rng=random.Random(1))
        first = set(game.active_numbers)
        mark_player(game, "A", ELIMINATED, rng=random.Random(2))
        self.assertEqual(len(game.active_numbers), 30)
        self.assertTrue(first.issubset(set(game.active_numbers)))
        self.assertEqual(len(game.active_numbers), len(set(game.active_numbers)))

    def test_eliminated_player_stays_in_pot(self):
        game = create_game(["A", "B", "C"], 50, 5, 2, 10, rng=random.Random(1))
        mark_player(game, "A", ELIMINATED, random.Random(2))
        self.assertEqual(game.total_pot, Decimal("30.00"))

    def test_dropout_is_removed_from_pot(self):
        game = create_game(["A", "B", "C"], 50, 5, 2, 10, rng=random.Random(1))
        mark_player(game, "A", DROPPED)
        self.assertEqual(game.total_pot, Decimal("20.00"))

    def test_removed_player_is_removed_from_pot(self):
        game = create_game(["A", "B", "C"], 50, 5, 2, 10, rng=random.Random(1))
        mark_player(game, "A", REMOVED)
        self.assertEqual(game.total_pot, Decimal("20.00"))

    def test_custom_split(self):
        game = create_game(
            ["A", "B"], 50, 5, 2, 10, 60, 40, rng=random.Random(1)
        )
        self.assertEqual(game.winner_payout, Decimal("12.00"))
        self.assertEqual(game.house_payout, Decimal("8.00"))

    def test_invalid_split(self):
        self.assertTrue(validate_percentages(70, 20))
        self.assertFalse(validate_percentages(65, 35))

    def test_winner_is_declared(self):
        game = create_game(["A", "B"], 50, 5, 2, 10, rng=random.Random(1))
        mark_player(game, "A", ELIMINATED, random.Random(2))
        self.assertTrue(game.finished)
        self.assertEqual(game.winner_name, "B")
        self.assertEqual(game.winner_payout, Decimal("14.00"))

    def test_edit_split(self):
        game = create_game(["A", "B"], 50, 5, 2, 10, rng=random.Random(1))
        update_settings(game, 50, 2, 10, 55, 45)
        self.assertEqual(game.player_percentage, Decimal("55.00"))
        self.assertEqual(game.house_percentage, Decimal("45.00"))


if __name__ == "__main__":
    unittest.main()
