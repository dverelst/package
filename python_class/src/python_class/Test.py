import pybacktestchain as pt
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

def test_cointegration(stock1, stock2):
    """Test for cointegration between two time series."""
    score, p_value, _ = coint(stock1, stock2)
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
