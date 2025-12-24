import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def analyze_stock(ticker):
    # Standardize the input (make it uppercase, remove spaces)
    ticker = ticker.upper().strip()
    
    start_date = "2020-01-01"
    end_date = "2024-01-01"

    print(f"Downloading data for {ticker}...")
    
    # Download data
    # 'progress=False' stops yfinance from printing the loading bar text
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    # CS Concept: Error Handling
    # If the user typed a fake ticker, the dataframe will be empty.
    if data.empty:
        print(f"Error: Could not find data for symbol '{ticker}'. Are you sure it's correct?")
        return

    # Calculate Moving Averages
    data["SMA_50"] = data['Close'].rolling(window=50).mean()
    data["SMA_200"] = data['Close'].rolling(window=200).mean()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label=f'{ticker} Price', alpha=0.5, color='gray')
    plt.plot(data["SMA_50"], label='SMA 50', color='orange')
    plt.plot(data["SMA_200"], label='SMA 200', color='red')
    
    plt.title(f'{ticker} Golden Cross Analysis')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid(True, alpha=0.3) # Adds a grid for better readability
    plt.show()

# --- Main Execution Block ---
if __name__ == "__main__":
    # This loop allows the user to keep searching without restarting the script
    while True:
        user_input = input("\nEnter a stock ticker (or 'q' to quit): ")
        
        if user_input.lower() == 'q':
            print("Exiting program.")
            break
            
        analyze_stock(user_input)