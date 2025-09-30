import pandas as pd
import numpy as np
from PriceLoader import PriceLoader
from BenchmarkStrategy import Strategy

class VolatilityBreakoutStrategy(Strategy):
    # build Donchian breakout signals (+1 break above high, -1 break below low)
    def build_signals(self, prices: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        sigs = pd.DataFrame(0, index=prices.index, columns=prices.columns)
        for t in prices.columns:
            s = prices[t].astype(float)
            hi = s.rolling(window, min_periods=1).max()
            lo = s.rolling(window, min_periods=1).min()
            up = s > hi.shift(1)
            dn = s < lo.shift(1)
            sigs.loc[up, t] = 1
            sigs.loc[dn, t] = -1
        return sigs

    # load prices, build signals, then execute via base Strategy
    def run(self, window: int = 20):
        prices = self.load_prices_wide()
        signals = self.build_signals(prices, window=window)
        return self.simulate_trades(prices, signals)