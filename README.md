# Containerized SMA Trend Backtester

An algorithmic trading dashboard built with **Python, Streamlit, and Docker.**

This application provides a robust environment for backtesting Moving Average Crossover strategies. It features a vectorized backtesting engine, parameter optimization heatmaps, and institutional-grade risk analysis (Sharpe Ratio, Max Drawdown). The entire application is containerized for seamless cross-platform deployment.

### Key Features
Vectorized Engine: Uses pandas and numpy vectorization for high-speed backtesting (0.01s execution time), replacing slow iterative loops.

Risk Management Visualization: Includes "Underwater Plots" to visualize drawdown depth and duration, proving the strategy's ability to preserve capital during market crashes.

Parameter Optimization: Generates computation-intensive heatmaps to identify the most robust Moving Average combinations (e.g., SMA 85/100).

Interactive Dashboard: Built with Streamlit for real-time interaction—change tickers and windows instantly without restarting the script.

Dockerized Deployment: Fully containerized environment ensuring the app runs identically on Windows, Mac, Linux, or Cloud Servers.

The Strategy & Damage Control
The core strategy implemented is a Moving Average Crossover. While the standard "Golden Cross" (50/200 SMA) is popular, this engine allows for granular optimization.

### Finding: The 85/100 Edge
Through optimization, the SMA 85 / SMA 100 pair demonstrated superior risk-adjusted returns during the 2020-2023 volatility.

Why it worked: It was fast enough to exit positions before major drawdowns (COVID-19, 2022 Inflation) but slow enough to filter out daily noise.

Visual Proof: The "Underwater Plot" in the app demonstrates that while the market fell -25% in 2022, the strategy remained flat (cash), effectively neutralizing volatility drag.

> Note: The success of specific parameters (like 85/100) is a result of in-sample optimization. For production trading, Walk-Forward Optimization would be required to prevent overfitting.

## Technical Architecture
The project follows a modular Object-Oriented Programming (OOP) structure to ensure maintainability and scalability.

1. Data Layer (stock_data.py)
Class: StockData

Handles API connections (via yfinance) and data sanitation.

Ensures clean time-series data is passed to the logic layer.

2. Logic Layer (strategy.py)
Class: SMABacktester

Contains the core financial logic.

Vectorization: Signals are generated using np.where on entire array columns rather than iterating row-by-row.

Calculations: Computes Sharpe Ratio (Annualized) and running Max Drawdown.

3. Presentation Layer (app.py)
Framework: Streamlit

Acts as the frontend client. It imports the backend classes, instantiates objects, and renders the returned Matplotlib figures and DataFrames.

4. Infrastructure (Docker)
Container: Linux (Debian-based)

Python: 3.11-slim

Isolation: The Dockerfile freezes dependencies (pandas 2.0+, matplotlib, etc.) to eliminate "it works on my machine" issues.

Usage Guide
Prerequisites
Docker Desktop must be installed and running.

For Windows Users
Clone the repository.

Double-click the run_windows.bat file.

The script will wake up Docker, build/start the container, and automatically open your browser to the dashboard.

For Mac & Linux Users
Clone the repository.

Open your terminal and navigate to the project folder.

Make the launch script executable (only needed once):

Bash

chmod +x run_mac_linux.sh
Run the app:

Bash

./run_mac_linux.sh
Manual Run (Command Line)
If you prefer to run Docker manually without the scripts:

Bash

docker build -t SMA-backtester .
docker run -p 8501:8501 SMA-backtester
Then visit http://localhost:8501.

License
This project is licensed under the MIT License - see the LICENSE file for details.

> Disclaimer: This project is for educational and research purposes only. Past performance is not indicative of future results. Nothing in this repository constitutes financial advice.
