from AbstractStrategy import Strategy
from PriceLoader import PriceLoader
import pandas as pd

class BenchmarkStrategy(Strategy):
    def __init__(self, prices:pd.DataFrame, tickers:list):
        super().__init__()
        self._symbol = tickers
        self._prices:pd.DataFrame = prices
        self.x_shares = 5
        self.cash = 1_000_000
        self.portfolio_value = [self.cash]
        self.positions = {t: {'position_value': 0, 'shares': 0} for t in self._symbol}

    def generate_signals(self):
        """
        Benchmark strategy: Buy and hold - buy equal amounts of all stocks at the beginning
        and hold them throughout the entire period.
        """
        prices = self._prices.astype(float)
        # Create signal DataFrame initialized to 0
        sigs = pd.DataFrame(0, index=prices.index, columns=prices.columns)
        
        # Buy signal only on the first day for all stocks
        sigs.iloc[0] = 1
        
        return sigs

    def initial_pos(self):
        """
        Initialize positions by buying equal amounts of all available stocks
        """
        # Calculate equal allocation per stock
        available_cash = self.cash
        num_stocks = len(self._symbol)
        
        if num_stocks == 0:
            return
            
        cash_per_stock = available_cash / num_stocks
        
        for ticker in self._symbol:
            try:
                # Get the first available price for this ticker
                price_series = self._prices[ticker].dropna()
                if len(price_series) == 0:
                    continue
                    
                initial_price = price_series.iloc[0]
                shares_to_buy = int(cash_per_stock / initial_price)
                
                if shares_to_buy > 0:
                    cost = shares_to_buy * initial_price
                    self.cash -= cost
                    self.positions[ticker]['shares'] = shares_to_buy
                    self.positions[ticker]['position_value'] = cost
                    
            except Exception as e:
                print(f'Error initializing position for {ticker}: {e}')
                continue

   
if __name__ == '__main__':
    pl = PriceLoader()
    tickers = pl.available_ticker
    stocks ={t:pl.load_price_data(t) for t in tickers}
    prices = pd.concat(stocks, axis=1)
    bm = BenchmarkStrategy(prices,tickers)
    bm.initial_pos()
    bm.run()
    print(f"Initial cash: {bm.cash}")
    print(f"Positions: {bm.positions}")
