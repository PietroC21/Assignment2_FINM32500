# rsi_strategy.py
from PriceLoader import PriceLoader
from BenchmarkStrategy import Strategy
import pandas as pd


class RSIStrategy(Strategy):
    def __init__(self, symbol: str, loader: PriceLoader, window: int = 14):
        super().__init__(symbol)
        self.loader = loader
        self.window = window

    def generate_signals(self, start=None, end=None) -> pd.DataFrame:
        # get price data
        prices = self.loader.get_prices(self.symbol, start, end).astype(float)

        # compute RSI
        delta = prices.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(self.window).mean()
        avg_loss = loss.rolling(self.window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # buy signal when RSI < 30
        signal = (rsi < 30).astype(int)

        return pd.DataFrame({
            "price": prices,
            "RSI": rsi,
            "signal": signal,
            "position": signal
        })