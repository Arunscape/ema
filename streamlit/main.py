import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import streamlit as st
import altair as alt



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

data

# Calculate EMAs (fast, slow, signal)
fast_ema = data["Adj Close"].ewm(span=12, min_periods=12).mean()
slow_ema = data["Adj Close"].ewm(span=26, min_periods=26).mean()
signal_ema = fast_ema.ewm(span=9, min_periods=9).mean()


# Calculate MACD and Signal line
macd = fast_ema - slow_ema

# Highlight buy/sell signals
buy_signals = macd > signal_ema  # When MACD crosses above signal line
sell_signals = macd < signal_ema  # When MACD crosses below signal line


# Calculate Bollinger Bands (replace with your calculation if different)
data['Upper Band'] = data['Adj Close'].rolling(window=20).mean() + 2 * data['Adj Close'].rolling(window=20).std()
data['Lower Band'] = data['Adj Close'].rolling(window=20).mean() - 2 * data['Adj Close'].rolling(window=20).std()


# Data preparation for Altair
base = alt.Chart(data).transform_fold(fold=['Fast EMA', 'Slow EMA', 'MACD', 'Upper Band', 'Lower Band'], as_=['value', 'Indicator'])

# Main price plot
main_chart = base.mark_line(color='steelblue').encode(
    x='index:T',
    y='Adj Close:Q',
).properties(
    width=800,
    height=400,
    title=f"{ticker} Price Chart with Indicators ({start_date} - {end_date})"
).add_line(
    base.mark_line(color='orange').encode(y='Fast EMA:Q'),
    base.mark_line(color='purple').encode(y='Slow EMA:Q'),
).add_band(
    base.mark_area(opacity=0.2).encode(
        y='Lower Band:Q',
        y2='Upper Band:Q',
        color='lightgray'
    )
)

# MACD plot
macd_chart = base.mark_line(size=2).encode(
    x='index:T',
    y='Indicator:N',
    color='field:N'
).transform_filter(alt.datum['Indicator'] != 'Adj Close').properties(
    width=800,
    height=200,
    title='MACD',
    y_axis=alt.Axis(labels=False)  # Remove MACD value labels
).add_rule(
    base.mark_rule().encode(y='0:Q', strokeDash=[3, 3])
)

# Highlight buy/sell signals as scattered points on main chart
main_chart = main_chart.add_points(
    base.transform_filter(alt.datum['Indicator'] == 'MACD'),
    mark=alt.MarkPoint(size=10, filled=True),
    encode=alt.Color('Indicator:N', scale=alt.Scale(domain=['MACD', 'Signal'], scheme='redblue'))
).transform_filter(alt.datum['Indicator'] == 'MACD')

# Combine and display plots
c = main_chart & macd_chart

st.altair_chart(c, use_container_width=True)
