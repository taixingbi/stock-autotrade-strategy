
# https://readthedocs.org/projects/robin-stocks/downloads/pdf/latest/
from datetime import datetime
from pytz import timezone

from yahoo_fin import stock_info as si
import cryptocompare

import os
import robin_stocks.robinhood as rs

from django.conf import settings

CRYPTO= ["BTC", "DOGE", "ETH"]


# ----------------------- login  -----------------------
def login():
    print("login successfully")
    robinUser = os.environ.get("robinhood_username")
    robinPass = os.environ.get("robinhood_password")

    res= rs.login(username=robinUser,
            password=robinPass,
            expiresIn=86400,
            by_sms=True)
    # print(res)
    return rs

rs = login()

# get time
def getTimeNow():
    timenow = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
    return timenow

# ----------------------- check real time price peak price -----------------------
class CheckPrice:
    def __init__(self, name):
        self.name = name
        self.peakPrice = 0

    def live(self):
        # print("livePrice")
        live_price = 0
        if self.name in CRYPTO: 
            response= cryptocompare.get_price(self.name, currency='USD') 
            live_price= response[self.name]['USD']
        else:
            # live_price= si.get_live_price(self.name) 
            # live_price= live_price.item() # numpy to float
            try:
                live_price = rs.stocks.get_latest_price(self.name, includeExtendedHours=True)
                if live_price[0]:
                    live_price = round( float(live_price[0]), 2)
                else:
                    live_price = 0.00
            except:
                print(self.name + ' price does not exist in Robinhood yet\n')
                return 0

        # timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # timestamp = time.time()
        return live_price

    def getShareDecimal(self, price):
        return round(1.0 * price/self.live(), 5)

    def getShare(self, price):
        return int(1.0 * price/self.live() )

    def peak(self):
        livePrice = self.live()
        print(self.peakPrice, livePrice)
        if self.peakPrice < livePrice : 
            self.peakPrice = livePrice
        return self.peakPrice # $30

# ----------------------- check my stock -----------------------
def check_my_stocks(name):
    my_stocks = rs.build_holdings()
    # print(my_stocks)
    for key, stock in my_stocks.items():
        if key == name : return stock

    return None

def stock_have_share(name):
    stock = check_my_stocks(name)
    print(stock)
    if stock: 
        shares_float = float(stock['quantity']) 
        return shares_float > 1, int(shares_float) 
    return False, 0

# ----------------------- order stock -----------------------
# triger a market sell order if stock falls to
def stock_sell_stop(name, share, price):
    res = rs.orders.order_sell_stop_loss(name,
                                share,
                                price,
                                timeInForce='gtc',
                                extendedHours=True,
                                jsonify=True)
    print(res)
# stock_sell_limit("TQQQ", 1, 150)

def stock_sell(name, share):
    res = rs.orders.order_sell_market(name,
                                share,
                                timeInForce='gtc',
                                extendedHours=False,
                                jsonify=True)
    print(res)

def stockSelltrailingStop(name, share, percentage):
    try:
        res = rs.orders.order_sell_trailing_stop(   name, 
                                                    share, 
                                                    percentage,
                                                    trailType= 'percentage',
                                                    timeInForce= 'gtc', 
                                                    extendedHours= False,
                                                    jsonify=True)
        print(res)
        return res
    except: 
        return "order_sell_trailing_stop " + name + " does not exist" 

def stockBuytrailingStop(name, share, percentage):
    try:
        res = rs.orders.order_buy_trailing_stop(    name, 
                                                    share, 
                                                    percentage,
                                                    trailType= 'percentage',
                                                    timeInForce= 'gtc', 
                                                    extendedHours= False,
                                                    jsonify=True)
        return res
    except:
        return "order_buy_trailing_stop " + name + " does not exist" 


# triger a market buy order if stock rises to
def stockBuyStop(name, share, price):
    res= rs.orders.order(   name, 
                            share, 
                            "buy", 
                            limitPrice=None, 
                            stopPrice= price, 
                            timeInForce='gtc', 
                            extendedHours=False, 
                            jsonify=True)
    print(res)

    try:
        res['id']
        return True
    except:
        print("stock_buy_stop failed")
        return False

    # {'detail': 'Only accepting immediate limit orders for this symbol since it has not traded yet.'}
# stock_buy_stop("QQQ", 1, 500)
def cancel_stock_order(order_id):
    if order_id:
        rs.orders.cancel_stock_order(order_id)

def getInstrumentId(name):
    try:
        res = rs.stocks.find_instrument_data(name)
        instrumentId = res[0]['id']
        return instrumentId
    except:
        pass
    return None

def getConfirmedOrder(name):
    instrumentId = getInstrumentId(name)
    if not instrumentId: return ""

    openStockOrders = rs.orders.get_all_open_stock_orders()
    for openStockOrder in openStockOrders:
        if openStockOrder['instrument_id'] == instrumentId :
            # print(openStockOrder)
            return  name  \
                    + " " + openStockOrder['side'] \
                    + " share: " + str(int(float(openStockOrder['quantity']))) \
                    + " stopPrice: $" + str(round(float(openStockOrder['stop_price']),2)) \
                    + " " + openStockOrder['state']

    return ""
#             
# filled             the order was filled
# queued             the order was queued till 9:30 open to confirm
# confirmed          the order was confirmed, waiting for trigger  
# cancelled          the order was cancelled
# failed             the order does not exist

def getallOpenStockOrders():
    res = rs.orders.get_all_open_stock_orders()
    print(res)
    return res


# ----------------------- triger -----------------------

if __name__ == "__main__":
    res = stockSelltrailingStop("UVXYA", 1000000000, 1)
    print(res)