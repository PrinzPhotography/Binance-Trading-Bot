from binance.client import Client
from binance import AsyncClient, BinanceSocketManager
from datetime import datetime
from binance import AsyncClient
from binance.enums import *
import config
import pandas as pd
import time
import PySimpleGUI as sg
from colorama import Fore
from colorama import Style

client = Client(config.apiKey, config.apiSecurity)

buy_to_sell = {

    "0.2059": "0.2105",
    "0.2105": "0.2150",
    "0.2150": "0.2196",
    "0.2196": "0.2242",
    "0.2242": "0.2288",
    "0.2288": "0.2339",
    "0.2339": "0.2389",
    "0.2389": "0.2440",
    "0.2440": "0.2491",


}

sell_to_buy = {

    "0.2491": "0.2440",
    "0.2440": "0.2389",
    "0.2389": "0.2339",
    "0.2339": "0.2288",
    "0.2288": "0.2242",
    "0.2242": "0.2196",
    "0.2196": "0.2150",
    "0.2150": "0.2105",
    "0.2105": "0.2059"

}


array_orderids = []

while True:
    orders = client.get_open_orders()
    for o in orders:
        orderid_price = []
        id = o["orderId"]
        preis = o["price"]
        price = preis[:6]
        exec_token_amount = o["origQty"]

        orderid_price.append(id)
        orderid_price.append(price)
        orderid_price.append(exec_token_amount)


        if o["side"] == "BUY":
            sell_price = buy_to_sell.get(price)
            orderid_price.append(sell_price)
        elif o["side"] == "SELL":
            buy_price = sell_to_buy.get(price)
            orderid_price.append(buy_price)

        array_orderids.append(orderid_price)

        order_status = client.get_order(
            symbol='NULSUSDT',
            orderId=id
        )

        if order_status["status"] == "FILLED":
            if o["side"] == "BUY":
                for a in array_orderids:
                    if a[0] == id:
                        new_sell_price = a[3]
                        buy = client.order_limit_buy(
                            symbol="NULSUSDT",
                            quantity=a[2],
                            price=new_sell_price
                        )
                        array_orderids.clear()
                        orderid_price.clear()
            elif o["side"] == "SELL":
                for a in array_orderids:
                    if a[0] == id:
                        new_buy_price = a[3]
                        new_token_amount = order_status["cummulativeQuoteQty"] / new_buy_price
                        sell = client.order_limit_sell(
                            symbol="NULSUSDT",
                            quantity=new_token_amount,
                            price=new_buy_price
                        )
                        array_orderids.clear()
                        orderid_price.clear()

            print(f"Order {id} ist durch")
        else:
            print(f"Order {id} ist offen")



# array_orderids = []
# array_tradeids = []
#
# for o in orders:
#     orderid_price = []
#     id = o["orderId"]
#     preis = o["price"]
#     price = preis[:6]
#
#     orderid_price.append(id)
#     orderid_price.append(price)
#
#     if o["side"] == "BUY":
#         sell_price = buy_to_sell.get(price)
#         orderid_price.append(sell_price)
#     elif o["side"] == "SELL":
#         buy_price = sell_to_buy.get(price)
#         orderid_price.append(buy_price)
#
#     array_orderids.append(orderid_price)
#
# while True:
#     time.sleep(2)
#     trades = client.get_my_trades(symbol='NULSUSDT')
#
#     for t in trades:
#         tradeid = t["orderId"]
#         if tradeid not in array_tradeids:
#             array_tradeids.append(tradeid)
#
#     for a in array_orderids:
#         if 266677654 in array_tradeids:
#             print("ID gefunden: 266677654")
#             break
#         else:
#             print("ID nicht gefunden")