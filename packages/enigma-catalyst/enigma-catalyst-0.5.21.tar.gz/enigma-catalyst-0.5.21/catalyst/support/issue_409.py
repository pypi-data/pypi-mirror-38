from catalyst.api import symbol, get_order, order, get_open_orders
from catalyst.utils.run_algo import run_algorithm
import pandas as pd


def initialize(context):
    pass


def handle_data(context, data):
    sym = symbol("XRP_BTC")
    #res = data.can_trade(sym)

    #history = data.history(symbol("bch_btc"), ['close'],
    #                       bar_count=11,
    #                       frequency='5T')

    #print('\nnow: %s\n%s' % (data.current_dt, history))
    #if not hasattr(context, 'i'):
    #    context.i = 0
    #context.i += 1
    #print(history)


    #get_order(5, return_price=True)
    print(get_open_orders(sym))

   # print(context.exchanges['poloniex'].get_trades(symbol("xrp_btc"), start_dt=1533081600000))
    #if context.i > 10:
    #    raise Exception('stop')
   #order(symbol("XRP_BTC"), 1)



live = True
if live:
    run_algorithm(initialize=lambda ctx: True,
                  handle_data=handle_data,
                  exchange_name='poloniex',
                  quote_currency='btc',
                  algo_namespace='issue-409',
                  live=live,
                  data_frequency='minute',
                  capital_base=0.015,
                  simulate_orders=False,
                  auth_aliases=dict(poloniex='auth3')#poloniex,auth3"
                  #start=pd.to_datetime('2017-09-14', utc=True),
                  #end=pd.to_datetime('2018-08-01', utc=True),
                  )
