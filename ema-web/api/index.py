from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


@app.get("/api/healthchecker")
def healthchecker():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}

@app.get("/api/ticker/{ticker}")
def ticker_info(ticker):

    data = get_data(ticker)

    ema = ema_crosses_ma(data)
    macd = macd_crossovers(data)

    return ema, macd





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
    print("Dates where 20EMA crosses above 50MA (upward):")
    print(crosses_up[["Close", "EMA_20", "MA_50"]])
    print("\nDates where 20EMA crosses below 50MA (downward):")
    print(crosses_down[["Close", "EMA_20", "MA_50"]])

    return crosses_up[["Close", "EMA_20", "MA_50"]], crosses_down[["Close", "EMA_20", "MA_50"]]


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

    bullish_crossovers = [df.index[i] for i in macd_above_signal]
    bearish_crossovers = [df.index[i] for i in macd_below_signal]
    print("Bullish crossovers:", bullish_crossovers)
    print("Bearish crossovers:", bearish_crossovers)

    return bullish_crossovers, bearish_crossovers
