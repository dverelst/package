import yfinance as yf
import pandas as pd 
from sec_cik_mapper import StockMapper
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging 
from scipy.optimize import minimize
import numpy as np
from pybacktestchain import blockchain
from pybacktestchain import broker
from pybacktestchain import data_module
import os

class Backtest:
    initial_date: datetime
    final_date: datetime
    s: timedelta = timedelta(days=360)
    time_column: str = 'Date'
    company_column: str = 'ticker'
    close_column : str ='Close'
    weight : pd.DataFrame
    initial_cash: int = 1000000  # Initial cash in the portfolio
    name_blockchain: str = 'backtest'
    verbose: bool = True
    broker = broker.Broker(cash=initial_cash, verbose=verbose)
    
    def __post_init__(self):
        self.backtest_name = f"{self.weight.columns}"
        self.broker.initialize_blockchain(self.name_blockchain)

    def run_backtest(self):
        logging.info(f"Running backtest from {self.initial_date} to {self.final_date}.")
        logging.info(f"Retrieving price data for universe")

        # self.initial_date to yyyy-mm-dd format
        init_ = self.initial_date.strftime('%Y-%m-%d')
        
        # self.final_date to yyyy-mm-dd format
        final_ = self.final_date.strftime('%Y-%m-%d')
        
        df = data_module.get_stocks_data(self.weight.columns, init_, final_)

        # Initialize the DataModule
        data_module = data_module.DataModule(df)
        
        portfolio_value = pd.Series(index=self.weight.index, dtype=float)
        daily_pnl = pd.Series(index=self.weight.index.index, dtype=float)
        current_capital = self.initial_cash
        portfolio_value.iloc[0] = current_capital 

        for i, date in enumerate(self.weight.index):
            if i == 0:
                continue 
            
            current_weights = self.weights.loc[date]
            current_prices = df.loc[date]["Close"]
            prev_prices = df.loc[i-1]["Close"]
        
        # Calculate the portfolio allocation for the current day
            allocations = current_capital * current_weights
        
        # Determine the number of shares to hold for each asset
            shares = allocations / prev_prices

        # Compute the new portfolio value based on current prices
            current_portfolio_value = (shares * current_prices).sum()
            portfolio_value.iloc[i] = current_portfolio_value

        # Compute daily PnL
            daily_pnl.iloc[i] = current_portfolio_value - portfolio_value.iloc[i - 1]
        
        # Update the current capital
            current_capital = current_portfolio_value

    # Compute daily returns
        daily_returns = daily_pnl / portfolio_value.shift(1).fillna(self.initial_cash)

    # Calculate the Sharpe ratio
        excess_returns = daily_returns
        sharpe_ratio = excess_returns.mean() / excess_returns.std()



        logging.info(f"Backtest completed. Final portfolio value: {daily_pnl[:, -1]}")

        df.to_csv(f"backtests/{self.backtest_name}.csv")

        # store the backtest in the blockchain
        self.broker.blockchain.add_block(self.backtest_name, df.to_string())

        return daily_pnl, sharpe_ratio
        # save to csv, use the backtest name 
        

import yfinance as yf
import pandas as pd 
from sec_cik_mapper import StockMapper
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging 
from scipy.optimize import minimize
import numpy as np
from pybacktestchain import blockchain
from pybacktestchain import broker
from pybacktestchain import data_module
import os

class Backtest:
    initial_date: datetime
    final_date: datetime
    s: timedelta = timedelta(days=360)
    time_column: str = 'Date'
    company_column: str = 'ticker'
    close_column : str ='Close'
    weight : pd.DataFrame
    initial_cash: int = 1000000  # Initial cash in the portfolio
    name_blockchain: str = 'backtest'
    verbose: bool = True
    broker = broker.Broker(cash=initial_cash, verbose=verbose)
    
    def __post_init__(self):
        self.backtest_name = f"{self.weight.columns}"
        self.broker.initialize_blockchain(self.name_blockchain)

    def run_backtest(self):
        logging.info(f"Running backtest from {self.initial_date} to {self.final_date}.")
        logging.info(f"Retrieving price data for universe")

        # self.initial_date to yyyy-mm-dd format
        init_ = self.initial_date.strftime('%Y-%m-%d')
        
        # self.final_date to yyyy-mm-dd format
        final_ = self.final_date.strftime('%Y-%m-%d')
        
        ticker1 = data_module.get_stock_data(self.weight.columns[0], init_, final_)
        ticker2 = data_module.get_stock_data(self.weight.columns[1], init_, final_)
        ticker1 = ticker1.set_index("Date")["Close"]
        ticker2 = ticker2.set_index("Date")["Close"]

        prices = pd.DataFrame({f"{self.weight.columns[0]}": ticker1, f"{self.weight.columns[1]}": ticker2})

        portfolio_value = pd.Series(index=self.weight.index, dtype=float)
        current_capital = self.initial_cash
        portfolio_value.iloc[0] = current_capital 

        daily_pnl = pd.Series(index=self.weight.index, dtype=float)

        for i, date in enumerate(self.weight.index):
            if i == 0:
                continue 
            
            price = prices.loc[date]
            allocation = self.weight.loc[date]
            print(allocation)
            #print(df["ticker" == self.weight.columns[0]].loc[date])

        return 
        # save to csv, use the backtest name 
        
