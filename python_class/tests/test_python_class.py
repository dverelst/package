from python_class import Cointegration
from python_class.Backtest import *
import datetime as dt

stock1 = "JPM"
stock2 = "BAC"
start_date = "2020-01-01"
end_date =  "2025-01-10"

returns1 = Cointegration.log_returns(stock1, start_date, end_date)
returns2 = Cointegration.log_returns(stock2, start_date, end_date)

spread = Cointegration.OLS_spread(returns1, returns2)[0]
beta = Cointegration.OLS_spread(returns1, returns2)[1].iloc[0]

buy_signal = Cointegration.trading_signals(spread)[0]
sell_signal = Cointegration.trading_signals(spread)[1]

strat = Cointegration.positions_dataframe(stock1, stock2, start_date, end_date, buy_signal, sell_signal, beta)

backtest = Backtest()
backtest.weight = strat
backtest.final_date = dt.datetime(2025, 1, 10)
backtest.initial_date = dt.datetime(2020, 1, 1)
 
backtest.run_backtest()
