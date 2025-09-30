import pandas as pd
import numpy as np
from PriceLoader import PriceLoader
from BenchmarkStrategy import Strategy

class MACDStrategy(Strategy):
    # build MACD cross signals (+1 upcross, -1 downcross)
    def build_signals(self, prices: pd.DataFrame, fast: int = 12, slow: int = 26, signal_window: int = 9) -> pd.DataFrame:
        sigs = pd.DataFrame(0, index=prices.index, columns=prices.columns)
        for t in prices.columns:
            s = prices[t].astype(float)
            ema_f = s.ewm(span=fast, adjust=False).mean()
            ema_s = s.ewm(span=slow, adjust=False).mean()
            macd = ema_f - ema_s
            macd_sig = macd.ewm(span=signal_window, adjust=False).mean()
            up = (macd > macd_sig) & (macd.shift(1) <= macd_sig.shift(1))
            dn = (macd < macd_sig) & (macd.shift(1) >= macd_sig.shift(1))
            sigs.loc[up, t] = 1
            sigs.loc[dn, t] = -1
        return sigs

    # load prices, build signals, delegate execution to base Strategy
    def run(self, fast: int = 12, slow: int = 26, signal_window: int = 9):
        prices = self.load_prices_wide()
        signals = self.build_signals(prices, fast=fast, slow=slow, signal_window=signal_window)
        return self.simulate_trades(prices, signals)