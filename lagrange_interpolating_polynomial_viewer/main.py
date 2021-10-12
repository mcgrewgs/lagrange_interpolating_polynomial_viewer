#!/usr/bin/env pipenv run python

from typing import Any, Dict, List, Union
from functools import reduce
import PySimpleGUI as sg  # type: ignore
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore
from matplotlib.figure import Figure  # type: ignore
import matplotlib as mpl  # type: ignore

mpl.use("TkAgg")


def draw_figure(canvas: sg.Canvas, figure: Figure) -> FigureCanvasTkAgg:
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def lagrange_interpolating_polynomial(
    xList: List[float], yList: List[float], xVal: float
) -> float:
    assert len(xList) == len(yList)
    return sum(
        [
            yList[i]
            * reduce(
                lambda curr, nxt: curr * nxt,
                [
                    ((xVal - xList[j]) / (xList[i] - xList[j]))
                    for j in range(len(xList))
                    if j != i
                ],
                1.0,
            )
            for i in range(len(xList))
        ]
    )


default_window_settings: Dict[str, Any] = {
    "resizable": True,
    "auto_size_buttons": True,
    "auto_size_text": True,
}

default_canvas_key = "-CANVAS-"

layout: List[List[Union[sg.Text, sg.Button, sg.Canvas]]] = [
    [sg.Text("Plot test")],
    [sg.Canvas(key=default_canvas_key)],
    [sg.Button("OK")],
]

window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
    **default_window_settings,
)

figWidth = 5
defaultDpi = 128
fig = Figure(figsize=(figWidth, 4), dpi=defaultDpi)
x = sorted([2.0 * i for i in range(5)] + [-2.0 * i for i in range(1, 5)])
# y = [i * i for i in x]
y = [np.random.random() * 1000.0 for _ in x]

windowExtraWidth = 0.1
tMin = min(x) - windowExtraWidth
tMax = max(x) + windowExtraWidth

t = np.linspace(tMin, tMax, 2 * figWidth * defaultDpi)
p = [lagrange_interpolating_polynomial(x, y, tVal) for tVal in t]

subplot = fig.add_subplot(1, 1, 1)
subplot.plot(t, p, "b")
subplot.plot(x, y, "go")

draw_figure(window[default_canvas_key].TKCanvas, fig)

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
