from binance.client import Client
from binance.helpers import round_step_size
import time
import binance_functions

while True:

    key = "nq4KORrOs13hq59a1bUByJSasGHIALEJr3M0IUXU346kXE0xQ9419GrsQ8Op36aa"
    sec = "G5SyNeaUHZqBR06Qr9tuTx25dUTKRYzqgo9im5TDXfod8nWTCpTfnuite5oDoG51"
    client = Client(key, sec)


    array_orderids = []

    orders = client.get_open_orders()

    for o in orders:
        orderid_price = []
        id = o["orderId"]
        preis = o["price"]
        symbols_all = o["symbol"]
        exec_token_amount = o["origQty"]
        side = o["side"]

        orderid_price.append(id)

        binance_functions.get_ticker_step(symbols_all, preis, exec_token_amount, orderid_price, side, id, array_orderids)

