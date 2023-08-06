from catalyst.api import symbol, order
from catalyst.utils.run_algo import run_algorithm

import pandas as pd


def initialize(context):
    pass


def handle_data(context, data):
    history = data.history(symbol("btc_usd"), ['close'],
                 bar_count=5, frequency='1T')

    print(history)

    order(symbol("btc_usd"), 0.1)


live = True

run_algorithm(initialize=lambda ctx: True,
              handle_data=handle_data,
              exchange_name='bitfinex',
              quote_currency='usd',
              algo_namespace='issue-475',
              live=live,
              data_frequency='minute',
              capital_base=3000,
              #start=pd.to_datetime('2018-08-12', utc=True),
              #end=pd.to_datetime('2018-08-13', utc=True),
              )
