import pandas as pd
from stock.module import *

from model.log import *
from model.order import *
import json
import time
import re 

# state
# 1 init
# 11 readyToBuy
# 11 confirmedBuy
# 12 filleddBuy
# 21 readyToSell
# 22 confirmedSell
# 23 filledSell

class TraderStock:
    def __init__(self):
        self.log_crud = Log_crud()
        self.order_crud = Order_crud()
        self.timenow = getTimeNow()
        # activeOrder1
        self.state = {}
        self.confirmedOrder = {}

    def log(self, log):
        print(log)
        self.log_crud.create(self.timenow, log)
        self.log_crud.delete()

    def setState(self, name, state):
        self.state[name] = state

    def getState(self, name):
        if name not in self.state:
            self.state[name] = "buy"
        return self.state[name]

    def updateTimenow(self):
        self.timenow = getTimeNow()

    def updateStock(self):
        stocks =  self.order_crud.read()
        return stocks

    def updateOrder(self, name):
        self.confirmedOrder[name] = getConfirmedOrder(name)

    def buy(self, name, buyShare, buyStopPercentage):
        LOG = ""
        if not self.confirmedOrder[name]:
            print("buy")
            res = stockBuytrailingStop(name, buyShare, buyStopPercentage)
            LOG += " " + name + " trailing stop buy " + str(res)
            if "id" in res:
                self.updateOrder(name)
                self.log(LOG)
                return True
        else:
            LOG += " " + self.confirmedOrder[name]

        self.log(LOG)

    def sell(self, name, sellShare, sellStopPercentage):
        LOG = ""
        isStockHaveShare, shareHold = stock_have_share(name)
        if not sellShare:   sellShare = shareHold

        if not self.confirmedOrder[name]:
            print("sell")
            res = stockSelltrailingStop(name, sellShare, sellStopPercentage)
            LOG += " " + name + " trailing stop sell " + str(res)

            if "detail" in res and "Not enough shares to sell" in res["detail"]:
                res = stockSelltrailingStop(name, shareHold, sellStopPercentage)
                LOG += " share " + str(sellShare) + " udpated to " + str(shareHold) + " " + name + " trailing stop sell " + str(res)

            if "id" in res:
                self.updateOrder(name)
                self.log(LOG)
                return True
         
        else:
            LOG += " " + self.confirmedOrder[name]

        if sellShare == 0: LOG += " SELL ALL"

        self.log(LOG)

    def activeOrder1(self, name, sellShare, sellStopPercentage, buyShare, buyStopPercentage):
        state = self.getState(name)
        if state=="buy": 
            if self.buy(name, buyShare, buyStopPercentage):
                self.setState(name, "sell")

        if state=="sell": 
            if self.sell(name, sellShare, sellStopPercentage):
                self.setState(name, "buy")

    def activeOrder2(self, name, sellShare, sellStopPercentage):
        self.sell(name, sellShare, sellStopPercentage)

    def ipoOrder(self):
        print("ipoOrder")


    def process(self):
        self.updateTimenow()
        print("\n" + self.timenow)

        stocks = self.updateStock()
        for name, sellShare, sellStopPercentage, buyShare, buyStopPercentage, active in stocks:
            self.updateOrder(name)
            if active: 
                if buyShare > 0: self.activeOrder1(name, sellShare, sellStopPercentage, buyShare, buyStopPercentage)
                if buyShare == 0: self.activeOrder2(name, sellShare, sellStopPercentage)
            else: 
                if name in self.state: self.state[name]
