from decimal import Decimal
import random
import unittest

from game_logic import (
    ACTIVE,
    DROPPED,
    ELIMINATED,
    REMOVED,
    create_game,
    mark_player,
    update_settings,
)


class HotPotatoTests(unittest.TestCase):
    def test_numbers_are_unique_and_retained(self):
        game = create_game(
            ["A", "B", "C"],
            max_number=100,
            initial_count=25,
            add_per_elimination=5,
            entry_fee=10,
            rng=random.Random(1),
        )
        first = set(game.active_numbers)
        mark_player(game, "A", ELIMINATED, rng=random.Random(2))
        self.assertEqual(len(game.active_numbers), 30)
        self.assertTrue(first.issubset(set(game.active_numbers)))
        self.assertEqual(len(game.active_numbers), len(set(game.active_numbers)))

    def test_eliminated_player_stays_in_pot(self):
        game = create_game(["A", "B", "C"], 50, 5, 2, 10, random.Random(1))
        mark_player(game, "A", ELIMINATED, random.Random(2))
        self.assertEqual(game.total_pot, Decimal("30.00"))

    def test_dropout_is_removed_from_pot(self):
        game = create_game(["A", "B", "C"], 50, 5, 2, 10, random.Random(1))
        mark_player(game, "A", DROPPED)
        self.assertEqual(game.total_pot, Decimal("20.00"))

    def test_removed_player_is_removed_from_pot(self):
        game = create_game(["A", "B", "C"], 50, 5, 2, 10, random.Random(1))
        mark_player(game, "A", REMOVED)
        self.assertEqual(game.total_pot, Decimal("20.00"))

    def test_winner_is_declared(self):
        game = create_game(["A", "B"], 50, 5, 2, 10, random.Random(1))
        mark_player(game, "A", ELIMINATED, random.Random(2))
        self.assertTrue(game.finished)
        self.assertEqual(game.winner_name, "B")
        self.assertEqual(game.winner_payout, Decimal("14.00"))

    def test_cannot_reduce_range_below_active_number(self):
        game = create_game(["A", "B"], 50, 5, 2, 10, random.Random(1))
        with self.assertRaises(ValueError):
            update_settings(game, max(game.active_numbers) - 1, 2, 10)


if __name__ == "__main__":
    unittest.main()
