# Buy if 20-day MA > 50-day MA
from PriceLoader import PriceLoader
from BenchmarkStrategy import Strategy
import pandas as pd

class MovingAverageStrategy(Strategy):
    def __init__(self, symbol: str, loader: PriceLoader, short_window: int = 20, long_window: int = 50):
        super().__init__(symbol)
        self.loader = loader
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, start=None, end=None) -> pd.DataFrame:
        # get price data from the loader
        prices = self.loader.get_prices(self.symbol, start, end)

        # calculate moving averages
        short_ma = prices.rolling(self.short_window).mean()
        long_ma = prices.rolling(self.long_window).mean()

        # simple signal: 1 if short > long else 0
        signal = (short_ma > long_ma).astype(int)

        return pd.DataFrame({
            "price": prices,
            f"SMA{self.short_window}": short_ma,
            f"SMA{self.long_window}": long_ma,
            "signal": signal,
            "position": signal
        })