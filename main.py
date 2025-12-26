from stock_data import StockData
from strategy import SMABacktester 

def main():
    while True:
        print("\n--- STOCK TOOL MENU ---")
        print("1. Analyze a Stock")
        print("2. Optimize a Stock")
        print("Q. Quit")
        
        choice = input("Select: ").upper().strip()
        
        if choice == 'Q':
            break

        ticker = input("Enter ticker: ")
        
        # 1. Instantiate the Data Object
        stock = StockData(ticker)
        
        # 2. Download the data (If it fails, loop back)
        if not stock.download():
            continue

        # 3. Instantiate the Backtester Object with the data
        # Note: stock.data accesses the dataframe inside the object
        backtester = SMABacktester(ticker, stock.data)

        if choice == '1':
            # Ask for custom params or default
            use_custom = input("Use custom parameters? (y/n): ").lower()
            if use_custom == 'y':
                s = int(input("Short: (eg. 50) "))
                l = int(input("Long: (eg. 200) "))
                backtester.run_backtest(s, l)
            else:
                backtester.run_backtest(50, 200)
                
            backtester.plot_performance()
            backtester.print_summary()

        elif choice == '2':
            backtester.run_optimization()

if __name__ == "__main__":
    main()