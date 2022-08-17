from decimal import Decimal

class StockTrader():
    def __init__(self, name, password, bal, portfolioRecord):
        self.name = name
        self.__password = password
        self.__bal = float(bal)
        self.__portfolio = portfolioRecord

    def buy(self, coin, money, price):
        if coin not in self.__portfolio:
            self.__portfolio[coin] = Decimal(0.0)
        self.__portfolio[coin] += Decimal(money / price)
        self.__bal -= float(money)
    
    def sell(self, coin, amount, price):
        self.__portfolio[coin] -= Decimal(amount)
        self.__bal += float(amount * price)

    def getName(self):
        return self.name

    def getPassword(self):
        return self.__password

    def getBal(self):
        return self.__bal
    
    def getPortfolio(self):
        return self.__portfolio
