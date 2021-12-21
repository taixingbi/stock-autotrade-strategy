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

    def buy(self, name, share, StopPercentage):
        confirmedOrder = self.confirmedOrder[name]
        LOG = confirmedOrder
        if not confirmedOrder:
            success, log = stockBuytrailingStop(name, share, StopPercentage)
            LOG += log
            if success:
                self.updateOrder(name)
                self.log(LOG)
                return True

        self.log(LOG)

    def sell(self, name, share, StopPercentage):
        confirmedOrder = self.confirmedOrder[name]
        LOG = confirmedOrder
        if not confirmedOrder:
            success, log = stockSelltrailingStop(name, share, StopPercentage)
            LOG += log
            if success: 
                self.updateOrder(name)
                self.log(LOG)
                return True

        self.log(LOG)

    def strategy1(self, name, sellShare, sellStopPercentage, buyShare, buyStopPercentage):
        state = self.getState(name)
        print("state", state)

        if state=="buy": 
            if self.buy(name, buyShare, buyStopPercentage):
                self.setState(name, "sell")

        if state=="sell": 
            if self.sell(name, sellShare, sellStopPercentage):
                self.setState(name, "buy")

    def strategy2(self, name, sellShare, sellStopPercentage):
        self.sell(name, sellShare, sellStopPercentage)

    def strategy3(self, name, sellShare, sellStopPercentage, buyShare, buyStopPercentage): # ipo
        print("ipoOrder")
        self.sell(name, sellShare, sellStopPercentage)
        self.buy(name, buyShare, buyStopPercentage)


    def process(self):
        self.updateTimenow()
        print("\n" + self.timenow)

        stocks = self.updateStock()
        for name, sellShare, sellStopPercentage, buyShare, buyStopPercentage, active, mode in stocks:
            self.updateOrder(name)
            if active: 
                # buy sell rotate
                if mode == "strategy1": self.strategy1(name, sellShare, sellStopPercentage, buyShare, buyStopPercentage)
                # sell all
                if mode == "strategy2": self.strategy2(name, sellShare, sellStopPercentage)
                # ipo  1. sell all always 2. buy all 
                if mode == "strategy3": self.strategy3(name, sellShare, sellStopPercentage, buyShare, buyStopPercentage)

            else: 
                self.setState(name, "buy")
