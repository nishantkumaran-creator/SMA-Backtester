import yfinance as yf

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker.upper().strip()
        self.data = None

    def download(self, start_date="2020-01-01", end_date="2024-01-01"):
        print(f"Downloading data for {self.ticker}...")
        try:
            # Download data
            self.data = yf.download(self.ticker, start=start_date, end=end_date, progress=False)
            
            if self.data.empty:
                print(f"Error: No data found for {self.ticker}")
                return False
            
            # Helper to return the raw close prices (useful for optimization)
            return True
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_close_prices(self):
        """Returns the Close column as a Series, dropping NAs"""
        if self.data is not None:
            return self.data['Close']
        return None