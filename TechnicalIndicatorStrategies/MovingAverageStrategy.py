import pandas as pd
import numpy as np
from PriceLoader import PriceLoader  # data loader
from BenchmarkStrategy import Strategy  # base class with execution logic

class MovingAverageStrategy(Strategy):
    # build simple SMA crossover signals (+1 upcross, -1 downcross)
    def build_signals(self, prices: pd.DataFrame, short: int = 50, long: int = 200) -> pd.DataFrame:
        sigs = pd.DataFrame(0, index=prices.index, columns=prices.columns)
        for t in prices.columns:
            s = prices[t].astype(float)
            sma_s = s.rolling(short, min_periods=1).mean()
            sma_l = s.rolling(long, min_periods=1).mean()
            up = (sma_s > sma_l) & (sma_s.shift(1) <= sma_l.shift(1))
            dn = (sma_s < sma_l) & (sma_s.shift(1) >= sma_l.shift(1))
            sigs.loc[up, t] = 1
            sigs.loc[dn, t] = -1
        return sigs

    # load prices, build signals, then let base Strategy execute with constraints
    def run(self, short: int = 50, long: int = 200):
        prices = self.load_prices_wide()  # provided by base via PriceLoader
        signals = self.build_signals(prices, short=short, long=long)
        return self.simulate_trades(prices, signals)  # provided by base