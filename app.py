import streamlit as st
import pandas as pd
from stock_data import StockData
from strategy import SMABacktester

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SMA Backtester", layout="wide")
st.title("SMA Backtester")

# --- SIDEBAR: USER INPUTS ---
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Stock Ticker", value="NVDA").upper()

# Date Range Selection
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-01-01"))

# Strategy Parameters
short_window = st.sidebar.slider("Short Window (Days)", 5, 100, 50)
long_window = st.sidebar.slider("Long Window (Days)", 100, 365, 200)

# --- MAIN LOGIC ---
if st.sidebar.button("Run Backtest"):
    with st.spinner("Fetching Data..."):
        # Initialize Data
        stock = StockData(ticker)
        success = stock.download(start_date=start_date, end_date=end_date)

    if success:
        # Initialize Backtester
        backtester = SMABacktester(ticker, stock.data)
        
        # Run Strategy
        backtester.run_backtest(short_window, long_window)
        
        # --- DISPLAY METRICS ---
        strat_sharpe, strat_dd, market_sharpe, market_dd = backtester.calculate_risk_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Strategy Return", f"{(backtester.df['Cumulative_Strategy'].iloc[-1]-1)*100:.2f}%")
        col2.metric("Market Return", f"{(backtester.df['Cumulative_Market'].iloc[-1]-1)*100:.2f}%")
        col3.metric("Sharpe Ratio", f"{strat_sharpe:.2f}", delta=f"{strat_sharpe - market_sharpe:.2f}")
        col4.metric("Max Drawdown", f"{strat_dd*100:.2f}%")

        # --- DISPLAY PLOTS ---
        st.subheader("Price & Performance Analysis")
        fig_perf = backtester.plot_performance()
        st.pyplot(fig_perf)

        # --- OPTIMIZATION TAB ---
        with st.expander("See Optimization Heatmap (Computationally Intensive)"):
            if st.button("Run Optimization"):
                with st.spinner("Optimizing..."):
                    fig_opt = backtester.run_optimization()
                    st.pyplot(fig_opt)
    else:
        st.error(f"Could not download data for {ticker}. Please check the symbol.")