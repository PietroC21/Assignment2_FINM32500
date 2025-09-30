# volatility_breakout_strategy.py
from PriceLoader import PriceLoader
from BenchmarkStrategy import Strategy
import pandas as pd


class VolatilityBreakoutStrategy(Strategy):
    def __init__(self, symbol: str, loader: PriceLoader, window: int = 20):
        super().__init__(symbol)
        self.loader = loader
        self.window = window

    def generate_signals(self, start=None, end=None) -> pd.DataFrame:
        # get price data
        prices = self.loader.get_prices(self.symbol, start, end).astype(float)

        # daily returns
        daily_ret = prices.pct_change()

        # rolling volatility (std of returns)
        rolling_vol = daily_ret.rolling(self.window).std()

        # buy signal: when return > rolling volatility
        signal = (daily_ret > rolling_vol).astype(int)

        return pd.DataFrame({
            "price": prices,
            "return": daily_ret,
            f"vol_{self.window}": rolling_vol,
            "signal": signal,
            "position": signal
        })