from AbstractStrategy import Strategy
import pandas as pd

class MACDStrategy(Strategy):
    def __init__(self, prices:pd.DataFrame, tickers:list):
        super().__init__
        self.cash = 1_000_000
        self._symbol = tickers
        self._window = 9
        self._fast = 12
        self._slow = 26
        self.name = 'MACDStrategy'
        self._prices:pd.DataFrame = prices
        self.portfolio_value = []
        self.positions = { t:{'position_value':0,
                              'shares':0} for t in self._symbol}
    
    def generate_signals(self):
        sigs = pd.DataFrame(0, index=self._prices.index, columns=self._prices.columns)
         
        s = self._prices.astype(float)
        ema_f = s.ewm(span=self._fast, adjust=False).mean()
        ema_s = s.ewm(span=self._slow, adjust=False).mean()
        macd = ema_f - ema_s
        macd_sig = macd.ewm(span=self._window, adjust=False).mean()
        up = (macd > macd_sig) 
        dn = (macd < macd_sig) 
        sigs[up] = 1
        sigs[dn] = -1
        return sigs
             
