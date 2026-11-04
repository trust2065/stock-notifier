from dataclasses import dataclass

import pandas as pd
import pandas_ta as ta
import yfinance as yf


@dataclass(frozen=True)
class StockInformation:
    symbol: str
    prices: pd.DataFrame
    current_k: float
    current_d: float


def fetch_stock_information(
    symbol: str,
    period: str = "6mo",
    interval: str = "1wk",
) -> StockInformation:
    """Fetch historical prices and calculate the latest stochastic values."""
    prices = yf.download(symbol, period=period, interval=interval)
    if prices.empty:
        raise ValueError(f"No stock data found for {symbol}")

    if isinstance(prices.columns, pd.MultiIndex):
        prices = prices.xs(symbol, level="Ticker", axis=1)

    low_9 = prices["Low"].rolling(9).min()
    high_9 = prices["High"].rolling(9).max()

    rsv = (prices["Close"] - low_9) / (high_9 - low_9) * 100

    k_values = []
    d_values = []
    k = 50.0
    d = 50.0

    for value in rsv:
        if pd.isna(value):
            k_values.append(float("nan"))
            d_values.append(float("nan"))
            continue

        k = k * 2 / 3 + value / 3
        d = d * 2 / 3 + k / 3
        k_values.append(k)
        d_values.append(d)

    return StockInformation(
        symbol=symbol,
        prices=prices,
        current_k=float(k_values[-1]),
        current_d=float(d_values[-1]),
    )
