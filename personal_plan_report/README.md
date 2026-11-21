# Personal Plan Report (Modular)

Multi-page Streamlit dashboard that reads your Google Sheet.

## Structure
- `app.py` — Home overview
- `pages/` — Weight, Calories, Study, Workouts, Milestones
- `utils.py` — Shared data loading and filters

## Setup
```bash
cp .env.example .env
pip install -r requirements.txt
streamlit run app.py
```

The sheet ID and GID stay in `.env`.
