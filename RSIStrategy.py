# Buy if RSI < 30 (oversold)

import PriceLoader
from BenchmarkStrategy import Strategy
import pandas as pd

class RSIStrategy(Strategy):
    def __init__(self, symbol: str, window: int = 14):
        super().__init__(symbol)
        self.window = window

    def _compute_rsi(self, prices: pd.Series) -> pd.Series:
        delta = prices.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(self.window, min_periods=self.window).mean()
        avg_loss = loss.rolling(self.window, min_periods=self.window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self, prices: pd.Series) -> pd.DataFrame:
        rsi = self._compute_rsi(prices)
        # Buy signal when RSI < 30 (oversold), else 0 (flat)
        signal = (rsi < 30).astype(int)

        return pd.DataFrame({
            "price": prices,
            "RSI": rsi,
            "signal": signal,
            "position": signal
        })