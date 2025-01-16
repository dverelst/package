from python_class import Cointegration
from python_class.Backtest import *
import datetime as dt

returns1 = Cointegration.log_returns("AAPL", "2010-01-01", "2025-01-10")
returns2 = Cointegration.log_returns("AMD", "2010-01-01", "2025-01-10")
print(returns1)

spread = Cointegration.OLS_spread(returns1, returns2)[0]
beta = Cointegration.OLS_spread(returns1, returns2)[1][0]

buy_signal = Cointegration.generate_trading_signals(spread)[0]
sell_signal = Cointegration.generate_trading_signals(spread)[1]

strat = Cointegration.generate_positions_dataframe("AAPL", "NVDA", "2010-01-01", "2025-01-10", buy_signal, sell_signal, beta)

backtest = Backtest()
backtest.weight = strat
backtest.final_date = dt.datetime(2025, 1, 10)
backtest.initial_date = dt.datetime(2010, 1, 1)
 
backtest.run_backtest()
