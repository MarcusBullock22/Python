from decimal import Decimal
import random
import unittest

from game_logic import (
    DROPPED,
    ELIMINATED,
    REMOVED,
    check_roll,
    create_game,
    mark_player,
    update_settings,
)


class HotPotatoTests(unittest.TestCase):
    def test_numbers_are_unique_and_retained(self):
        game = create_game(["A", "B", "C"], 100, 25, 5, 10, rng=random.Random(1))
        first = set(game.active_numbers)
        mark_player(game, "A", ELIMINATED, random.Random(2))
        self.assertEqual(len(game.active_numbers), 30)
        self.assertTrue(first.issubset(set(game.active_numbers)))
        self.assertEqual(len(game.active_numbers), len(set(game.active_numbers)))

    def test_roll_check(self):
        game = create_game(["A", "B"], 50, 5, 2, 10, rng=random.Random(1))
        hot_number = game.active_numbers[0]
        safe_number = next(n for n in range(1, 51) if n not in game.active_numbers)
        self.assertTrue(check_roll(game, "A", hot_number))
        self.assertFalse(check_roll(game, "B", safe_number))

    def test_custom_split(self):
        game = create_game(["A", "B", "C"], 50, 5, 2, 10, 60, 40, random.Random(1))
        self.assertEqual(game.total_pot, Decimal("30.00"))
        self.assertEqual(game.winner_payout, Decimal("18.00"))
        self.assertEqual(game.house_payout, Decimal("12.00"))

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

    def test_winner_is_declared(self):
        game = create_game(["A", "B"], 50, 5, 2, 10, rng=random.Random(1))
        mark_player(game, "A", ELIMINATED, random.Random(2))
        self.assertTrue(game.finished)
        self.assertEqual(game.winner_name, "B")
        self.assertEqual(game.winner_payout, Decimal("14.00"))

    def test_percentage_must_total_100(self):
        with self.assertRaises(ValueError):
            create_game(["A", "B"], 50, 5, 2, 10, 70, 20, random.Random(1))

    def test_edit_percentages(self):
        game = create_game(["A", "B"], 50, 5, 2, 10, rng=random.Random(1))
        update_settings(game, 50, 2, 10, 65, 35)
        self.assertEqual(game.player_percentage, Decimal("65.00"))
        self.assertEqual(game.house_percentage, Decimal("35.00"))


if __name__ == "__main__":
    unittest.main()
