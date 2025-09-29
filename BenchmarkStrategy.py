from PriceLoader import PriceLoader, get_sp500_tickers

class BenchMarkStrategy:
    def __init__(self,x):
        self.pl = PriceLoader()
        self.tickers = self.pl.available_ticker
        self.x_shares = x
        self.cash = 1_000_000
        self.portfolio_value = self.cash
        self.positions = {}
    def initial_pos(self):
        for i in self.tickers:
            try:
                cur_price = self.pl.load_price_data(i).iloc[0].iloc[0]
                value = self.x_shares*float(cur_price)
                if value > self.cash:
                    self.tickers.remove(i)
                    continue
                self.cash -= value
                self.positions[i] = value
            except Exception as e:
                self.tickers.remove(i)
                print(e)

bm = BenchMarkStrategy(5)
bm.initial_pos()
print(bm.positions)
