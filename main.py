import json
import math
from math import sin, cos
from abc import abstractmethod
from typing import List
import PySimpleGUI as Sg
from enum import Enum


class Color(Enum):
    POINT_COLOR = "red"
    LINE_COLOR = "green"
    RECTANGLE_COLOR = "blue"
    CIRCLE_COLOR = "brown"


def rotate(x: float, y: float, a: float):
    new_x = x * cos(a) + y * sin(a)
    new_y = -x * sin(a) + y * cos(a)
    return new_x, new_y


class Shape:

    @abstractmethod
    def transfigure(self, dx: float, dy: float):
        pass

    @abstractmethod
    def rotate(self, a: float):
        pass

    @abstractmethod
    def show(self, graph: Sg.Graph):
        pass

    @abstractmethod
    def to_json(self):
        pass


class Point(Shape):
    x: float
    y: float

    def __init__(self, object):
        self.x = object["x"]
        self.y = object["y"]

    def transfigure(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def rotate(self, a: float):
        self.x, self.y = rotate(self.x, self.y, a)

    def show(self, graph: Sg.Graph):
        graph.draw_point((self.x, self.y), size=6, color=Color.POINT_COLOR.value)

    def to_json(self):
        return {
            "type": "point",
            "x": self.x,
            "y": self.y
        }


class Line(Shape):
    x1: float
    x2: float
    y1: float
    y2: float

    def __init__(self, object):
        self.x1 = object["x1"]
        self.x2 = object["x2"]
        self.y1 = object["y1"]
        self.y2 = object["y2"]

    def transfigure(self, dx: float, dy: float):
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

    def rotate(self, a: float):
        self.x1, self.y1 = rotate(self.x1, self.y1, a)
        self.x2, self.y2 = rotate(self.x2, self.y2, a)

    def show(self, graph: Sg.Graph):
        pf = (self.x1, self.y1)
        pt = (self.x2, self.y2)
        graph.draw_line(pf, pt, color=Color.LINE_COLOR.value)

    def to_json(self):
        return {
            "type": "line",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2
        }


class Rectangle(Shape):
    x1: float
    x2: float
    x3: float
    x4: float
    y1: float
    y2: float
    y3: float
    y4: float

    def __init__(self, object):
        self.x1 = object["x1"]
        self.x2 = object["x2"]
        self.x3 = object["x3"]
        self.x4 = object["x4"]
        self.y1 = object["y1"]
        self.y2 = object["y2"]
        self.y3 = object["y3"]
        self.y4 = object["y4"]

    def transfigure(self, dx: float, dy: float):
        self.x1 += dx
        self.x2 += dx
        self.x3 += dx
        self.x4 += dx
        self.y1 += dy
        self.y2 += dy
        self.y3 += dy
        self.y4 += dy

    def rotate(self, a: float):
        self.x1, self.y1 = rotate(self.x1, self.y1, a)
        self.x2, self.y2 = rotate(self.x2, self.y2, a)
        self.x3, self.y3 = rotate(self.x3, self.y3, a)
        self.x4, self.y4 = rotate(self.x4, self.y4, a)

    def show(self, graph: Sg.Graph):

        graph.draw_line((self.x1, self.y1), (self.x2, self.y2), color=Color.RECTANGLE_COLOR.value)
        graph.draw_line((self.x3, self.y3), (self.x2, self.y2), color=Color.RECTANGLE_COLOR.value)
        graph.draw_line((self.x3, self.y3), (self.x4, self.y4), color=Color.RECTANGLE_COLOR.value)
        graph.draw_line((self.x1, self.y1), (self.x4, self.y4), color=Color.RECTANGLE_COLOR.value)

    def to_json(self):
        return {
            "type": "rectangle",
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x1,
            "y2": self.y2,
            "x3": self.x2,
            "y3": self.y2,
            "x4": self.x2,
            "y4": self.y1
        }


class Circle(Shape):
    x: float
    y: float
    r: float

    def __init__(self, object):
        self.x = object["x"]
        self.y = object["y"]
        self.r = object["r"]

    def transfigure(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def rotate(self, a: float):
        self.x, self.y = rotate(self.x, self.y, a)

    def show(self, graph: Sg.Graph):
        graph.draw_circle((self.x, self.y), self.r, line_color=Color.CIRCLE_COLOR.value)

    def to_json(self):
        return {
            "type": "circle",
            "x": self.x,
            "y": self.y,
            "r": self.r,
        }


class Composite(Shape):
    figures: List[Shape]

    def __init__(self, object):
        self.figures = []
        for figure in object["figures"]:
            self.insert(figure)

    def transfigure(self, dx: float, dy: float):
        for shape in self.figures:
            shape.transfigure(dx, dy)

    def rotate(self, a: float):
        for shape in self.figures:
            shape.rotate(a)

    def insert(self, object):
        type = {
            "point": Point,
            "line": Line,
            "rectangle": Rectangle,
            "circle": Circle,
            "composite": Composite
        }
        try:
            self.figures.append(type[object["type"]](object))
        except KeyError:
            print(object["type"], "is invalid!")

    def show(self, graph: Sg.Graph):
        for figure in self.figures:
            figure.show(graph)

    def to_json(self):
        return {
            "type": "composite",
            "figures": [figure.to_json() for figure in self.figures]
        }


def reset_graph(graph: Sg.Graph):
    graph.erase()
    w, h = graph.CanvasSize
    graph.draw_text(0, (-10, -13), color='black')
    graph.draw_text(-w, (-w + 20, -13), color='black')
    graph.draw_text(w, (w - 20, -13), color='black')
    graph.draw_text(-h, (-27, -h + 13), color='black')
    graph.draw_text(h, (-20, h - 13), color='black')
    for i in range(-w, w, 15):
        graph.draw_line((i, 0), (i + 5, 0), color='black')
    for i in range(-h, h, 15):
        graph.draw_line((0, i), (0, i + 5), color='black')


def create_window(title, width, height):
    layout = [
        [Sg.Graph(canvas_size=(width, height), graph_bottom_left=(-width, -height),
                  graph_top_right=(width, height), background_color='white', enable_events=True, key='graph')],
        [Sg.Text('Announcement: '), Sg.Text(key='announcement')],
        [Sg.Text('Add new composite (json): '), Sg.Multiline(size=(60, 4)), Sg.Button('Insert')],
        [Sg.Text('Transfigure composite, '), Sg.Text('dx ='), Sg.InputText(size=(15, 1)),
         Sg.Text('dy ='), Sg.InputText(size=(15, 1)), Sg.Button('Transfigure')],
        [Sg.Text('Rotate composite: '), Sg.Text('a ='), Sg.InputText(size=(15, 1)),
         Sg.Text('(degree)'), Sg.Button('Rotate')],
        [Sg.Button(key='Load', button_text='Load composite'),
         Sg.Button(key='Save', button_text='Save composite')]
    ]

    window = Sg.Window(title, layout, finalize=True)

    return window


def main():
    f = open('figure.json')
    figure_file = open('figure.json')
    obj = json.load(figure_file)
    composite = Composite(obj)
    f.close()

    window = create_window("Tran Quang Dao 20200128", 200, 200)

    graph = window['graph']

    reset_graph(graph)
    composite.show(graph)

    while True:
        event, values = window.read()
        if event == 'Insert':
            try:
                composite.insert(json.loads(values[0]))
            except Exception:
                window['announcement'].update('Invalid composite!')
        elif event == 'Transfigure':
            try:
                composite.transfigure(float(values[1]), float(values[2]))
            except Exception:
                window['announcement'].update('Type of dx and dy must be float or integer!')
        elif event == 'Rotate':
            try:
                composite.rotate(float(values[3]) / 360 * math.pi)
            except Exception:
                window['announcement'].update('Type of a must be float or integer!')
        elif event == 'Load':
            try:
                f = open('figure.json')
                figure_file = open('figure.json')
                obj = json.load(figure_file)
                composite = Composite(obj)
                f.close()
            except Exception:
                window['announcement'].update('Can\'t load the composite!')
        elif event == 'Save':
            try:
                f = open('saved_figure.json', 'w')
                f.write(json.dumps(composite.to_json()))
                f.close()
                window['announcement'].update('Save successfully composite in file: saved_figure.json')
            except Exception:
                window['announcement'].update('Can\'t save the composite!')
        elif event == Sg.WIN_CLOSED:
            break
        if event in ['Insert', 'Transfigure', 'Rotate', 'Load']:
            reset_graph(graph)
            composite.show(graph)
    window.close()


main()
