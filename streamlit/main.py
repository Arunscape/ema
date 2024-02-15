#import yfinance as yf
#import pandas as pd
#import numpy as np
#import datetime as dt
from dateutil.relativedelta import relativedelta
#import streamlit as st
#import altair as alt

import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import altair as alt

def ema_crosses_ma(data, short_ema=12, long_ema=26):
    # Calculate 20-day EMA and 50-day MA
    data["Short EMA"] = data["Close"].ewm(span=short_ema, adjust=False).mean()
    data["Long EMA"] = data["Close"].rolling(window=long_ema, adjust=False).mean()

    ## Find rows where EMA crosses MA (upward)
    #crosses_up = data[
    #    (data["EMA_20"] > data["MA_50"])
    #    & (data["EMA_20"].shift(1) < data["MA_50"].shift(1))
    #]

    ## Find rows where EMA crosses MA (downward)
    #crosses_down = data[
    #    (data["EMA_20"] < data["MA_50"])
    #    & (data["EMA_20"].shift(1) > data["MA_50"].shift(1))
    #]

    # Print results
    # print("Dates where 20EMA crosses above 50MA (upward):")
    # print(crosses_up[["Close", "EMA_20", "MA_50"]])
    # print("\nDates where 20EMA crosses below 50MA (downward):")
    # print(crosses_down[["Close", "EMA_20", "MA_50"]])

    return data


def macd_crossovers(data):
    df = data
    short_ema = df["Close"].ewm(span=12, adjust=False).mean()
    long_ema = df["Close"].ewm(span=26, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_histogram = macd_line - signal_line

    # print(macd_line)
    # print(signal_line)
    # print(macd_histogram)
    macd_above_signal = np.where(macd_line > signal_line, 1, 0)
    macd_below_signal = np.where(macd_line < signal_line, 1, 0)

    # Print the crossover points

    bullish_crossovers = pd.DataFrame([df.index[i] for i in macd_above_signal])
    bearish_crossovers = pd.DataFrame([df.index[i] for i in macd_below_signal])
    # print("Bullish crossovers:", bullish_crossovers)
    # print("Bearish crossovers:", bearish_crossovers)

    return bullish_crossovers, bearish_crossovers




@st.cache_data(persist="disk")
def get_data(ticker, start="2023-07-01", end=dt.datetime.today().strftime("%Y-%m-%d")):
    return yf.download(ticker, start="2023-07-01", end=end)

def add_ema(df, window=20):
    df["EMA"] = df['Close'].ewm(span=window, min_periods=window).mean()

def add_ma(df, window=50):
    df["MA"] = df['Close'].rolling(window=window).mean()


ticker = st.text_input("Enter ticker symbol:", value="AAPL")
ticker

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date:", value=dt.date.today()-relativedelta(years=1))
    ema_period = st.number_input("EMA period:", min_value=1, max_value=500, value=20)
with col2:
    end_date = st.date_input("End date:", value=dt.date.today())
    ma_period = st.number_input("MA period:", min_value=1, max_value=500, value=50)

# Handle date range errors
if start_date > end_date:
    st.error("Start date cannot be after end date.")

# Download historical data
df = get_data(ticker, start_date, end_date)


add_ema(df)
add_ma(df)


df


# Streamlit app
st.title("Line Chart of Pandas DataFrame")

# Select columns to display
selected_columns = st.multiselect(
    "Select columns to display:", df.columns.tolist(), default=["Open", "Close", "EMA", "MA"]
)

# Create Altair chart

lines = (
    alt.Chart(df, title=f"{ticker}")
    .mark_line()
    .encode(x="Date:T", y="Close:Q")
)


st.altair_chart(
        (lines ).interactive(),
    use_container_width=True,
)
