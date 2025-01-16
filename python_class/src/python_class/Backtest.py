
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

        for i in range(len(self.weight.index)):
            if i == 0:
                continue 
            
            price = prices.iloc[i]
            allocation = self.weight.iloc[i]
            portfolio_value.iloc[i] = price.iloc[i]*
            #print(df["ticker" == self.weight.columns[0]].loc[date])

        return 
        # save to csv, use the backtest name 
        
