#!/usr/bin/env pipenv run python

from typing import Any, Dict, List, Union
import PySimpleGUI as sg

default_window_settings: Dict[str, Any] = {"resizable": True}

layout: List[List[Union[sg.Text, sg.Button]]] = [[sg.Text("Hello")], [sg.Button("OK")]]

window = sg.Window("Demo", layout, **default_window_settings)

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
