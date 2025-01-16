from pybacktestchain import data_module
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def log_returns(ticker1, start_date, end_date):

    #computing the log returns of a given stock

    stocks_data = data_module.get_stock_data(ticker1, start_date, end_date)
    stocks_data= stocks_data.set_index("Date")
    stock1_close = stocks_data["Close"]

    log_returns = np.log(stock1_close / stock1_close.shift(1))
    log_returns = log_returns.dropna()

    return log_returns

def test_cointegration(returns1, returns2, alpha):
    #Testing Cointegration hypothesis between two returns series

    score, p_value, _ = coint(returns1, returns2)
    print(f"Cointegration Test: p-value = {p_value}")

    return p_value < alpha # Consider cointegrated if p-value < 0.05

def OLS_spread(returns1, returns2):
    #Computing the linear regression of the two stocks to use the beta as a hedge ratio

    X = sm.add_constant(returns2)
    model = sm.OLS(returns1, X).fit()
    spread = returns1 - model.predict(X)

    return spread, model.params

def trading_signals(spread, z_threshold=1.0):
    #Generating trading signals using the z-score of the spread

    z_score = (spread - spread.mean())/ spread.std()
    buy_signal = z_score < -z_threshold  # Buy the spread
    sell_signal = z_score > z_threshold  # Sell the spread

    return buy_signal, sell_signal, z_score

def positions_dataframe(ticker1, ticker2, start_date, end_date, buy_signal, sell_signal, hedge_ratio):
    
    positions = pd.DataFrame(index=buy_signal.index, columns=[ticker1, ticker2], dtype=float)
    positions[ticker1] = 0
    positions[ticker2] = 0

    # Iterate through the signals to update positions
    for i in range(0, len(buy_signal)):
        if buy_signal.iloc[i]:
            # Go long Stock1 and short Stock2
            positions.loc[buy_signal.index[i], ticker1] = 1
            positions.loc[buy_signal.index[i], ticker2] = float(-hedge_ratio)
        elif sell_signal.iloc[i]:
            # Go short Stock1 and long Stock2
            positions.loc[sell_signal.index[i], ticker1] = -1
            positions.loc[sell_signal.index[i], ticker2] = float(hedge_ratio)

    # Forward fill positions to maintain trades until new signals occur
    positions = positions.ffill().fillna(0)

    return positions

