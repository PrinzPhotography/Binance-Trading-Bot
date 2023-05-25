import PySimpleGUI as sg
import main
from datetime import datetime


def create(headings):
    trades_nuls = main.client.get_my_trades(symbol=main.token)

    data = []
    for t in trades_nuls:

        sides = t["isBuyer"]

        if sides:
            status = "BUY"
        elif not sides:
            status = "SELL"

        date = int(t["time"])
        time = datetime.fromtimestamp(date / 1000).strftime('%Y-%m-%d %H:%M:%S')

        symbol = t["symbol"]
        qty = t["qty"]
        price = t["quoteQty"]
        fee = t["commission"]

        datensatz = [time, symbol, status, qty, price, fee]
        data.append(datensatz)

    token_table = [
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

    table_window = sg.Window("Übersicht aller Trades", token_table, modal=True)

    while True:
        event, values = table_window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    table_window.close()
