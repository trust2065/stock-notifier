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

    kd = ta.stoch(
        prices["High"],
        prices["Low"],
        prices["Close"],
        k=9,
        d=3,
        smooth_k=3,
    )
    if kd is None:
        raise ValueError(f"Unable to calculate stochastic values for {symbol}")

    return StockInformation(
        symbol=symbol,
        prices=prices,
        current_k=float(kd["STOCHk_9_3_3"].iloc[-1]),
        current_d=float(kd["STOCHd_9_3_3"].iloc[-1]),
    )
