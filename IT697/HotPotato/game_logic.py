from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
import random
from typing import Optional


ACTIVE = "Active"
ELIMINATED = "Eliminated"
DROPPED = "Dropped"
REMOVED = "Removed / Disqualified"


@dataclass
class Player:
    name: str
    status: str = ACTIVE
    elimination_order: Optional[int] = None


@dataclass
class GameState:
    max_number: int
    initial_count: int
    add_per_elimination: int
    entry_fee: Decimal
    player_percentage: Decimal
    house_percentage: Decimal
    players: list[Player]
    active_numbers: list[int] = field(default_factory=list)
    last_added_numbers: list[int] = field(default_factory=list)
    round_number: int = 0
    elimination_count: int = 0
    started: bool = False
    finished: bool = False
    winner_name: Optional[str] = None
    log: list[str] = field(default_factory=list)

    @property
    def eligible_players(self) -> list[Player]:
        return [p for p in self.players if p.status in (ACTIVE, ELIMINATED)]

    @property
    def active_players(self) -> list[Player]:
        return [p for p in self.players if p.status == ACTIVE]

    @property
    def paid_player_count(self) -> int:
        return len(self.eligible_players)

    @property
    def total_pot(self) -> Decimal:
        return money(self.entry_fee * self.paid_player_count)

    @property
    def winner_payout(self) -> Decimal:
        return money(self.total_pot * self.player_percentage / Decimal("100"))

    @property
    def house_payout(self) -> Decimal:
        return money(self.total_pot * self.house_percentage / Decimal("100"))

    @property
    def remainder(self) -> Decimal:
        # Backward-compatible alias used by older UI code.
        return self.house_payout


def money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def percent(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def validate_percentages(
    player_percentage: Decimal | int | float | str,
    house_percentage: Decimal | int | float | str,
) -> list[str]:
    player_pct = percent(player_percentage)
    house_pct = percent(house_percentage)
    errors: list[str] = []
    if player_pct < 0 or player_pct > 100:
        errors.append("Player percentage must be between 0 and 100.")
    if house_pct < 0 or house_pct > 100:
        errors.append("House percentage must be between 0 and 100.")
    if player_pct + house_pct != Decimal("100.00"):
        errors.append("Player and house percentages must total 100%.")
    return errors


def validate_setup(
    player_names: list[str],
    max_number: int,
    initial_count: int,
    add_per_elimination: int,
    entry_fee: Decimal | int | float | str,
    player_percentage: Decimal | int | float | str = 70,
    house_percentage: Decimal | int | float | str = 30,
) -> list[str]:
    errors: list[str] = []
    cleaned = [name.strip() for name in player_names if name.strip()]

    if not 2 <= len(cleaned) <= 25:
        errors.append("Enter between 2 and 25 player names.")
    if len({name.casefold() for name in cleaned}) != len(cleaned):
        errors.append("Player names must be unique.")
    if not 1 <= max_number <= 999:
        errors.append("Maximum roll number must be between 1 and 999.")
    if not 1 <= initial_count <= max_number:
        errors.append("Initial hot-potato count must be between 1 and the maximum roll number.")
    if add_per_elimination < 1:
        errors.append("Numbers added after an elimination must be at least 1.")
    if money(entry_fee) <= 0:
        errors.append("Entry fee must be greater than $0.00.")
    errors.extend(validate_percentages(player_percentage, house_percentage))
    return errors


def create_game(
    player_names: list[str],
    max_number: int,
    initial_count: int,
    add_per_elimination: int,
    entry_fee: Decimal | int | float | str,
    player_percentage: Decimal | int | float | str = 70,
    house_percentage: Decimal | int | float | str = 30,
    rng: random.Random | None = None,
) -> GameState:
    errors = validate_setup(
        player_names,
        max_number,
        initial_count,
        add_per_elimination,
        entry_fee,
        player_percentage,
        house_percentage,
    )
    if errors:
        raise ValueError(" ".join(errors))

    game = GameState(
        max_number=max_number,
        initial_count=initial_count,
        add_per_elimination=add_per_elimination,
        entry_fee=money(entry_fee),
        player_percentage=percent(player_percentage),
        house_percentage=percent(house_percentage),
        players=[Player(name.strip()) for name in player_names if name.strip()],
        started=True,
    )
    new_numbers = add_unique_numbers(game, initial_count, rng)
    game.round_number = 1
    game.last_added_numbers = new_numbers
    game.log.append(
        f"Game started with {len(game.players)} players at ${game.entry_fee:.2f} each. "
        f"Split: {game.player_percentage:.2f}% player / {game.house_percentage:.2f}% house."
    )
    game.log.append(f"Round 1 initial hot potato numbers: {format_numbers(new_numbers)}")
    return game


def add_unique_numbers(
    game: GameState, requested_count: int, rng: random.Random | None = None
) -> list[int]:
    rng = rng or random.SystemRandom()
    available = sorted(set(range(1, game.max_number + 1)) - set(game.active_numbers))
    count = min(requested_count, len(available))
    selected = sorted(rng.sample(available, count)) if count else []
    game.active_numbers = sorted(game.active_numbers + selected)
    game.last_added_numbers = selected
    return selected


def check_roll(game: GameState, player_name: str, roll: int) -> bool:
    player = next((p for p in game.players if p.name == player_name), None)
    if player is None:
        raise ValueError("Player was not found.")
    if player.status != ACTIVE:
        raise ValueError(f"{player.name} is already marked as {player.status}.")
    if game.finished:
        raise ValueError("The game is already finished.")
    if not 1 <= roll <= game.max_number:
        raise ValueError(f"Roll must be between 1 and {game.max_number}.")

    is_hot = roll in game.active_numbers
    result = "HOT POTATO" if is_hot else "safe"
    game.log.append(f"{player.name} rolled {roll} — {result}.")
    return is_hot


def mark_player(
    game: GameState,
    player_name: str,
    outcome: str,
    rng: random.Random | None = None,
) -> list[int]:
    player = next((p for p in game.players if p.name == player_name), None)
    if player is None:
        raise ValueError("Player was not found.")
    if player.status != ACTIVE:
        raise ValueError(f"{player.name} is already marked as {player.status}.")
    if game.finished:
        raise ValueError("The game is already finished.")
    if outcome not in (ELIMINATED, DROPPED, REMOVED):
        raise ValueError("Invalid player outcome.")

    player.status = outcome
    added: list[int] = []

    if outcome == ELIMINATED:
        game.elimination_count += 1
        player.elimination_order = game.elimination_count
        game.log.append(f"{player.name} was eliminated.")
        game.round_number += 1
        added = add_unique_numbers(game, game.add_per_elimination, rng)
        if added:
            game.log.append(
                f"Round {game.round_number} new hot potato numbers: {format_numbers(added)}"
            )
        else:
            game.log.append(f"Round {game.round_number}: no unused numbers remained to add.")
    elif outcome == DROPPED:
        game.log.append(
            f"{player.name} dropped due to connectivity and was removed from the pot."
        )
    else:
        game.log.append(
            f"{player.name} was removed/disqualified and was removed from the pot."
        )

    determine_winner(game)
    return added


def determine_winner(game: GameState) -> Optional[str]:
    active = game.active_players
    if len(active) == 1:
        game.finished = True
        game.winner_name = active[0].name
        game.log.append(
            f"{game.winner_name} won ${game.winner_payout:.2f} from a ${game.total_pot:.2f} pot. "
            f"House receives ${game.house_payout:.2f}."
        )
        return game.winner_name
    if len(active) == 0:
        game.finished = True
        game.winner_name = None
        game.log.append("The game ended with no active players and no winner.")
    return None


def update_settings(
    game: GameState,
    max_number: int,
    add_per_elimination: int,
    entry_fee: Decimal | int | float | str,
    player_percentage: Decimal | int | float | str,
    house_percentage: Decimal | int | float | str,
) -> None:
    if max_number < max(game.active_numbers, default=0):
        raise ValueError(
            "The maximum number cannot be lower than an already-active hot potato number."
        )
    if not 1 <= max_number <= 999:
        raise ValueError("Maximum roll number must be between 1 and 999.")
    if add_per_elimination < 1:
        raise ValueError("Numbers added after an elimination must be at least 1.")
    if money(entry_fee) <= 0:
        raise ValueError("Entry fee must be greater than $0.00.")
    percentage_errors = validate_percentages(player_percentage, house_percentage)
    if percentage_errors:
        raise ValueError(" ".join(percentage_errors))

    old = (
        game.max_number,
        game.add_per_elimination,
        game.entry_fee,
        game.player_percentage,
        game.house_percentage,
    )
    game.max_number = max_number
    game.add_per_elimination = add_per_elimination
    game.entry_fee = money(entry_fee)
    game.player_percentage = percent(player_percentage)
    game.house_percentage = percent(house_percentage)
    game.log.append(
        "Game settings edited: "
        f"range 1-{old[0]} → 1-{game.max_number}, "
        f"add count {old[1]} → {game.add_per_elimination}, "
        f"entry fee ${old[2]:.2f} → ${game.entry_fee:.2f}, "
        f"split {old[3]:.2f}/{old[4]:.2f} → "
        f"{game.player_percentage:.2f}/{game.house_percentage:.2f}."
    )


def format_numbers(numbers: list[int]) -> str:
    return ", ".join(str(number) for number in sorted(numbers))


def announcement(game: GameState) -> str:
    label = "initial" if game.round_number == 1 else "new"
    return (
        f"The {label} hot potato numbers for this round are: "
        f"{format_numbers(game.last_added_numbers)}"
    )
