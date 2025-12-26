import matplotlib
matplotlib.use('Agg')  # Prevents plotting crashes in Docker
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from stock_data import StockData
from strategy import SMABacktester

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SMA Backtester", layout="wide")
st.title("SMA Backtester")

# --- SESSION STATE SETUP ---
# This ensures data survives the "Refresh" when you click buttons
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'ticker' not in st.session_state:
    st.session_state.ticker = None

# --- SIDEBAR: USER INPUTS ---
st.sidebar.header("Configuration")
ticker_input = st.sidebar.text_input("Stock Ticker", value="NVDA").upper()
# Date Range Selection
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-01-01"))

# Strategy Parameters
short_window = st.sidebar.slider("Short Window (Days)", 5, 100, 50)
long_window = st.sidebar.slider("Long Window (Days)", 100, 365, 200)

# --- ACTION: DOWNLOAD DATA ---
if st.sidebar.button("Get/Refresh Data"):
    with st.spinner(f"Fetching data for {ticker_input}..."):
        stock = StockData(ticker_input)
        if stock.download(start_date=start_date, end_date=end_date):
            # SAVE TO MEMORY (Critical Step)
            st.session_state.stock_data = stock.data
            st.session_state.ticker = ticker_input
        else:
            st.error("Failed to download data.")
# --- MAIN LOGIC ---
if st.session_state.stock_data is not None:
    # Retrieve from memory
    df = st.session_state.stock_data
    current_ticker = st.session_state.ticker
    
    # Initialize Backtester
    backtester = SMABacktester(current_ticker, df)
    
    # Run Strategy (Always runs if data exists)
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

    # --- OPTIMIZATION TAB (FIXED WITH SESSION STATE) ---
    st.markdown("---")
    st.header("Optimization")

    # 1. Initialize Session State variables if they don't exist
    if 'opt_run' not in st.session_state:
        st.session_state.opt_run = False
    if 'opt_fig' not in st.session_state:
        st.session_state.opt_fig = None

    # The Trigger
    if st.button("Run Optimization"):
        st.session_state.opt_run = True

    # 3. If the state is True, we run the code (and it stays True)
    if st.session_state.opt_run:
        if st.session_state.opt_fig is None:
                with st.spinner("Crunching numbers (Vectorized)..."):
                    try:
                        fig = backtester.run_optimization()
                        st.session_state.opt_fig = fig # Save result to memory
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # Display the result (If it exists in memory)
        if st.session_state.opt_fig:
            st.success("Optimization Complete!")
            st.pyplot(st.session_state.opt_fig)
            
            # Button to clear it
            if st.button("Clear Optimization"):
                st.session_state.opt_run = False
                st.session_state.opt_fig = None
                st.experimental_rerun()
else:
    st.info("Click 'Get/Refresh Data' in the sidebar to start!")