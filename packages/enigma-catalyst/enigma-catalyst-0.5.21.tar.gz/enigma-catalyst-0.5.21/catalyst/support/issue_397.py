"""
    This is a very simple example referenced in the beginner's tutorial:
    https://enigmampc.github.io/catalyst/beginner-tutorial.html

    Run this example, by executing the following from your terminal:
      catalyst ingest-exchange -x bitfinex -f daily -i btc_usdt
      catalyst run -f buy_btc_simple.py -x bitfinex --start 2016-1-1 \
        --end 2017-9-30 -o buy_btc_simple_out.pickle

    If you want to run this code using another exchange, make sure that
    the asset is available on that exchange. For example, if you were to run
    it for exchange Poloniex, you would need to edit the following line:

        context.asset = symbol('btc_usdt')     # note 'usdt' instead of 'usd'

    and specify exchange poloniex as follows:
    catalyst ingest-exchange -x poloniex -f daily -i btc_usdt
    catalyst run -f buy_btc_simple.py -x poloniex --start 2016-1-1 \
        --end 2017-9-30 -o buy_btc_simple_out.pickle

    To see which assets are available on each exchange, visit:
    https://www.enigma.co/catalyst/status
"""
from catalyst import run_algorithm
from catalyst.api import order, record, symbol
import pandas as pd
import time


def initialize(context):
    context.asset1 = symbol('btc_usdt')
    context.asset2 = symbol('bch_btc')


def handle_data(context, data):
    time.sleep(10)
    #order(context.asset, 1)
    #record(btc=data.current(context.asset, 'price'))
    history = data.history([context.asset1], 'close', bar_count=2, frequency='1m')
                     #, context.asset2],
                 #['close', 'volume'],
                 #bar_count=3,
                 #frequency='1D')

    #order(context.asset, 1)

    print(history)


if __name__ == '__main__':
    run_algorithm(
        capital_base=10000,
        data_frequency='minute',
        initialize=initialize,
        handle_data=handle_data,
        exchange_name='binance',
        algo_namespace='buy_btc_simple',
        quote_currency='eur',
        start=pd.to_datetime('2018-09-21', utc=True),
        end=pd.to_datetime('2018-09-22', utc=True),
    )
