from MovingAverageStrategy import MovingAverageStrategy
from MACDStrategy import MACDStrategy
from VolatilityBreakoutStrategy import VolatilityBreakoutStrategy
from RSIStrategy import RSIStrategy
from PriceLoader import PriceLoader
import matplotlib.pyplot as plt
import pandas as pd
import os

class Simulator:
    def __init__(self):
        self.pl = PriceLoader()
        self.tickers = self.pl.available_ticker
        stocks ={t:self.pl.load_price_data(t) for t in self.tickers}
        self.prices = pd.concat(stocks, axis=1)
        self.prices.columns = self.prices.columns.droplevel(1)
        ma = MovingAverageStrategy(self.prices, self.tickers)
        vol = VolatilityBreakoutStrategy(self.prices, self.tickers)
        rsi = RSIStrategy(self.prices, self.tickers)
        mac = MACDStrategy(self.prices, self.tickers)
        self.strat = [ma, vol, rsi, mac]
    
    def simulate_trade(self, strategy):
        sigs:pd.DataFrame = strategy.generate_signals()
        for time, s in sigs.iterrows():
            
            position_value = 0
            for tick in self.tickers:
                #Get new price for given stock at time t
                price = self.prices.loc[time,tick].astype(float)
                #update value of portfolio for given stock
                if strategy.positions[tick]['position_value']>0:
                    strategy.positions[tick]['position_value'] = (price/strategy.positions[tick]['position_value'] - 1)*100

                #Update positions if there is a buy or sell signal
                if s[tick]==1:
                    if strategy.cash > price:
                        strategy.positions[tick]['position_value'] += price
                        position_value += strategy.positions[tick]['position_value']
                        strategy.positions[tick]['shares'] +=1 
                        strategy.cash -= price
                elif s[tick]==-1:
                    if strategy.positions[tick]['shares']>0:
                        strategy.positions[tick]['position_value'] -=price
                        position_value += strategy.positions[tick]['position_value']
                        strategy.positions[tick]['shares'] -=1 
                        strategy.cash += price
                else:
                    continue
            
            strategy.portfolio_value.append(float(strategy.cash+position_value))
    def run_strats(self):
        names = ['MovingAverageStrategy', 'VolatilityBreakoutStrategy', 'RSIStrategy', 'MACDStrategy']
        for n,s in zip(names,self.strat):
            print(f'Simulating {n} ')
            self.simulate_trade(s)
    
    def plot_portoflio(self):
        names = ['MovingAverageStrategy', 'VolatilityBreakoutStrategy', 'RSIStrategy', 'MACDStrategy']
        DIR = 'Plots'
        os.makedirs('Plots', exist_ok=True)
        for n, s in zip(names, self.strat):
        
            fig, ax = plt.subplots(figsize=(10, 6))

            ax.plot(s.portfolio_value, label=f'Portfolio Value for {n}')
            ax.set_title(f'Portfolio Value for {n} Strategy Over Time', fontsize=14)
            ax.set_xlabel("Date/Time", fontsize=12)
            ax.set_ylabel("Portfolio Value ($)", fontsize=12)
            ax.legend()
            
            # 5. Optional: Add a grid for better readability
            ax.grid(True, linestyle='--', alpha=0.7)

            # 6. Save the figure
            filename = f'{n.replace(" ", "_")}.png'
            plt.savefig(os.path.join(DIR,filename))
            
            # 7. Close the figure to free up memory (important in loops)
            plt.close(fig)
            

         
if __name__ == '__main__':
    s = Simulator()
    s.run_strats()
    s.plot_portoflio()