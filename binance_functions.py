from binance.client import Client
from binance.helpers import round_step_size
import time

key = "nq4KORrOs13hq59a1bUByJSasGHIALEJr3M0IUXU346kXE0xQ9419GrsQ8Op36aa"
sec = "G5SyNeaUHZqBR06Qr9tuTx25dUTKRYzqgo9im5TDXfod8nWTCpTfnuite5oDoG51"
client = Client(key, sec)



buy_to_sell = {

        "0.1949": 0.2005,
        "0.2005": 0.2059,
        "0.2059": 0.2105,
        "0.2105": 0.2150,
        "0.215": 0.2196,
        "0.2196": 0.2242,
        "0.2242": 0.2288,
        "0.2288": 0.2339,
        "0.2339": 0.2389,
        "0.2389": 0.2440,
        "0.244": 0.2491,
        "0.2491": 0.2542,
        "0.2542": 0.2683,
        "0.230": 0.2320,
        "0.232": 0.2343,
        "0.2343": 0.2367,
        "0.2367": 0.2391,
        "0.2391": 0.2415,
        # "0.2415": 0.2439,
        "0.2415": 0.2510,
        "0.251": 0.2635,
        "0.2439": 0.2464,
        "0.2464": 0.2489,
        "0.2489": 0.2514,
        "0.2514": 0.2539,
        "0.2539": 0.2565,
        "0.2565": 0.2591,
        "0.2591": 0.2617,
        "0.2274": 0.2300,
        "0.2251": 0.2274,
        "0.2228": 0.2251,
        "0.2206": 0.2228,
        "0.2184": 0.2206,
        "0.2162": 0.2184,
        "0.214": 0.2162,
        "0.2119": 0.214,
        "0.2098": 0.2119,
        "0.2077": 0.2098,
        "0.2056": 0.2077,
        "0.2036": 0.2056,
        "0.2015": 0.2036,
        "0.1995": 0.2015,
        "0.1975": 0.1995

    }

sell_to_buy = {

        "0.2491": 0.2440,
        "0.244": 0.2389,
        "0.2389": 0.2339,
        "0.2339": 0.2288,
        "0.2288": 0.2242,
        "0.2242": 0.2196,
        "0.2196": 0.2150,
        "0.215": 0.2105,
        "0.2105": 0.2059,
        "0.2059": 0.2005,
        "0.2005": 0.1949,
        "0.1949": 0.1853,
        "0.2617": 0.2591,
        "0.2591": 0.2565,
        "0.2565": 0.2539,
        "0.2539": 0.2514,
        "0.2514": 0.2489,
        "0.2489": 0.2464,
        "0.2464": 0.2439,
        "0.2439": 0.2415,
        # "0.2415": 0.2391,
        "0.2391": 0.2367,
        "0.2367": 0.2343,
        "0.2343": 0.2320,
        "0.232": 0.2300,
        "0.230": 0.2274,
        "0.2274": 0.2251,
        "0.2251": 0.2228,
        "0.2228": 0.2206,
        "0.2206": 0.2184,
        "0.2184": 0.2162,
        "0.2162": 0.2140,
        "0.214": 0.2119,
        "0.2119": 0.2098,
        "0.2098": 0.2077,
        "0.2077": 0.2056,
        "0.2056": 0.2036,
        "0.2036": 0.2015,
        "0.2015": 0.1995,
        "0.1995": 0.1975,
        "0.251": 0.2415,
        "0.2635": 0.2510

    }




def get_ticker_step(symbols_all, preis, exec_token_amount, orderid_price, side, id, array_orderids):
    global stepSize
    ticketSize = client.get_exchange_info()
    for l in ticketSize["symbols"]:
        if l["symbol"] == symbols_all:
            for a in l["filters"]:
                if a["filterType"] == "PRICE_FILTER":
                    b = a["tickSize"]
                    price = str(round_step_size(preis, b))
                    orderid_price.append(price)
                    if side == "BUY":
                        sell_price = buy_to_sell.get(price)
                        orderid_price.append(sell_price)
                    elif side == "SELL":
                        buy_price = sell_to_buy.get(price)
                        orderid_price.append(buy_price)


    tickerSize = client.get_exchange_info()
    for p in tickerSize["symbols"]:
        if p["symbol"] == symbols_all:
            for ba in p["filters"]:
                if ba["filterType"] == "LOT_SIZE":
                    stepSize = ba["stepSize"]
                    cut_token = round_step_size(exec_token_amount, stepSize)
                    orderid_price.append(cut_token)

    get_order_status(symbols_all, id, side, stepSize, array_orderids, orderid_price)



def get_order_status(symbols_all, id, side, stepSize, array_orderids, orderid_price):
    order_status = client.get_order(
        symbol=symbols_all,
        orderId=id
    )

    if order_status["status"] == "FILLED":
        if side == "BUY":
            for a in array_orderids:
                if a[0] == id:
                    new_sell_price = a[3]
                    quantity = a[2]

                    create_sell_order(symbols_all, quantity, new_sell_price)

                    array_orderids.clear()
                    orderid_price.clear()
        elif side == "SELL":
            for a in array_orderids:
                if a[0] == id:
                    new_buy_price = a[3]

                    cut_token_amount = float(order_status["cummulativeQuoteQty"]) / float(new_buy_price)
                    new_token_amount = round_step_size(cut_token_amount, stepSize)

                    create_buy_order(symbols_all, new_token_amount, new_buy_price)

                    array_orderids.clear()
                    orderid_price.clear()
        print(f"Checke Order: {id}...")
        time.sleep(1)
        print("Status: - Ausgeführt -")

    elif order_status["status"] == "CANCELED":
        print(f"Checke Order: {id}...")
        print("Status: - Abgebrochen -")
    else:
        print(f"Checke Order: {id}...")
        time.sleep(1)
        print("Status: - Offen -")

def create_sell_order(symbols_all, quantity, new_sell_price):
    buy = client.order_limit_sell(
        symbol=symbols_all,
        quantity=quantity,
        price=new_sell_price
    )

def create_buy_order(symbols_all, new_token_amount, new_buy_price):
    sell = client.order_limit_buy(
        symbol=symbols_all,
        quantity=new_token_amount,
        price=new_buy_price
    )