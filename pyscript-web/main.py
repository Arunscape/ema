import pandas as pd
from pyweb import pydom
from pyodide.http import open_url
from pyscript import display
from js import console

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

title = "Arun's EMA and MACD calculator"
page_message = "Calculates EMA and MACD"
url = "https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv"

pydom["title#header-title"].html = title
pydom["a#page-title"].html = title
pydom["div#page-message"].html = page_message
pydom["input#txt-url"][0].value = url


b = 42069

def log(message):
    # log to pandas dev console
    print(message)
    # log to JS console
    console.log(message)

def loadFromURL(event):
    pydom["div#pandas-output-inner"].html = ""
    url = pydom["input#txt-url"][0].value

    log(f"Trying to fetch CSV from {url}")
    df = pd.read_csv(open_url(url))

    pydom["div#pandas-output"].style["display"] = "block"
    pydom["div#pandas-dev-console"].style["display"] = "block"

    display(df, target="pandas-output-inner", append="False")


def ticker_info(ticker):
    data = get_data(ticker)

    crosses_up, crosses_down = ema_crosses_ma(data)
    bullish_macd, bearish_macd = macd_crossovers(data)

    return {
        "ema": {
            "crosses_up": crosses_up,
            "crosses_down": crosses_down,
        },
        "macd": {
            "bullish_macd": bullish_macd,
            "bearish_macd": bearish_macd,
        },
    }


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

    bullish_crossovers = [df.index[i] for i in macd_above_signal]
    bearish_crossovers = [df.index[i] for i in macd_below_signal]
    print("Bullish crossovers:", bullish_crossovers)
    print("Bearish crossovers:", bearish_crossovers)

    return bullish_crossovers, bearish_crossovers
