import yfinance as yf
import time

class Investment:

    def __init__(self, stock, price_bought, amount):
        self.stock = stock
        self.price_bought = price_bought
        self.amount = amount

def trade(ticker):
    global funds

    stock = yf.Ticker(ticker)

    print(stock.history(period='1d'))

    # work out price to buy/sell
    
    price_to_buy = 10
    prices_to_sell = [9, 11]
    price = stock.info['regularMarketPrice']

    #wait for stock to get to the price we want to buy it at
    while(price > price_to_buy):
        time.sleep(1)
        price = stock.info['regularMarketPrice']
    
    #buy stock
    investment = Investment(stock, price, funds)
    funds = 0

    #wait for stock to get to price we will sell it at
    while(price > prices_to_sell[0] and price < prices_to_sell[1]):
        time.sleep(1)
        price = stock.info['regularMarketPrice']

    #sell stock
    funds = investment.amount * (price / investment.price_bought)

    if price < prices_to_sell[1]:
        return False

    return True

if __name__ == "__main__":
    stocks = ["BAC", "F", "CSCO", "INTC"]
    funds = 100
    for s in stocks:
        while(funds > 0):
            if trade(s) == False:
                break
            print(funds)