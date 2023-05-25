import PySimpleGUI
import PySimpleGUI as sg
import main

sg.theme("DarkAmber")

layout = [
    [
        sg.Text("Token", size=(30, 1))
    ],
    [
        sg.Combo(main.symbols, key="-TOKEN-")
    ],
    [
        sg.Text("Zeitraum", size=(30, 1))
    ],
    [
        sg.Input(size=(20, 1)), sg.CalendarButton("Von", key="-VON-", size=(10, 1)),
        sg.Text("-"),
        sg.Input(size=(20, 1)), sg.CalendarButton("Bis", key="-BIS-", size=(10, 1))
    ],
    [
        sg.Button("Ok"),
        sg.Button("Schließen")
    ]
]

window = sg.Window("Binance Data Analytics", layout)

while True:
    event, values = window.read()
    if event == "Ok":
        main.token = values["-TOKEN-"]
        table.create(main.headings)
    if event == "Schließen" or event == sg.WIN_CLOSED:
        break

window.close()
