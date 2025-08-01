import streamlit as st
import requests
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from fuzzywuzzy import process

# 1. Fetch Item Mapping
@st.cache_data
def fetch_item_mapping():
    """
    Fetch item ID mapping from OSRS Wiki API.
    Returns:
        pd.DataFrame: Item names, IDs, and high alch values.
    """
    url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
    headers = {'User-Agent': 'OSRS Price Predictor marcbullock22@gmail.com'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Error fetching item mapping: {e}")
        return None

# 2. Data Collection
def fetch_osrs_data(item_id, item_name, timestep='1h', days=180):
    """
    Fetch historical price data for an OSRS item.
    Args:
        item_id (int): Item ID from mapping.
        item_name (str): Item name for display.
        timestep (str): Time interval ('5m', '1h', '6h').
        days (int): Number of days to fetch.
    Returns:
        pd.DataFrame: Data with timestamp, price, volume, and features, or None if failed.
    """
    url = f"https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep={timestep}&id={item_id}"
    headers = {'User-Agent': 'OSRS Price Predictor marcbullock22@gmail.com'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()['data']
        if not data:
            st.error(f"No data returned for {item_name} (ID: {item_id})")
            return None
    except Exception as e:
        st.error(f"Error fetching data for {item_name} (ID: {item_id}): {e}")
        return None
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df[['timestamp', 'avgHighPrice', 'highPriceVolume']]
    df.columns = ['timestamp', 'price', 'volume']
    df = df[df['timestamp'] >= datetime.now() - timedelta(days=days)]
    
    # Feature Engineering
    df['price_lag1'] = df['price'].shift(1)
    df['price_lag7'] = df['price'].shift(7)
    df['returns'] = df['price'].pct_change(fill_method=None)
    df['volatility'] = df['returns'].rolling(window=7).std()
    df = df.dropna()
    
    if len(df) < 50:
        st.warning(f"Insufficient data for {item_name}: {len(df)} samples")
        return None
    
    return df

# 3. Preprocess Data
def preprocess_data(df, sequence_length=10):
    """
    Prepare data for LSTM: scale and create sequences.
    Args:
        df (pd.DataFrame): Price, volume, and feature data.
        sequence_length (int): Number of time steps for LSTM input.
    Returns:
        X_train, X_test, y_train, y_test, scaler: Training data and scaler.
    """
    features = ['price', 'volume', 'price_lag1', 'price_lag7', 'volatility']
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[features])
    
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i])
        y.append(scaled_data[i, 0])  # Predict next price
    X, y = np.array(X), np.array(y)
    
    train_size = int(0.8 * len(X))
    if train_size < 10 or len(X) - train_size < 10:
        st.warning("Not enough data for train/test split")
        return None, None, None, None, None
    
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    return X_train, X_test, y_train, y_test, scaler

# 4. Build LSTM Model
def build_lstm_model(sequence_length, n_features=5):
    """
    Create an LSTM model for price prediction.
    Args:
        sequence_length (int): Number of time steps.
        n_features (int): Number of features.
    Returns:
        keras.Model: Compiled LSTM model.
    """
    model = Sequential([
        Input(shape=(sequence_length, n_features)),
        LSTM(50, activation='relu', return_sequences=True),
        LSTM(50, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# 5. Calculate Profit
def calculate_profit(suggested_buy_price, suggested_sell_price, trade_units):
    """
    Calculate profit for flipping based on suggested buy/sell prices.
    Args:
        suggested_buy_price (float): Current price to buy.
        suggested_sell_price (float): Predicted price to sell.
        trade_units (int): Number of units to trade (up to buy limit).
    Returns:
        tuple: Profit per unit and total profit in GP after 1% GE tax.
    """
    profit_per_unit = suggested_sell_price - suggested_buy_price
    total_profit = profit_per_unit * trade_units * 0.99  # 1% GE tax
    return profit_per_unit, max(total_profit, 0)

# 6. Train, Evaluate, and Plot
def train_and_evaluate(item_id, item_name, buy_limit=1000, margin_threshold=3.0, trade_units=None):
    """
    Fetch data, train model, evaluate, and plot results for an item.
    Args:
        item_id (int): Item ID.
        item_name (str): Item name.
        buy_limit (int): GE buy limit.
        margin_threshold (float): Profit margin threshold for recommendation.
        trade_units (int): Number of units to trade (default: 10 for high-price items).
    Returns:
        tuple: Matplotlib figure and results dictionary.
    """
    df = fetch_osrs_data(item_id, item_name, timestep='1h', days=180)
    if df is None:
        return None, None
    
    sequence_length = 10
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df, sequence_length)
    if X_train is None:
        return None, None
    
    model = build_lstm_model(sequence_length, n_features=5)
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=0)
    
    y_pred = model.predict(X_test, verbose=0)
    
    dummy = np.zeros((len(y_test), 4))
    y_test_input = np.hstack((y_test.reshape(-1, 1), dummy))
    y_pred_input = np.hstack((y_pred, dummy))
    
    y_test_inv = scaler.inverse_transform(y_test_input)[:, 0]
    y_pred_inv = scaler.inverse_transform(y_pred_input)[:, 0]
    
    mse = np.mean((y_test_inv - y_pred_inv) ** 2)
    
    last_price = df['price'].iloc[-1]  # Suggested buy price
    pred_price = y_pred_inv[-1]  # Suggested sell price
    profit_margin = (pred_price - last_price) / last_price * 100
    
    # Default trade units: 10 for high-price items (>100,000 GP), else use buy limit
    if trade_units is None:
        trade_units = 1 if last_price > 100000 else buy_limit
    
    # Calculate profit
    profit_per_unit, total_profit = calculate_profit(last_price, pred_price, trade_units)
    
    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(y_test_inv, label='Actual Price', color='blue')
    ax1.plot(y_pred_inv, label='Predicted Price', color='orange')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price (GP)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    buy_signals = np.where((y_pred_inv[1:] > y_test_inv[:-1] * 1.015), 1, 0)  # 1.5% threshold
    buy_indices = np.where(buy_signals)[0]
    ax1.scatter(buy_indices, y_pred_inv[buy_indices], color='green', label='Buy Signal', marker='^', s=100)
    ax1.legend(loc='upper left')
    
    ax2 = ax1.twinx()
    ax2.plot(df['volume'].iloc[-len(y_test_inv):], label='Trade Volume', color='purple', alpha=0.5)
    ax2.set_ylabel('Volume', color='purple')
    ax2.tick_params(axis='y', labelcolor='purple')
    ax2.legend(loc='upper right')
    
    plt.title(f'Price Prediction and Volume for {item_name}')
    plt.tight_layout()
    return fig, {
        'item_name': item_name,
        'profit_margin': profit_margin,
        'total_profit': total_profit,
        'mse': mse,
        'suggested_buy_price': last_price,
        'suggested_sell_price': pred_price,
        'profit_per_unit': profit_per_unit,
        'trade_units': trade_units
    }

# 7. Streamlit App
def main():
    """
    Streamlit app with search bar for OSRS item price prediction.
    """
    st.title("OSRS Item Price Predictor")
    st.write("Search for an item to predict its price and merching potential.")
    
    # Profit margin threshold slider
    margin_threshold = st.slider("Select profit margin threshold for recommendation (%):", 
                                min_value=1.0, max_value=10.0, value=3.0, step=0.5)
    
    # Fetch item mapping
    item_mapping = fetch_item_mapping()
    if item_mapping is None:
        return
    
    item_names = item_mapping['name'].tolist()
    
    # Search bar with fuzzy matching
    search_query = st.text_input("Enter item name (e.g., Abyssal whip):")
    if search_query:
        matches = process.extract(search_query, item_names, limit=5)
        matched_names = [match[0] for match in matches]
        selected_item = st.selectbox("Select an item:", matched_names)
    else:
        selected_item = st.selectbox("Select an item:", item_names)
    
    # Get item details
    item_row = item_mapping[item_mapping['name'] == selected_item]
    if not item_row.empty:
        item_id = item_row['id'].iloc[0]
        buy_limit = item_row.get('limit', 1000).iloc[0]  # Default to 1000 if no limit
        st.write(f"Analyzing {selected_item} (ID: {item_id}, Buy Limit: {buy_limit})...")
        
        # Check data availability before setting default units
        temp_data = fetch_osrs_data(item_id, selected_item)
        if temp_data is None:
            st.error(f"Cannot proceed with analysis for {selected_item} due to data unavailability.")
            return
        default_units = 1 if temp_data['price'].iloc[-1] > 100000 else buy_limit
        
        # Input for number of units to trade
        trade_units = st.number_input(f"Number of units to trade (max {buy_limit}):", 
                                     min_value=1, max_value=int(buy_limit), value=int(default_units))
        
        # Run analysis
        fig, result = train_and_evaluate(item_id, selected_item, buy_limit, margin_threshold, trade_units)
        if result:
            st.write(f"**MSE**: {result['mse']:.2f} GP²")
            st.write(f"**Predicted Profit Margin**: {result['profit_margin']:.2f}%")
            st.write(f"**Suggested Buy Price**: {result['suggested_buy_price']:.2f} GP")
            st.write(f"**Suggested Sell Price**: {result['suggested_sell_price']:.2f} GP")
            st.write(f"**Profit per Unit**: {result['profit_per_unit']:.2f} GP")
            st.write(f"**Total Profit (One Flip, {result['trade_units']} units)**: {result['total_profit']:.2f} GP")
            
            avg_volume = temp_data['volume'].mean()
            is_high_volume = avg_volume > 10000  # High-volume threshold
            final_threshold = 3.0 if is_high_volume else margin_threshold
            
            if result['profit_margin'] > final_threshold and result['total_profit'] > 0:
                st.success(f"Recommend: Buy {selected_item} for flipping!")
            else:
                st.warning(f"{selected_item} may not be ideal for merching.")
            
            st.pyplot(fig)
    
    st.write("Note: Use suggested buy/sell prices as a guide. Check GE Tracker or OSRS Wiki for real-time prices.")

if __name__ == '__main__':
    main()