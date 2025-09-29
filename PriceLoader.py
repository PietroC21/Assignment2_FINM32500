import yfinance as yf
import datetime
import pandas as pd
import requests
import os

# --- Configuration ---
DATA_DIR = 'sp500_daily_prices_parquet'
START_DATE = datetime.datetime(2015,1,1)
END_DATE = datetime.datetime(2025,1,1)
BATCH_SIZE = 50
def get_sp500_tickers():
        #Use url to retrive html file
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        # Set a User-Agent to mimic a browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers)
        
        #read html file and get information
        tables = pd.read_html(response.text, flavor='html5lib')

        #Get the symbols and return it in a form of a list
        sp_500 = tables[0]
        tickers = sp_500['Symbol'].tolist()
        return tickers

def download_and_store():
    tickers = get_sp500_tickers()
    os.makedirs(DATA_DIR, exist_ok=True)

    total_batches = (len(tickers) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(tickers), BATCH_SIZE):
        batch_tickers = tickers[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        print(f"\n--- Batch {batch_num}/{total_batches}: Downloading {len(batch_tickers)} tickers ---")

        try:
            # Download data for this batch
            data = yf.download(
                batch_tickers,
                start=START_DATE,
                end=END_DATE,
                progress=False,
                auto_adjust=True
            )

            # Get the 'Close' prices only
            price_data = data['Close'].copy()

            for ticker in batch_tickers:
                if ticker in price_data.columns:
                    ticker_data = price_data[[ticker]].rename(columns={ticker: 'Price'})

                    # Skip if any missing values
                    if ticker_data.isnull().values.any():
                        print(f"Skipping {ticker}: contains missing values")
                        continue

                    # Save as a parquet file
                    file_path = os.path.join(DATA_DIR, f'{ticker}.parquet')
                    ticker_data.to_parquet(file_path)
                else:
                    print(f"{ticker} not found in downloaded data columns: {list(price_data.columns)}")

        except Exception as e:
            print(f"[{i+1}/{len(tickers)}] ERROR downloading or saving batch {batch_num}: {e}")

class PriceLoader:
    def __init__(self,data_dir: str = DATA_DIR):
         self.data_dir = data_dir
         self._available_ticker =  None

    @property
    def available_ticker(self):
         if self._available_ticker is None:
              files = os.listdir(self.data_dir)
              self._available_ticker = [ f.replace('.parquet', '')for f in files if f.endswith('.parquet')]
         return self._available_ticker

    def load_price_data(self, ticker):
         if ticker not in self.available_ticker:
            print(f"Error: Price data for ticker '{ticker}' not found in {self.data_dir}.")
            return None
         file_path = os.path.join(self.data_dir, f'{ticker}.parquet')
         try:
              df = pd.read_parquet(file_path)
              print(f"Successfully loaded data for {ticker}. Shape: {df.shape}")
              return df
         except Exception as e:
            print(f"Error reading Parquet file for {ticker}: {e}")
            return None



