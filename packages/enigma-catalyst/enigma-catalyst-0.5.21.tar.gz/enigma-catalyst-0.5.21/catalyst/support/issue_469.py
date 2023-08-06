from catalyst.api import symbol, get_order, order, get_open_orders
from catalyst.utils.run_algo import run_algorithm


def initialize(context):
    context.asset = symbol("bat_btc")
    context.index = 0


def handle_data(context, data):

    if context.index == 0:
        order(symbol("bat_btc"), -9.9, limit_price=0.00002630)

    print("blotter={}".format(context.blotter.orders))


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
    print("open orders={}".format(get_open_orders(context.asset)))

    context.index += 1


   # print(context.exchanges['poloniex'].get_trades(symbol("xrp_btc"), start_dt=1533081600000))
    #if context.i > 10:
    #    raise Exception('stop')
   #order(symbol("XRP_BTC"), 1)



live = True
if live:
    run_algorithm(initialize=initialize,
                  handle_data=handle_data,
                  exchange_name='poloniex',
                  quote_currency='btc',
                  algo_namespace='issue-469',
                  live=live,
                  data_frequency='minute',
                  capital_base=0.014,
                  simulate_orders=False,
                  auth_aliases=dict(poloniex='auth3')#poloniex,auth3"
                  #start=pd.to_datetime('2017-09-14', utc=True),
                  #end=pd.to_datetime('2018-08-01', utc=True),
                  )
