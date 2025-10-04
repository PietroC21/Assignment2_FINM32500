from AbstractStrategy import Strategy
import pandas as pd

class VolatilityBreakoutStrategy(Strategy):
    def __init__(self, prices:pd.DataFrame, tickers:list):
        super().__init__
        self.cash = 1_000_000
        self._symbol = tickers
        self._window = 20
        self.name = 'RSIStrategy'
        self._prices:pd.DataFrame = prices
        self.portfolio_value = []
        self.positions = { t:{'position_value':0,
                              'shares':0} for t in self._symbol}

    def generate_signals(self):
        s = self._prices.astype(float)
        returns = s.pct_change()
        rolling_std = s.rolling(window=self._window).std()
        sigs = pd.DataFrame(0, index=s.index, columns=s.columns)
        up = returns > rolling_std
        dn = returns < rolling_std
        sigs[up] = 1
        sigs[dn] = -1
        return sigs
