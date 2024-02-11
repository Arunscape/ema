import pandas as pd
import yfinance as yf

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

yf.set_tz_cache_location("./.yfinance_cache")


def ema_crosses_ma(ticker):
    # Download historical stock data
    data = yf.download(ticker, start="2022-01-01", end="2022-12-31")

    # Calculate 20-day EMA and 50-day MA
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()

    # Find rows where EMA crosses MA (upward)
    crosses_up = data[(data['EMA_20'] > data['MA_50']) & (data['EMA_20'].shift(1) < data['MA_50'].shift(1))]

    # Find rows where EMA crosses MA (downward)
    crosses_down = data[(data['EMA_20'] < data['MA_50']) & (data['EMA_20'].shift(1) > data['MA_50'].shift(1))]

    # Print results
    print("Dates where 20EMA crosses above 50MA (upward):")
    print(crosses_up[['Close', 'EMA_20', 'MA_50']])
    print("\nDates where 20EMA crosses below 50MA (downward):")
    print(crosses_down[['Close', 'EMA_20', 'MA_50']])

# Example usage
ticker_symbol = "AAPL"  # Change this to the desired stock symbol
ema_crosses_ma(ticker_symbol)

