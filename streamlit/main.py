import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import streamlit as st
import mplfinance as mpf


def get_data(ticker, start="2023-07-01", end=dt.datetime.today().strftime("%Y-%m-%d")):
    return yf.download(ticker, start="2023-07-01", end=end)


#def ema_crosses_ma(data):
#    # Download historical stock data
#    #
#
#    # Calculate 20-day EMA and 50-day MA
#    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
#    data["MA_50"] = data["Close"].rolling(window=50).mean()
#
#    # Find rows where EMA crosses MA (upward)
#    crosses_up = data[
#        (data["EMA_20"] > data["MA_50"])
#        & (data["EMA_20"].shift(1) < data["MA_50"].shift(1))
#    ]
#
#    # Find rows where EMA crosses MA (downward)
#    crosses_down = data[
#        (data["EMA_20"] < data["MA_50"])
#        & (data["EMA_20"].shift(1) > data["MA_50"].shift(1))
#    ]
#
#    # Print results
#    # print("Dates where 20EMA crosses above 50MA (upward):")
#    # print(crosses_up[["Close", "EMA_20", "MA_50"]])
#    # print("\nDates where 20EMA crosses below 50MA (downward):")
#    # print(crosses_down[["Close", "EMA_20", "MA_50"]])
#
#    return (
#        crosses_up[["Close", "EMA_20", "MA_50"]],
#        crosses_down[["Close", "EMA_20", "MA_50"]],
#    )
#
#
#def macd_crossovers(data):
#    df = data
#    short_ema = df["Close"].ewm(span=12, adjust=False).mean()
#    long_ema = df["Close"].ewm(span=26, adjust=False).mean()
#    macd_line = short_ema - long_ema
#    signal_line = macd_line.ewm(span=9, adjust=False).mean()
#    macd_histogram = macd_line - signal_line
#
#    # print(macd_line)
#    # print(signal_line)
#    # print(macd_histogram)
#    macd_above_signal = np.where(macd_line > signal_line, 1, 0)
#    macd_below_signal = np.where(macd_line < signal_line, 1, 0)
#
#    # Print the crossover points
#
#    bullish_crossovers = pd.DataFrame([df.index[i] for i in macd_above_signal])
#    bearish_crossovers = pd.DataFrame([df.index[i] for i in macd_below_signal])
#    # print("Bullish crossovers:", bullish_crossovers)
#    # print("Bearish crossovers:", bearish_crossovers)
#
#    return bullish_crossovers, bearish_crossovers

#apikey = st.secrets["polygon_api_key"]
#
#if apikey is None:
#    apikey = st.input("API key for polygon not provided. You can get one here: https://polygon.io/docs/stocks/getting-started")
#else:
#    "✅ API key loaded"
#
#client = RESTClient(api_key=apikey)


ticker = st.text_input("Enter a stock ticker", "AAPL")

start_col, end_col = st.columns(2)

with start_col:
    start_date = st.date_input("Start Date", dt.date.today() - relativedelta(years=1))
with end_col:
    end_date = st.date_input("End Date", dt.date.today())


data = get_data(ticker)

# Calculate EMAs (fast, slow, signal)
fast_ema = data["Adj Close"].ewm(span=12, min_periods=12).mean()
slow_ema = data["Adj Close"].ewm(span=26, min_periods=26).mean()
signal_ema = fast_ema.ewm(span=9, min_periods=9).mean()

# Calculate MACD and Signal line
macd = fast_ema - slow_ema
signal = signal_ema

# Highlight buy/sell signals
buy_signals = macd > signal  # When MACD crosses above signal line
sell_signals = macd < signal  # When MACD crosses below signal line


# Configure interactive plot
mcfg = {
    "type": "candle",
    "style": "yahoo",
    "volume": True,
    "mav": (fast_ema.name, slow_ema.name),
    "addplot": [
        {"type": "macd", "mav": (fast_ema.name, slow_ema.name), "color": "r", "width": 1},
        {"type": "bband", "period": 20, "std": 2},  # Bollinger Bands with window 20 and std 2
        {"scatter": buy_signals.index, "marker": "^", "color": "green", "size": 100},
        {"scatter": sell_signals.index, "marker": "v", "color": "red", "size": 100}
    ],
    "interactive": True  # Enable interactive elements
}


# Plot the chart
#x = mpf.plot(data, mcfg, #title=f"{ticker} Price Chart with Indicators ({start_date} - {end_date})")
x = mpf.plot(data, **mcfg)
st.write(x)
