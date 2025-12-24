import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class GoldenCrossBacktester:
    def __init__(self, ticker, stock_data):
        self.ticker = ticker
        # We make a copy so we don't mess up the original data if we run multiple tests
        self.df = stock_data.copy()
        self.results = None

    def run_backtest(self, short_window, long_window):
        """Executes the vectorized backtest logic"""
        
        # 1. Calculate Moving Averages
        self.df["SMA_Short"] = self.df['Close'].rolling(window=short_window).mean()
        self.df["SMA_Long"] = self.df['Close'].rolling(window=long_window).mean()

        # 2. Generate Signals
        self.df['Signal'] = np.where(self.df['SMA_Short'] > self.df['SMA_Long'], 1, 0)

        # 3. Calculate Returns
        self.df['Stock_Return'] = self.df['Close'].pct_change()
        self.df['Strategy_Return'] = self.df['Signal'].shift(1) * self.df['Stock_Return']

        # 4. Cumulative Returns
        self.df['Cumulative_Market'] = (1 + self.df['Stock_Return']).cumprod()
        self.df['Cumulative_Strategy'] = (1 + self.df['Strategy_Return']).cumprod()
        
        self.short_window = short_window
        self.long_window = long_window

    def plot_performance(self):
        """Plots the Price and the Strategy Performance"""
        if 'Cumulative_Strategy' not in self.df.columns:
            print("Run backtest first!")
            return

        # Define Title Logic
        if self.short_window == 50 and self.long_window == 200:
            strategy_name = "Golden Cross"
        else:
            strategy_name = f"SMA {self.short_window}/{self.long_window}"

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Plot 1: Price
        ax1.plot(self.df['Close'], label=f'{self.ticker} Price', alpha=0.5, color='gray')
        ax1.plot(self.df["SMA_Short"], label=f'SMA {self.short_window}', color='orange')
        ax1.plot(self.df["SMA_Long"], label=f'SMA {self.long_window}', color='red')
        ax1.set_title(f'{self.ticker} Price Analysis')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Returns
        ax2.plot(self.df['Cumulative_Market'], label='Buy & Hold', color='gray', linestyle='--')
        ax2.plot(self.df['Cumulative_Strategy'], label=f'{strategy_name}', color='green')
        ax2.set_title(f'Performance: Buy & Hold vs. {strategy_name}')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def calculate_risk_metrics(self):
        """Calculates Sharpe Ratio and Max Drawdown"""
        if 'Strategy_Return' not in self.df.columns:
            print("Run backtest first!")
            return None, None, None, None

        def get_metrics(series):
            daily_mean = series.mean()
            daily_std = series.std()
            sharpe = (daily_mean / daily_std) * (252 ** 0.5) if daily_std != 0 else 0
            
            cumulative = (1 + series).cumprod()
            running_max = cumulative.cummax()
            drawdown = (cumulative / running_max) - 1
            max_dd = drawdown.min()
            return sharpe, max_dd

        # Calculate for Strategy
        strat_sharpe, strat_dd = get_metrics(self.df['Strategy_Return'])
        
        # CHANGE 2: Calculate for Market (Buy & Hold)
        market_sharpe, market_dd = get_metrics(self.df['Stock_Return'])

        return strat_sharpe, strat_dd, market_sharpe, market_dd

    def print_summary(self):
        if 'Cumulative_Strategy' not in self.df.columns:
            print("Error: Please run run_backtest() before printing summary.")
            return
        latest_strategy = self.df['Cumulative_Strategy'].iloc[-1]
        latest_market = self.df['Cumulative_Market'].iloc[-1]
        strat_sharpe, strat_dd, market_sharpe, market_dd = self.calculate_risk_metrics()

        print(f"{'Metric':<15} {'Strategy':<15} {'Buy & Hold':<15}")
        print("-" * 45)
        print(f"{'Total Return':<15} {(latest_strategy - 1)*100:.2f}%{'':<8} {(latest_market - 1)*100:.2f}%")
        print(f"{'Sharpe Ratio':<15} {strat_sharpe:.2f}{'':<11} {market_sharpe:.2f}")
        print(f"{'Max Drawdown':<15} {strat_dd*100:.2f}%{'':<8} {market_dd*100:.2f}%")
        print("---------------------------------------------\n")

    def run_optimization(self):
        """Runs the loop to find best parameters"""
        print(f"\nOptimizing parameters for {self.ticker}...")
        
        prices = self.df['Close'].dropna().to_numpy().flatten()
        short_range = range(10, 60, 5) 
        long_range = range(100, 220, 10)
        
        self.results = pd.DataFrame(index=short_range, columns=long_range)
        
        for short_w in short_range:
            for long_w in long_range:
                if short_w >= long_w:
                    self.results.loc[short_w, long_w] = total_ret
                    continue
                
                # Simplified loop logic for speed
                sma_short = pd.Series(prices).rolling(window=short_w).mean()
                sma_long = pd.Series(prices).rolling(window=long_w).mean()
                signal = np.where(sma_short > sma_long, 1, 0)
                
                market_ret = pd.Series(prices).pct_change()
                strategy_ret = pd.Series(signal).shift(1) * market_ret
                total_ret = (1 + strategy_ret).prod() - 1
                
                self.results.loc[short_w, long_w] = total_ret

        plt.figure(figsize=(10, 8))
        sns.heatmap(self.results.astype(float), annot=True, fmt=".2f", cmap="RdYlGn", center=0)
        plt.title(f"Optimization Heatmap: {self.ticker}")
        plt.xlabel("Long Window")
        plt.ylabel("Short Window")
        plt.show()