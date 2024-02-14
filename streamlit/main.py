import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

import streamlit as st

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)


def get_data(ticker, start="2023-07-01", end=datetime.today().strftime("%Y-%m-%d")):
    return yf.download(ticker, start="2023-07-01", end=end)


def ema_crosses_ma(data):
    # Download historical stock data
    #

    # Calculate 20-day EMA and 50-day MA
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
    data["MA_50"] = data["Close"].rolling(window=50).mean()

    # Find rows where EMA crosses MA (upward)
    crosses_up = data[
        (data["EMA_20"] > data["MA_50"])
        & (data["EMA_20"].shift(1) < data["MA_50"].shift(1))
    ]

    # Find rows where EMA crosses MA (downward)
    crosses_down = data[
        (data["EMA_20"] < data["MA_50"])
        & (data["EMA_20"].shift(1) > data["MA_50"].shift(1))
    ]

    # Print results
    # print("Dates where 20EMA crosses above 50MA (upward):")
    # print(crosses_up[["Close", "EMA_20", "MA_50"]])
    # print("\nDates where 20EMA crosses below 50MA (downward):")
    # print(crosses_down[["Close", "EMA_20", "MA_50"]])

    return (
        crosses_up[["Close", "EMA_20", "MA_50"]],
        crosses_down[["Close", "EMA_20", "MA_50"]],
    )


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



def get_tsx():
    response = requests.get('https://stockanalysis.com/api/screener/a/f?m=marketCap&s=desc&c=no,s,marketCap&f=exchange-is-TSX,subtype-isnot-etf!cef&dd=true&i=symbols')
    response = response.json()
    response = response["data"]["data"]
    return [d["s"].removeprefix("tsx/") for d in response]

tsx_stocks = get_tsx()
nyse_stocks = get_nyse()

nyse_stocks

ticker = st.multiselect(
    'Select the stocks you want to analyze:',
    nyse_stocks + tsx_stocks,
    [])

st.write('You selected:', ticker)


start_col, end_col = st.columns(2)

with start_col:
    start_date = st.date_input("Start Date", date.today() - relativedelta(years=1))
with end_col:
    end_date = st.date_input("End Date", date.today())
