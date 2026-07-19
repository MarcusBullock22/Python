# Hot Potato Game Manager

A Streamlit app for managing a cumulative hot-potato elimination game.

## Included rules and features

- Supports 2–25 players.
- Configurable roll range from 1–999.
- Unique initial numbers that remain active for the entire game.
- Configurable new numbers after every elimination.
- Fixed entry fee.
- Configurable player and house percentages that must total 100%.
- Eliminated players remain in the pot.
- Connectivity dropouts and removed/disqualified players are removed from the pot.
- Choose an outcome once, then click a player's name directly to apply it.
- Automatic payout recalculation and winner declaration.
- Copyable round announcements showing only newly generated numbers.
- Full game log and downloadable JSON record.
- In-game setting edits and reset confirmation warnings.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
python -m unittest test_game_logic.py
```
