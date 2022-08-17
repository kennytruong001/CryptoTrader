import requests
import hashlib
import boto3

import display
import stocktrader
#Database: AWS DynamoDB
table_name = "CryptoTrader"
client = boto3.client('dynamodb')
table = boto3.resource('dynamodb').Table(table_name)

# item_richard = {
#     "User":{
#         "S": "richard"
#     },
#     "Password":{
#         "S": "4573a839ffe27bbd6a9305d6ea6617b7332a5cb8659fbfdc256fe917eda0a79e"
#     },
#     "Balance": {
#         "S": "5000.00"
#     },
#     "Portfolio": {
#         "L": [
#             {
#                 "M": {
#                     "dogecoin": {
#                         "S": "100"
#                     }
#                 }
#             }
#         ]
#     }
# }
item_get = {
    "User":{
        "S": "richard"
    }
}
    # "Password":{
    #     "S": "4573a839ffe27bbd6a9305d6ea6617b7332a5cb8659fbfdc256fe917eda0a79e"
    # },
    # "Balance": {
    #     "S": "5000.00"
    # },
    # "Portfolio": {
    #     "L": [
    #         {
    #             "M": {
    #                 "dogecoin": {
    #                     "S": "100"
    #                 }
    #             }
    #         }
    #     ]
    # }
#}
#db.put_item(TableName = table_name, Item = item_richard)
#response = db.get_item(TableName=table_name, Key = item_get)
#response = table.get_item(Key={'User':'richard'})
#print(response["Item"]['Portfolio'][0]['dogecoin'])
# response = requests.get("https://valorant-api.com/v1/weapons")

# response = response.json()
# response_data = response["data"]
# #data_dict = response_data.keys()
# for item in response_data:
#     weapon = item["displayName"]
#     fireRate = item["weaponStats"]["fireRate"]
#     category = item["category"].replace("EEquippableCategory::", "")
#     gunPic = item["displayIcon"]
#     print(f"{weapon}({category})'s fire rate: {fireRate}                 link to pic->{gunPic}")
#     #print(item["displayIcon"])

# response = requests.get("https://www.fruityvice.com/api/fruit/all").json()

# for fruit in response:
#     fruitName = fruit["name"]
#     sugar = fruit["nutritions"]["sugar"]
#     print(f"{fruitName} has {sugar}g of sugar")

#userRecord = {}
cryptoList = []
columns = ["User", "Password", "Balance", "Portfolio"]
#portfolioRecord = {}
response = requests.get("https://api.coingecko.com/api/v3/coins/").json()

for item in response:
    cryptoList.append(item["id"])

# recordFile = open("record.txt", "r+")
# for line in recordFile:
#     username, password, bal, portfolio= line.strip().split(",")
#     if portfolio != '':
#         portfolioList = portfolio.split(";") #list of strings
#         for item in portfolioList:
#             if item != '':
#                 portfolio_key, portfolio_value = item.split(":")
#             portfolioRecord[portfolio_key] = float(portfolio_value)
#     userRecord[username] = stocktrader.StockTrader(username, password, bal, portfolioRecord)
#     portfolioRecord = {}

display.Display.displayMainMenu()
action = input()

while True:
    if action == "1":
        input_name = input("Username: ")
        input_pass = input("Password: ")
        sha256_pass = hashlib.sha256(input_pass.encode())
        userInfo = table.get_item(Key={"User":input_name})["Item"]
        #if sha256_pass.hexdigest() == userRecord[input_name].getPassword():
        if sha256_pass.hexdigest() == userInfo["Password"]:
            print(f"Welcome back {input_name}!")
            user = stocktrader.StockTrader(userInfo["User"], userInfo["Password"], userInfo["Balance"], userInfo["Portfolio"])
            break
        else:
            print("User does not exist! Please try again.")

    elif action == "2":
        input_name = input("What username would you like?: ")
        input_pass = input("What password would you like?: ")
        sha256_pass = hashlib.sha256(input_pass.encode())
        trader = stocktrader.StockTrader(input_name, sha256_pass, 10000)
        print(f"Welcome {input_name}!")
        break
    else:
        print("Invalid input, please try again")
        display.Display.displayMenu()
        action = input()

display.Display.displayTradingMenu()
action = input()
while True:
    if action == "1":
        cryptocoin2buy = input("What cryptocurrency would you like to buy?: ")
        while (cryptocoin2buy not in cryptoList):
            print("That cryptocoin does not exist in CryptoTrader, try again")
            cryptocoin2buy = input("What cryptocurrency would you like to buy?: ")
        amount = float(input("How much would you like to buy in USD?: "))

        cryptocoin = requests.get(f"https://api.coingecko.com/api/v3/coins/{cryptocoin2buy}").json()
        price = cryptocoin["market_data"]["current_price"]["usd"]
        user.buy(cryptocoin2buy, amount, price)


        print(f"{input_name} bought ${amount} worth of {cryptocoin2buy}. You now own {user.getPortfolio()[cryptocoin2buy]}.")
        display.Display.displayTradingMenu()
        action = input()

    elif action == "2":
        cryptocoin2sell = input("What cryptocurrency would you like to sell?: ")
        while (cryptocoin2sell not in cryptoList):
            print("That cryptocoin does not exist in CryptoTrader, try again")
            cryptocoin2sell = input("What cryptocurrency would you like to sell?: ")
        amount = float(input("How much of the currently do you want to sell: "))

        cryptocoin = requests.get(f"https://api.coingecko.com/api/v3/coins/{cryptocoin2sell}").json()
        price = cryptocoin["market_data"]["current_price"]["usd"]
        user.sell(cryptocoin2sell, amount, price)

        print(f"{input_name} sold ${amount} {cryptocoin2sell}. Your balance is now {user.getBal()}.")

        #userRecord[input_name].portfolio = {k:v for k,v in userRecord[input_name].portfolio.items() if v==0.0}

        display.Display.displayTradingMenu()
        action = input()

    elif action == "3":
        # for coin in userRecord[input_name].portfolio:
        #     print(coin)
        print(user.getPortfolio())
        display.Display.displayTradingMenu()
        action = input()
    
    elif action == "4":
        print(f"Your balance is ${user.getBal()}.")
        display.Display.displayTradingMenu()
        action = input()
    
    elif action == "5":
        cryptocoin2check = input("What cryptocurrency would you like to check?: ")
        while (cryptocoin2check not in cryptoList):
            print("That cryptocoin does not exist in CryptoTrader, try again")
            cryptocoin2check = input("What cryptocurrency would you like to check?: ")

        cryptocoin = requests.get(f"https://api.coingecko.com/api/v3/coins/{cryptocoin2check}").json()
        price = cryptocoin["market_data"]["current_price"]["usd"]
        print(f"{cryptocoin2check} is currently ${price}")

        display.Display.displayTradingMenu()
        action = input()

    elif action == "6":

        # recordFile = open("record.txt", "w")
        # first = True
        # for user in userRecord.values():
        #     if first:
        #         recordFile.write(f"{user.name},{user.getPassword()},{user.getBal()},")
        #         first = False
        #     else: 
        #         recordFile.write(f"\n{user.name},{user.getPassword()},{user.getBal()},")

        #     for coin in user.getPortfolio():
        #         recordFile.write(f"{coin}:{user.getPortfolio()[coin]};")
        table.put_item(Item={
            columns[0] : user.getName(),
            columns[1] : user.getPassword(),
            columns[2] : str(user.getBal()),
            columns[3] : user.getPortfolio()
        })
        print("Thanks for using Crypto-Trader!")
        break
    else:
        print("Not valid action! Try something else.")
        display.Display.displayTradingMenu()
        action = input()



# ticker = cryptocoin["tickers"][0]["base"]
# ath = cryptocoin["market_data"]["ath"]["usd"]
# atl = cryptocoin["market_data"]["atl"]["usd"]
# market_cap = cryptocoin["market_data"]["market_cap"]["usd"]
# total_vol = cryptocoin["market_data"]["total_volume"]["usd"]
# high24h = cryptocoin["market_data"]["high_24h"]["usd"]
# low24h = cryptocoin["market_data"]["low_24h"]["usd"]

# "price_change_24h": -57.1515167406,
# "price_change_percentage_24h": -0.24555,
# "price_change_percentage_7d": 12.84514,
# "price_change_percentage_14d": 7.18868,
# "price_change_percentage_30d": 12.15784,
# "price_change_percentage_60d": -23.50278,
# "price_change_percentage_200d": -51.00427,
# "price_change_percentage_1y": -28.30452,

#trader.buy(ticker, 10000, price)
#print(f"Bitcoin({ticker}) is currently ${price}, with All-time High of ${ath} and All-time Low of ${atl}. Market cap is ${market_cap} with total volume of {total_vol}")

#recordFile.close()
#print(trader.portfolio)
