from pybacktestchain import data_module
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

def test_cointegration(ticker1, ticker2, start_date, end_date):
    """Test for cointegration between two time series."""
    stocks_data = data_module.get_stocks_data([ticker1, ticker2], start_date, end_date)

    stock1_close = stocks_data[stocks_data["ticker"]==ticker1]["Close"]
    stock2_close = stocks_data[stocks_data["ticker"]==ticker2]["Close"]
    
    log_returns1, log_returns2 = np.log(stock1_close / stock1_close.shift(1)),  np.log(stock2_close / stock2_close.shift(1))
    log_returns1, log_returns2 = log_returns1.dropna(), log_returns2.dropna()


    score, p_value, _ = coint(log_returns1, log_returns2)
    print(f"Cointegration Test: p-value = {p_value}")
    return p_value < 0.05  # Consider cointegrated if p-value < 0.05

def calculate_spread(stock1, stock2):
    """Calculate the spread between two cointegrated stocks."""
    X = sm.add_constant(stock2)
    model = sm.OLS(stock1, X).fit()
    spread = stock1 - model.predict(X)
    return spread, model.params

def generate_trading_signals(spread, z_threshold=1.0):
    """Generate trading signals based on z-score of the spread."""
    z_score = (spread - spread.mean()) / spread.std()
    buy_signal = z_score < -z_threshold  # Buy the spread
    sell_signal = z_score > z_threshold  # Sell the spread
    return buy_signal, sell_signal, z_score


test_cointegration("AMD", "TTE", "2010-01-01", "2025-01-10")