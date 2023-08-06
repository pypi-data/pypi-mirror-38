from catalyst.api import symbol, order, get_order, get_open_orders#, get_orderbook
from catalyst.utils.run_algo import run_algorithm
import pandas as pd

import csv
import os

def initialize(context):
    context.csvfile = open(os.path.splitext(
         os.path.basename(__file__))[0] + '.csv', 'w+')

    context.csvwriter = csv.writer(context.csvfile)

    context.pricing_data = pd.DataFrame()

    context.index = 0


def handle_data(context, data):
    context.asset = symbol("btc_usd")
    current = data.history(context.asset, ['price', 'volume'],
                 bar_count=1, frequency='1T')

    price = data.current(context.asset, 'price')
    volume = data.current(context.asset, 'volume')

    #pd.set_option("display.precision", 8)
    #print(history)

    context.pricing_data = context.pricing_data.append(current)
    context.csvwriter.writerow([current.index[0],
                                 current.iloc[0]['price'],
                                 current.iloc[0]['volume']])
    if context.index == 0 or context.index == 2 or context.index == 4:
        order(context.asset, 1)
        for item, orders in get_open_orders().items():
            o = orders[0]
            get_order(o.sid)

    elif context.index == 6:
        order(context.asset, -1)

    elif context.index == 8:
        order(context.asset, -1)

    if context.portfolio.positions:
        position = context.portfolio.positions[context.asset]
        print("index={}".format(context.index))
        print("amount={}, cost-basis={}".format(position.amount, position.cost_basis))

    #
    # context.csvwriter.writerow([data.current_dt,
    #                             current.iloc[0]['price'],
    #                             current.iloc[0]['volume']])

    #print(context.blotter.current_dt)
    #print(data.current_dt)

    context.index += 1

def analyze(context=None, results=None):
    # Close open file properly at the end

    context.pricing_data.to_csv(os.path.splitext(
        os.path.basename(__file__))[0] + '2.csv')

    context.csvfile.close()






results = run_algorithm(initialize=initialize,
              handle_data=handle_data,
              analyze=analyze,
              exchange_name='poloniex',
              quote_currency='usd',
              algo_namespace='issue-430',
              live=False,
              data_frequency='minute',
              capital_base=3000,
              start=pd.to_datetime('2018-08-1', utc=True),
              end=pd.to_datetime('2018-09-1', utc=True),
              )

print("hi")