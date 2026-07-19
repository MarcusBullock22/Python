# OSRS Item Price Predictor

A machine learning-powered Streamlit app that predicts Old School RuneScape (OSRS) item prices and recommends profitable flips, helping players maximize Grand Exchange merching opportunities.

## Features

- **Live OSRS Data**: Pulls real-time item prices and trade volumes from the official OSRS Wiki API.
- **LSTM Price Prediction**: Uses a neural network to forecast future item prices.
- **Profitability Analysis**: Calculates expected margins and total profits after Grand Exchange tax.
- **Trade Recommendations**: Flags high-margin, high-volume items for flipping.
- **Interactive Search**: Fuzzy item search and filtering by profit margin thresholds.
- **Visual Insights**: Plots predicted vs. actual prices with buy/sell signals and trade volumes.

## Tech Stack

- **Languages**: Python
- **Frameworks**: Streamlit, TensorFlow/Keras
- **Libraries**: Pandas, NumPy, scikit-learn, Matplotlib, fuzzywuzzy, Requests
- **Data Source**: [OSRS Wiki API](https://prices.runescape.wiki/)
- **Model Type**: LSTM (Long Short-Term Memory) neural network

## How It Works

1. **Search an Item**: Use the search bar to find any tradable OSRS item.
2. **Fetch Data**: Pulls 180 days of historical prices and volumes from the OSRS Wiki API.
3. **Feature Engineering**: Generates lag prices, returns, and volatility indicators.
4. **Train Model**: Fits an LSTM model to predict short-term price movements.
5. **Calculate Profits**: Estimates margins and total profit after GE tax for a chosen quantity.
6. **Show Recommendations**: Displays profitability metrics and a recommendation badge.
7. **Visualize**: Plots predicted prices, actual prices, buy signals, and trade volumes.

## Potential Use Cases

- Flipping items on the Grand Exchange
- Identifying low-risk, high-volume merching targets
- Price trend analysis for long-term investing
- Testing data science models on gaming economics
