from AbstractStrategy import Strategy
from PriceLoader import PriceLoader
import pandas as pd

class MovingAverageStrategy(Strategy):
    def __init__(self, prices:pd.DataFrame, tickers:list):
        super().__init__
        self._short_window = 20
        self.cash = 1_000_000
        self._symbol = tickers
        self._long_window = 50
        self._prices:pd.DataFrame = prices
        self.portfolio_value = []
        self.positions = { t:{'position_value':0,
                              'shares':0} for t in self._symbol}



    def generate_signals(self):
        sigs = pd.DataFrame(0, index=self._prices.index, columns=self._prices.columns)
        for t in self._prices.columns:
            s = self._prices[t].astype(float)
            #Create the long and short moving average
            ma_short = s.rolling(self._short_window, min_periods=1).mean()
            ma_long = s.rolling(self._long_window, min_periods=1 ).mean()
            #Check  if there is a possibility for a buy or sell signal if conditions met
            up = (ma_short > ma_long)
            down = (ma_short < ma_long) 
            
            sigs.loc[up,t] = 1
            sigs.loc[down, t] = -1
        return sigs

       



