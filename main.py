import os
from binance.client import Client
from binance.helpers import round_step_size
from datetime import datetime
import time
import PySimpleGUI as sg
import csv


# # Accountinfos
# accountInfo = client.get_account()
# for a in accountInfo["balances"]:
#     if float(a["locked"]) > 0 or float(a["free"]) > 0:
#         print(a)

#
# # Alle Trades ansehen
# trades = client.get_my_trades(symbol=nuls)
#
# # Alle Order einsehen
# allOrders = client.get_all_orders(symbol="NULSUSDT")
#
# # Offene Order einsehen
# openOrders = client.get_open_orders(symbol='NULSUSDT')
#
# # Guthaben von Tokens
#balance = client.get_asset_balance(asset='NULS')
#
# # Token Details
# details = client.get_asset_details(asset="NULS")
#
# # Tokenpreise
# price_nuls = client.get_symbol_ticker(symbol=nuls)

# Kauforder erstellen
# buy = client.order_limit_buy(
#     symbol='',
#     quantity=,
#     price=''
# )
# # Verkauforder erstellen
# sell = client.order_limit_sell(
#     symbol='',
#     quantity=,
#     price=''
# )

# # Status der Order checken
# order = client.get_order(
#     symbol='NULSUSDT',
#     orderId='202500466'
# )

# Live Preis
# data = {"Token": [prices["symbol"]],
#         "Preis": [prices["price"]]
#         }
#
# posframe = pd.DataFrame(data)

# while True:
#     print(posframe)
#     prices = client.get_symbol_ticker(symbol=symbol)
#     new_row = {"Token": [prices["symbol"]],
#                "Preis": [prices["price"]]
#                }
#     posframe = posframe.append(new_row, ignore_index=True)
#     time.sleep(1)


# Guthaben aller Tokens

key = ""
sec = ""
layout_login = [
            [
                sg.Text("API KEY", background_color="#272533", text_color="white", size=(15,1)),
                sg.Input(key="-KEY-")
            ],
            [
                sg.Text("API SECURITY", background_color="#272533", text_color="white", size=(15,1)),
                sg.Input(key="-SEC-")
            ],
            [
                sg.Button("Login", button_color=("white", "green"), size=10),
                sg.Button("Abbrechen", button_color=("white", "darkred"), size=10)
            ]
        ]

window_login = sg.Window("Login", layout_login, background_color="#272533")

while True:
    event, values = window_login.read()
    key     = values["-KEY-"]
    sec     = values["-SEC-"]
    client  = Client(key, sec)
    if event == "Login" and key and sec:

        token       = ""
        headings    = ["Datum", "Token", "Status", "Menge", "Preis", "Gebühr"]
        now         = datetime.now()

        # Erstellen der Oberfläche
        sg.theme("BlueMono")

        main = [
            [
                sg.Button("Trades", size=(20, 3), button_color=("black", "darkorange")),
                sg.Button("Kauf-/Verkaufspreise berechnen", size=(20, 3), button_color=("black", "darkorange")),
                sg.Button("Paketpreise berechnen", size=(20, 3), button_color=("black", "darkorange")),
                sg.Button("Balance", size=(20, 3), button_color=("black", "darkorange"))
            ],
            [
                sg.Button("Bot starten", size=(87, 3), button_color=("black", "green"))
            ]
        ]

        window_login.close()
        window_main = sg.Window("Binance Data Analytics", main, background_color="#272533")

        while True:
            event, values = window_main.read()
            if event == "Trades":

                info = client.get_exchange_info()
                symbols = []

                for i in info["symbols"]:
                    sym = i["baseAsset"]
                    symbols.append(sym)

                layout = [
                    [
                        sg.Text("Token", size=(30, 1), background_color="#272533", text_color="white")
                    ],
                    [
                        sg.Combo(symbols, key="-TOKEN-")
                    ],
                    [
                        sg.Text("Zeitraum", size=(30, 1), background_color="#272533", text_color="white")
                    ],
                    [
                        sg.Input(size=(20, 1), key="-VON-"), sg.CalendarButton("Von", size=(10, 1)),
                        sg.Text("-", background_color="#272533", text_color="white"),
                        sg.Input(size=(20, 1), key="-BIS-"), sg.CalendarButton("Bis", size=(10, 1))
                    ],
                    [
                        sg.Button("Ok", button_color="darkgreen", size=(10)),
                        sg.Button("Schließen", button_color="darkred", size=(10))
                    ]
                ]

                window_trades = sg.Window("Übersicht der Trades", layout, background_color="#272533")

                while True:
                    event, values = window_trades.read()
                    if event == "Ok":

                        token   = values["-TOKEN-"] + "USDT"
                        von1    = values["-VON-"]
                        von     = von1[:von1.find(' ')]
                        bis1    = values["-BIS-"]
                        bis     = bis1[:bis1.find(' ')]

                        trades = client.get_my_trades(symbol=token)

                        data        = []
                        buy_trades  = []
                        sell_trades = []

                        for t in trades:

                            sides   = t["isBuyer"]
                            date    = int(t["time"])

                            if von and bis:

                                if datetime.fromtimestamp(date / 1000).strftime(
                                        '%Y-%m-%d') >= von and datetime.fromtimestamp(
                                        date / 1000).strftime('%Y-%m-%d') <= bis:

                                    time    = datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                    symbol  = t["symbol"]
                                    qty     = t["qty"]
                                    price   = t["quoteQty"]
                                    fee     = t["commission"]

                                    if sides:
                                        status      = "BUY"
                                        buy_data    = [time, symbol, status, qty, price, fee]
                                        buy_trades.append(buy_data)
                                    elif not sides:
                                        status      = "SELL"
                                        sell_data   = [time, symbol, status, qty, price, fee]
                                        sell_trades.append(sell_data)

                                    datensatz = [time, symbol, status, qty, price, fee]
                                    data.append(datensatz)

                            elif von and not bis:

                                if datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d') >= von:

                                    time    = datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                    symbol  = t["symbol"]
                                    qty     = t["qty"]
                                    price   = t["quoteQty"]
                                    fee     = t["commission"]

                                    if sides:
                                        status      = "BUY"
                                        buy_data    = [time, symbol, status, qty, price, fee]
                                        buy_trades.append(buy_data)
                                    elif not sides:
                                        status      = "SELL"
                                        sell_data   = [time, symbol, status, qty, price, fee]
                                        sell_trades.append(sell_data)

                                    datensatz = [time, symbol, status, qty, price, fee]
                                    data.append(datensatz)
                            elif bis and not von:

                                if datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d') <= bis:

                                    time    = datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                    symbol  = t["symbol"]
                                    qty     = t["qty"]
                                    price   = t["quoteQty"]
                                    fee     = t["commission"]

                                    if sides:
                                        status      = "BUY"
                                        buy_data    = [time, symbol, status, qty, price, fee]
                                        buy_trades.append(buy_data)
                                    elif not sides:
                                        status      = "SELL"
                                        sell_data   = [time, symbol, status, qty, price, fee]
                                        sell_trades.append(sell_data)

                                    datensatz = [time, symbol, status, qty, price, fee]
                                    data.append(datensatz)
                            else:

                                time    = datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d %H:%M:%S')
                                symbol  = t["symbol"]
                                qty     = t["qty"]
                                price   = t["quoteQty"]
                                fee     = t["commission"]

                                if sides:
                                    status      = "BUY"
                                    buy_data    = [time, symbol, status, qty, price, fee]
                                    buy_trades.append(buy_data)
                                elif not sides:
                                    status      = "SELL"
                                    sell_data   = [time, symbol, status, qty, price, fee]
                                    sell_trades.append(sell_data)

                                datensatz = [time, symbol, status, qty, price, fee]
                                data.append(datensatz)

                        all_trades_table = [

                            [
                                sg.Table(
                                    values=data,
                                    headings=headings,
                                    max_col_width=30,
                                    auto_size_columns=True,
                                    display_row_numbers=False,
                                    justification="left",
                                    num_rows=20,
                                    key="-TABLE-",
                                    row_height=30
                                )
                            ]
                        ]

                        buy_trades_table = [
                            [
                                sg.Table(
                                    values=buy_trades,
                                    headings=headings,
                                    max_col_width=30,
                                    auto_size_columns=True,
                                    display_row_numbers=False,
                                    justification="left",
                                    num_rows=20,
                                    key="-TABLE-",
                                    row_height=30
                                )
                            ]
                        ]

                        sell_trades_table = [
                            [
                                sg.Table(
                                    values=sell_trades,
                                    headings=headings,
                                    max_col_width=30,
                                    auto_size_columns=True,
                                    display_row_numbers=False,
                                    justification="left",
                                    num_rows=20,
                                    key="-TABLE-",
                                    row_height=30
                                )
                            ]
                        ]

                        tab_group = [
                            [
                                sg.TabGroup(
                                    [
                                        [
                                            sg.Tab("Alle Trades", all_trades_table)
                                        ],
                                        [
                                            sg.Tab("Kauf", buy_trades_table, background_color="green")
                                        ],
                                        [
                                            sg.Tab("Verkauft", sell_trades_table, background_color="red")
                                        ]
                                    ],
                                    tab_location="center"
                                )
                            ],
                            [
                                sg.Button(
                                    "Exit",
                                    button_color="red",
                                    size=(20)
                                ),
                                sg.Button(
                                    "Export to CSV",
                                    button_color=("white", "green"),
                                    size=20
                                )
                            ]
                        ]

                        table_window = sg.Window("Übersicht aller Trades", tab_group, modal=True)

                        while True:
                            event, values = table_window.read()
                            if event == "Export to CSV":
                                csv_file = open("Binance.csv")
                                csv_writer = csv.writer(csv_file)
                            if event == "Exit" or event == sg.WIN_CLOSED:
                                break
                        table_window.close()

                    if event == "Schließen" or event == sg.WIN_CLOSED:
                        break
                window_trades.close()
            if event == "Kauf-/Verkaufspreise berechnen":
                ##-----DEFAULT SETTINGS----------------------------------##
                bw: dict = {'size': (7, 2), 'font': ('Franklin Gothic Book', 24), 'button_color': ("black", "#F8F8F8")}
                bt: dict = {'size': (7, 2), 'font': ('Franklin Gothic Book', 24), 'button_color': ("black", "#F1EABC")}
                bo: dict = {'size': (15, 2), 'font': ('Franklin Gothic Book', 24), 'button_color': ("black", "#ECA527"),
                            'focus': True}

                ##-----WINDOW AND LAYOUT---------------------------------##
                layout: list = [
                    [sg.Text('Preisrechner', size=(50, 1), justification='right', background_color="#272533",
                             text_color='white', font=('Franklin Gothic Book', 14, 'bold'))],
                    [sg.Text('0.0000', size=(18, 1), justification='right', background_color='black', text_color='red',
                             font=('Digital-7', 48), relief='sunken', key="_DISPLAY_")],
                    [sg.Button('C', **bt), sg.Button('CE', **bt), sg.Button('%', **bt), sg.Button("/", **bt)],
                    [sg.Button('7', **bw), sg.Button('8', **bw), sg.Button('9', **bw), sg.Button("*", **bt)],
                    [sg.Button('4', **bw), sg.Button('5', **bw), sg.Button('6', **bw), sg.Button("-", **bt)],
                    [sg.Button('1', **bw), sg.Button('2', **bw), sg.Button('3', **bw), sg.Button("+", **bt)],
                    [sg.Button('0', **bw), sg.Button('.', **bw), sg.Button('=', **bo, bind_return_key=True)]
                ]

                window: object = sg.Window('Preisrechner', layout=layout, background_color="#272533", size=(580, 660),
                                           return_keyboard_events=True)

                ##----CALCULATOR FUNCTIONS-------------------------------##
                var: dict = {'front': [], 'back': [], 'decimal': False, 'x_val': 0.0, 'y_val': 0.0, 'result': 0.0,
                             'operator': ''}


                # -----HELPER FUNCTIONS
                def format_number() -> float:
                    ''' Create a consolidated string of numbers from front and back lists '''
                    return float(''.join(var['front']).replace(',', '') + '.' + ''.join(var['back']))


                def update_display(display_value: str):
                    ''' Update the calculator display after an event click '''
                    try:
                        window['_DISPLAY_'].update(value='{:,.4f}'.format(display_value))
                    except:
                        window['_DISPLAY_'].update(value=display_value)


                # -----CLICK EVENTS
                def number_click(event: str):
                    ''' Number button button click event '''
                    global var
                    if var['decimal']:
                        var['back'].append(event)
                    else:
                        var['front'].append(event)
                    update_display(format_number())


                def clear_click():
                    ''' CE or C button click event '''
                    global var
                    var['front'].clear()
                    var['back'].clear()
                    var['decimal'] = False


                def operator_click(event: str):
                    ''' + - / * button click event '''
                    global var
                    var['operator'] = event
                    try:
                        var['x_val'] = format_number()
                    except:
                        var['x_val'] = var['result']
                    clear_click()


                def calculate_click():
                    ''' Equals button click event '''
                    global var
                    try:
                        var['y_val'] = format_number()
                    except ValueError:  # When Equals is pressed without any input
                        var['x_val'] = var['result']
                    try:
                        var['result'] = eval(str(var['x_val']) + var['operator'] + str(var['y_val']))
                        update_display(var['result'])
                        clear_click()
                    except:
                        update_display("ERROR! DIV/0")
                        clear_click()


                # -----MAIN EVENT LOOP------------------------------------##
                while True:
                    event, values = window.read()
                    print(event)
                    if event is None:
                        break
                    if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        number_click(event)
                    if event in ['Escape:27', 'C', 'CE']:  # 'Escape:27 for keyboard control
                        clear_click()
                        update_display(0.0)
                        var['result'] = 0.0
                    if event in ['+', '-', '*', '/']:
                        operator_click(event)
                    if event == '=':
                        calculate_click()
                    if event == '.':
                        var['decimal'] = True
                    if event == '%':
                        update_display(var['result'] / 100.0)


            if event == "Paketpreise berechnen":

                info    = client.get_exchange_info()
                symbols = []

                for i in info["symbols"]:
                    sym = i["baseAsset"]
                    symbols.append(sym)

                packages_layout = [

                    [
                        sg.Text("Token", size=40, background_color="#272533", text_color="white"),
                        sg.Combo(symbols, key="-TOKEN_LIVE-")
                    ],
                    [
                        sg.Text("Einsatz in €", size=40, background_color="#272533", text_color="white"),
                        sg.Input(key="-EINSATZ-", size=10)
                    ],
                    [
                        sg.Text("Anzahl Pakete zum Sofortkauf", size=40, background_color="#272533", text_color="white"),
                        sg.Input(key="-ENTER_PRICE-", size=10)
                    ],
                    [
                        sg.Text("Preissprünge in %", size=40, background_color="#272533", text_color="white"),
                        sg.Input(key="-PRICE_PERCENT-", size=10)
                    ],
                    [
                        sg.Text("Paketgröße in €", size=40, background_color="#272533", text_color="white"),
                        sg.Input(key="-PACKAGE_SIZE-", size=10)
                    ],
                    [
                        sg.Text("Risikoabsicherung in %", size=40, background_color="#272533", text_color="white"),
                        sg.Input(key="-RISK-", size=10)
                    ],
                    [
                        sg.Button("Berechnen", button_color=("white", "green"), size=50)
                    ],
                    [
                        sg.Button("Abbrechen", button_color=("white", "darkred"), size=50)
                    ]

                ]

                window_pakete = sg.Window("Paketberechnung", packages_layout, background_color="#272533")

                while True:
                    event, values = window_pakete.read()

                    symbol_live     = values["-TOKEN_LIVE-"] + "USDT"
                    einsatz         = int(values["-EINSATZ-"])
                    price_percent   = int(values["-PRICE_PERCENT-"])
                    package_size    = int(values["-PACKAGE_SIZE-"])
                    enter_price     = int(values["-ENTER_PRICE-"])

                    ticketSize = client.get_exchange_info()
                    for l in ticketSize["symbols"]:
                        if l["symbol"] == symbol_live:
                            for a in l["filters"]:
                                if a["filterType"] == "PRICE_FILTER":
                                    price_size = a["tickSize"]


                    tickerSize = client.get_exchange_info()
                    for p in tickerSize["symbols"]:
                        if p["symbol"] == symbol_live:
                            for ba in p["filters"]:
                                if ba["filterType"] == "LOT_SIZE":
                                    step_size = ba["stepSize"]


                    if values["-RISK-"]:
                        risk            = int(values["-RISK-"])
                    else:
                        risk = False

                    if event == "Berechnen":

                        if package_size < 10:
                            sg.Popup("Paketwert liegt unter dem Minimum")
                        else:
                            headings_pakete = ["Token", "Status", "Preis", "Menge", "Paketpreis"]
                            headings_sell_pakete = ["Token", "Status", "Preis", "Menge", "Erlös"]
                            package_data_all = []
                            sell_package_data = []

                            client = Client(key, sec)
                            live_price = float(client.get_symbol_ticker(symbol=symbol_live)["price"])

                            einsatz_rest = einsatz - (enter_price * package_size)

                            if risk:
                                possible_amount_packages = risk / price_percent
                            else:
                                possible_amount_packages = einsatz_rest / package_size

                            for p in range(1, (int(possible_amount_packages) + 1)):
                                multiplikator = p
                                buy_price_package = round_step_size(live_price * ((1 - (price_percent / 100)) ** multiplikator), price_size)
                                if risk:
                                    buy_price = round_step_size(einsatz_rest / possible_amount_packages, price_size)
                                    token_amount = round_step_size(buy_price / buy_price_package, step_size)
                                else:
                                    token_amount = round_step_size(package_size / buy_price_package, step_size)
                                    buy_price = round_step_size(token_amount * buy_price_package, price_size)
                                status = ""
                                if buy_price_package < live_price:
                                    status = "BUY"
                                package_data = [symbol_live, status, buy_price_package, token_amount, buy_price]
                                package_data_all.append(package_data)

                            amount_token_available = (enter_price * package_size) / live_price
                            amount_token_per_sell = round_step_size(amount_token_available / enter_price, step_size)

                            for s in range(1, int(enter_price) + 1):
                                sell_multiplikator = s
                                sell_price_package = round_step_size(live_price / ((1 - (price_percent / 100)) ** sell_multiplikator), price_size)
                                sell_price_win = round_step_size(amount_token_per_sell * sell_price_package, price_size)
                                if sell_price_package > live_price:
                                    status = "SELL"
                                sell_data = [symbol_live, status, sell_price_package, amount_token_per_sell,
                                             sell_price_win]
                                sell_package_data.append(sell_data)

                            layout_buy_package_table = [

                                [
                                    sg.Table(
                                        values=package_data_all,
                                        headings=headings_pakete,
                                        max_col_width=35,
                                        auto_size_columns=True,
                                        display_row_numbers=True,
                                        justification="left",
                                        num_rows=15,
                                        key="-TABLE_BUY_PACKAGES-",
                                        row_height=30,
                                        background_color="#272533",
                                        text_color="white",
                                        enable_events=True
                                    ),
                                    sg.Text("Preis", size=10, background_color="#272533", text_color="white",
                                            pad=(20)),
                                    sg.Input(size=15, key="-INDIVIDUAL_BUY_PRICE-", enable_events=True),
                                    sg.Button("Paket erstellen", button_color=("black", "darkorange"), size=(12, 1), key="-BUTTON_BUY_PACKAGE-")
                                ]
                            ]
                            layout_sell_package_table = [

                                [
                                    sg.Table(
                                        values=sell_package_data,
                                        headings=headings_sell_pakete,
                                        max_col_width=35,
                                        auto_size_columns=True,
                                        display_row_numbers=True,
                                        justification="left",
                                        num_rows=15,
                                        key="-TABLE_SELL_PACKAGES-",
                                        row_height=30,
                                        background_color="#272533",
                                        text_color="white",
                                        enable_events=True
                                    ),
                                    sg.Text("Preis", size=10, background_color="#272533", text_color="white",
                                            pad=(20)),
                                    sg.Input(size=15, key="-INDIVIDUAL_SELL_PRICE-", enable_events=True),
                                    sg.Button("Paket erstellen", button_color=("black", "darkorange"), size=(12, 1))
                                ]

                            ]

                            tab_group_packages = [
                                [
                                    sg.TabGroup(
                                        [
                                            [
                                                sg.Tab("Pakete - Kauforder", layout_buy_package_table,
                                                       background_color="#272533")
                                            ],
                                            [
                                                sg.Tab("Pakete Verkauforder", layout_sell_package_table,
                                                       background_color="#272533")
                                            ]

                                        ],
                                        enable_events=True
                                    )
                                ],
                                [
                                    sg.Button("Alle erstellen", button_color=("white", "green"), size=(20, 2)),
                                    sg.Button("Abbrechen", button_color=("white", "darkred"), size=(20, 2))
                                ]
                            ]

                            window_package_table = sg.Window("Paketübersicht", tab_group_packages, background_color="#272533")
                            while True:
                                event, values = window_package_table.read()
                                if event == "-TABLE_BUY_PACKAGES-":
                                    row = values["-TABLE_BUY_PACKAGES-"][0]
                                    row_data = package_data_all[row]
                                    row_price = float(str(row_data[2]))
                                    row_qty = float(str(row_data[3]))
                                    window_package_table.Element("-INDIVIDUAL_BUY_PRICE-").update(row_price)
                                if event == "-TABLE_SELL_PACKAGES-":
                                    row = values["-TABLE_SELL_PACKAGES-"][0]
                                    row_data = sell_package_data[row]
                                    row_price = str(row_data[2])
                                    window_package_table.Element("-INDIVIDUAL_SELL_PRICE-").update(row_price)
                                if event == "-BUTTON_BUY_PACKAGE-":
                                    buy = client.order_limit_buy(
                                        symbol=symbol_live,
                                        quantity=row_qty,
                                        price=row_price
                                    )
                                if event == "Alle erstellen":
                                    for pack in package_data_all:
                                        print(pack[2])
                                        buy = client.order_limit_buy(
                                            symbol=symbol_live,
                                            quantity=pack[3],
                                            price=pack[2]
                                        )
                                if event == "Abbrechen" or event == sg.WIN_CLOSED:
                                    break
                            window_package_table.close()
                    if event == "Abbrechen":
                        break
                window_pakete.close()

            if event == "Bot starten":
                os.system("binance_bot.py")
                break


        if event == sg.WIN_CLOSED:
            window_main.close()

    elif event == "Login" and not key and not sec:
        sg.Popup("Bitte Logindaten eingeben", background_color="#272533")

    elif event == "Abbrechen" or event == sg.WIN_CLOSED:
        window_login.close()