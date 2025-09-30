# macd_strategy.py
from BenchmarkStrategy import Strategy
import pandas as pd
from PriceLoader import PriceLoader

class MACDStrategy(Strategy):
    def __init__(self, symbol: str, loader: PriceLoader, fast: int = 12, slow: int = 26, signal_span: int = 9):
        super().__init__(symbol)
        self.loader = loader
        self.fast = fast
        self.slow = slow
        self.signal_span = signal_span

    def generate_signals(self, start=None, end=None) -> pd.DataFrame:
        # get price data
        prices = self.loader.get_prices(self.symbol, start, end).astype(float)

        # basic MACD calculation
        ema_fast = prices.ewm(span=self.fast, adjust=False).mean()
        ema_slow = prices.ewm(span=self.slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        sig = macd.ewm(span=self.signal_span, adjust=False).mean()

        # simple rule: buy/hold when MACD > signal, else flat
        signal = (macd > sig).astype(int)

        return pd.DataFrame({
            "price": prices,
            "MACD": macd,
            "Signal": sig,
            "signal": signal,
            "position": signal
        })
