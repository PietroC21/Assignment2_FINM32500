from AbstractStrategy import Strategy
import numpy as np
import pandas as pd

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
    def __init__(self, prices:pd.DataFrame, tickers:list):
        super().__init__
        self.__low = 30
        self.__high = 70
        self.__windows = 10
        self.cash = 1_000_000
        self._symbol = tickers
        self._prices:pd.DataFrame = prices
        self.portfolio_value = []
        self.positions = { t:{'position_value':0,
                              'shares':0} for t in self._symbol}

    def generate_signals(self):
        sigs = pd.DataFrame(0, index=self._prices.index, columns=self._prices.columns)
        
        #price for stock t
        s = self._prices.astype(float)
        #calculate the rsi
        r = rsi(s.astype(float), self.__windows)

        #generate sell and buy signals
        up = (r > self.__low) 
        dn = (r < self.__high)

        #put them in singal dataframe
        sigs[up] = 1
        sigs[dn] = -1
        return sigs
