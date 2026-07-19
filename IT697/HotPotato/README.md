# Hot Potato Game Manager

A Streamlit app for managing a cumulative hot-potato elimination game.

## Included rules

- Supports 2–25 players.
- Uses a configurable roll range from 1–999.
- Generates a configurable number of unique initial hot-potato numbers.
- Retains every prior hot-potato number throughout the game.
- Adds configurable new unique numbers after each elimination.
- Uses a fixed entry fee for all players.
- Eliminated players remain in the pot.
- Connectivity dropouts and removed/disqualified players are removed from the pot.
- Automatically recalculates the total pot and 70% winner payout.
- Maintains fixed player order in the player table.
- Provides a copyable announcement containing only the newly generated numbers.
- Keeps a complete game log.
- Automatically declares the final active player the winner.
- Allows in-game setting edits after a confirmation warning.
- Exports the completed game record as JSON.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the app:

```bash
streamlit run app.py
```

Streamlit will open the app in your browser.

## Run tests

```bash
python -m unittest test_game_logic.py
```

## Important payout behavior

An eliminated player's entry stays in the pot. A player marked as a connectivity dropout or removed/disqualified is removed from the pot, so the pot and winner payout recalculate immediately.
