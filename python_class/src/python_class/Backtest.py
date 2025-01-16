import yfinance as yf
import pandas as pd 
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging 
import numpy as np
from python_class import Cointegration

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
    
    def __post_init__(self):
        self.backtest_name = f"{self.weight.columns}"

    def run_backtest(self):
        logging.info(f"Running backtest from {self.initial_date} to {self.final_date}.")
        logging.info(f"Retrieving price data for universe")

        # self.initial_date to yyyy-mm-dd format
        init_ = self.initial_date.strftime('%Y-%m-%d')
        # self.final_date to yyyy-mm-dd format
        final_ = self.final_date.strftime('%Y-%m-%d')
        
        returns1 = Cointegration.log_returns(f"{self.weight.columns[0]}",init_, final_)
        returns2 = Cointegration.log_returns(f"{self.weight.columns[1]}", init_, final_)

        returns = pd.DataFrame({f"{self.weight.columns[0]}": returns1, f"{self.weight.columns[1]}": returns2})
        returns_strat = pd.DataFrame(columns = ["Portfolio returns", "Portfolio Value"], index = self.weight.index)

        for i in range(len(self.weight.index)):
            returns_strat.iloc[i, 0] = self.weight.iloc[i].T @ returns.iloc[i]
            if i == 0:
                returns_strat.iloc[i, 1] = self.initial_cash*(1+returns_strat.iloc[i, 0])

            else:
                returns_strat.iloc[i, 1] = returns_strat.iloc[i-1, 1]*(1+returns_strat.iloc[i, 0])

        return returns_strat["Portfolio Value"]
        # save to csv, use the backtest name 
        
