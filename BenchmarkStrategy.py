from PriceLoader import PriceLoader, get_sp500_tickers

class BenchMarkStrategy:
    def __init__(self,x):
        self.pl = PriceLoader()
        self.tickers = self.pl.available_ticker
        self.x_shares = x
        self.cash = 1_000_000
        self.portfolio_value = [self.cash]
        self.positions = {}

    def initial_pos(self):
        for i in self.tickers:
            try:
                price = self.pl.load_price_data(i)
                cur_price = price.iloc[0].iloc[0]
                value = self.x_shares*float(cur_price)
                if value > self.cash:
                    self.tickers.remove(i)
                    continue
                self.cash -= value
                list_pos = price.values.tolist()
                list_pos = [i[0] for i in list_pos]
                self.positions[i] =  {
                    'value': cur_price,
                    'purchase_price': float(cur_price),
                    'list_price': list_pos}
            except Exception as e:
                self.tickers.remove(i)
                print(e)

    def run(self):
        sum = 0
        for i in range(1, 2516):
            for tick in self.positions.keys():
                prices = self.positions[tick]['list_price']
                cur_price = float(prices[i])
                purchase_price = self.positions[tick]['purchase_price']
                value = purchase_price*(float(cur_price)/purchase_price - 1)*100
                self.positions[tick]['value'] = value
                sum += value
            sum += self.cash
            self.portfolio_value.append(sum)


bm = BenchMarkStrategy(5)
bm.initial_pos()
bm.run()