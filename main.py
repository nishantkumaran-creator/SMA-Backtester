import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  
import seaborn as sns

def analyze_stock(ticker, short_window=50, long_window=200):
    ticker = ticker.upper().strip()
    start_date = "2020-01-01"
    end_date = "2024-01-01"

    print(f"Downloading data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if data.empty:
        print(f"Error: Could not find data for symbol '{ticker}'.")
        return

    # 1. Calculate Moving Averages
    data["SMA_Short"] = data['Close'].rolling(window=short_window).mean()
    data["SMA_Long"] = data['Close'].rolling(window=long_window).mean()

    # 2. Generate Signals
    data['Signal'] = np.where(data['SMA_Short'] > data['SMA_Long'], 1, 0)

    # 3. Calculate Returns
    data['Stock_Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Stock_Return']

    # 4. Cumulative Returns
    data['Cumulative_Market'] = (1 + data['Stock_Return']).cumprod()
    data['Cumulative_Strategy'] = (1 + data['Strategy_Return']).cumprod()

    if short_window == 50 and long_window == 200:
        strategy_name = "Golden Cross"
    else:
        strategy_name = f"SMA {short_window}/{long_window} Crossover"

    # --- PLOTTING ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    ax1.plot(data['Close'], label=f'{ticker} Price', alpha=0.5, color='gray')
    ax1.plot(data["SMA_Short"], label=f'SMA {short_window}', color='orange')
    ax1.plot(data["SMA_Long"], label=f'SMA {long_window}', color='red')
    ax1.set_title(f'{ticker} Price Analysis')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(data['Cumulative_Market'], label='Buy & Hold', color='gray', linestyle='--')
    ax2.plot(data['Cumulative_Strategy'], label=f'{strategy_name} Strategy', color='green')
    ax2.set_title(f'{ticker} Performance: Buy & Hold vs. {strategy_name}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    
    # This logic belongs here because 'data' has the calculated columns
    latest_strategy = data['Cumulative_Strategy'].iloc[-1]
    latest_market = data['Cumulative_Market'].iloc[-1]

    print(f"\n--- Results for {ticker} ---")
    print(f"Buy & Hold Return: {(latest_market - 1)*100:.2f}%")
    print(f"Strategy Return:   {(latest_strategy - 1)*100:.2f}%")
    print("-------------------------------\n")

def optimize_strategy(ticker):
    ticker = ticker.upper().strip()
    print(f"\nOptimizing parameters for {ticker} (this may take a moment)...")
    data = yf.download(ticker, start="2020-01-01", end="2024-01-01", progress=False)
    
    if data.empty:
        print("Data not found.")
        return

    prices = data['Close'].dropna().to_numpy().flatten()
    
    short_range = range(10, 60, 5) 
    long_range = range(100, 220, 10)
    
    results = pd.DataFrame(index=short_range, columns=long_range)
    
    for short_window in short_range:
        for long_window in long_range:
            if short_window >= long_window:
                results.loc[short_window, long_window] = np.nan
                continue
            
            sma_short = pd.Series(prices).rolling(window=short_window).mean()
            sma_long = pd.Series(prices).rolling(window=long_window).mean()
            
            signal = np.where(sma_short > sma_long, 1, 0)
            market_returns = pd.Series(prices).pct_change()
            strategy_returns = pd.Series(signal).shift(1) * market_returns
            total_return = (1 + strategy_returns).prod() - 1
            
            results.loc[short_window, long_window] = total_return

    plt.figure(figsize=(10, 8))
    sns.heatmap(results.astype(float), annot=True, fmt=".2f", cmap="RdYlGn", center=0)
    plt.title(f"Strategy Return Heatmap for {ticker}")
    plt.xlabel("Long Window Days")
    plt.ylabel("Short Window Days")
    plt.show()

# --- MAIN BLOCK ---
if __name__ == "__main__":
    while True:
        print("\n--- STOCK TOOL MENU ---")
        print("1. Analyze a Stock (Standard 50/200 Cross)")
        print("2. Analyze (Custom Parameters)")  # <--- NEW OPTION
        print("3. Optimize a Stock (Find Best Parameters)")
        print("Q. Quit")
        
        choice = input("Select an option: ").upper().strip()
        
        if choice == '1':
            ticker = input("Enter ticker: ")
            analyze_stock(ticker)
        elif choice == '2':
            ticker = input("Ticker: ")
            # Use 'int()' to convert string input to integer
            s_window = int(input("Short Window (e.g., 20): "))
            l_window = int(input("Long Window (e.g., 140): "))
            analyze_stock(ticker, s_window, l_window)
            
        elif choice == '3':
            optimize_strategy(input("Ticker: "))
        elif choice == 'Q':
            print("Exiting...")
            break
        else:
            print("Invalid option.")
        