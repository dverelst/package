from pybacktestchain import data_module
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt


def log_returns(ticker1, start_date, end_date):

    stocks_data = data_module.get_stock_data(ticker1, start_date, end_date)
    stocks_data= stocks_data.set_index("Date")
    stock1_close = stocks_data["Close"]

    log_returns = np.log(stock1_close / stock1_close.shift(1))
    log_returns = log_returns.dropna()

    return log_returns

def test_cointegration(returns1, returns2, alpha):
    """Test for cointegration between two time series."""

    score, p_value, _ = coint(returns1, returns2)
    print(f"Cointegration Test: p-value = {p_value}")

    return p_value < alpha # Consider cointegrated if p-value < 0.05

def OLS_spread(returns1, returns2):
    """Calculate the spread between two cointegrated stocks."""

    X = sm.add_constant(returns2)
    model = sm.OLS(returns1, X).fit()
    spread = returns1 - model.predict(X)

    return spread, model.params

def generate_trading_signals(spread, z_threshold=1.0):
    """Generate trading signals based on z-score of the spread."""

    z_score = (spread - spread.mean())/ spread.std()
    buy_signal = z_score < -z_threshold  # Buy the spread
    sell_signal = z_score > z_threshold  # Sell the spread

    return buy_signal, sell_signal, z_score

returns1 = log_returns("AAPL", "2010-01-01", "2025-01-10")
returns2 = log_returns("AMD", "2010-01-01", "2025-01-10")

#print(test_cointegration(returns1, returns2, 0.05))
#print(type(OLS_spread(returns1, returns2)[0]))
print(generate_trading_signals(OLS_spread(returns1, returns2)[0]))

print(returns1)