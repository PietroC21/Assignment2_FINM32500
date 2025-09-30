import pandas as pd
import numpy as np
from PriceLoader import PriceLoader
from BenchmarkStrategy import Strategy

# compute RSI (EWMA method)
def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    d = series.diff()
    gain = d.clip(lower=0)
    loss = (-d).clip(lower=0)
    ag = gain.ewm(alpha=1/window, adjust=False).mean()
    al = loss.ewm(alpha=1/window, adjust=False).mean()
    rs = ag / al.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)

class RSIStrategy(Strategy):
    # build RSI threshold signals (+1 cross up from low, -1 cross down from high)
    def build_signals(self, prices: pd.DataFrame, window: int = 14, low: int = 30, high: int = 70) -> pd.DataFrame:
        sigs = pd.DataFrame(0, index=prices.index, columns=prices.columns)
        for t in prices.columns:
            r = rsi(prices[t].astype(float), window)
            up = (r > low) & (r.shift(1) <= low)
            dn = (r < high) & (r.shift(1) >= high)
            sigs.loc[up, t] = 1
            sigs.loc[dn, t] = -1
        return sigs

    # load prices, build signals, hand off to base for execution
    def run(self, window: int = 14, low: int = 30, high: int = 70):
        prices = self.load_prices_wide()
        signals = self.build_signals(prices, window=window, low=low, high=high)
        return self.simulate_trades(prices, signals)