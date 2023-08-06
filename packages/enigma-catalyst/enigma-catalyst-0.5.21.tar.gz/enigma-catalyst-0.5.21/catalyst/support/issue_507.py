from catalyst.api import symbol, get_order, order, get_open_orders
from catalyst.utils.run_algo import run_algorithm


def initialize(context):
    context.asset = symbol("btc_usdt")
    context.index = 0


def handle_data(context, data):


    history = data.history(context.asset, ['close'],
                           bar_count=11,
                           frequency='15T')

    #print('\nnow: %s\n%s' % (data.current_dt, history))
    #if not hasattr(context, 'i'):
    #    context.i = 0
    #context.i += 1
    #print(history)


    #get_order(5, return_price=True)
    print(history)

    context.index += 1


   # print(context.exchanges['poloniex'].get_trades(symbol("xrp_btc"), start_dt=1533081600000))
    #if context.i > 10:
    #    raise Exception('stop')
   #order(symbol("XRP_BTC"), 1)



live = True
if live:
    run_algorithm(initialize=initialize,
                  handle_data=handle_data,
                  exchange_name='cryptopia',
                  quote_currency='btc',
                  algo_namespace='issue-508',
                  live=live,
                  data_frequency='minute',
                  capital_base=0.014,
                  simulate_orders=True
                  )
