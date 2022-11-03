from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import turtle as t
import time as ti
import json

class Circle:
    def __init__(self):
    # Opening JSON file
        f = open('figure.json')
    # returns JSON object as
    # a dictionary
        data = json.load(f)
    # Iterating through the json
    # list
        save = data["figures"]
        circle_x = save[1]['x']
        circle_y = save[1]['y']
        circle_r = save[1]['r']
        figure, axes = plt.subplots()
        Drawing_colored_circle = plt.Circle(( circle_x, circle_y ), circle_r , fill = False)
        axes.set_xlim((0, 50))
        axes.set_ylim((0, 50))
        axes.add_artist( Drawing_colored_circle )
        plt.grid()
        # plt.show() 