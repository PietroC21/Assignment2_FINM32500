from AbstractStrategy import Strategy
import pandas as pd

class MovingAverageStrategy(Strategy):
    def __init__(self, prices:pd.DataFrame, tickers:list):
        super().__init__
        self._short_window = 20
        self._symbol = tickers
        self._long_window = 50
        self._prices:pd.DataFrame = prices
        self.positions = { t:{'position_value':0,
                              'shares':0} for t in self._symbol}
        self.cash = 1_000_000
        self.portfolio_value = [self.cash]
        
    def generate_signals(self):
        prices = self._prices.astype(float)
        # Compute short and long moving averages for all tickers at once
        ma_short = prices.rolling(self._short_window, min_periods=1).mean()
        ma_long = prices.rolling(self._long_window, min_periods=1).mean()

        # Create signal DataFrame initialized to 0
        sigs = pd.DataFrame(0, index=prices.index, columns=prices.columns)

        # Vectorized boolean masks
        up = ma_short > ma_long
        down = ma_short < ma_long

        # Assign signals using masks
        sigs[up] = 1
        sigs[down] = -1

        return sigs


        



