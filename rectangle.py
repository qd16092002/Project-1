from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import turtle as t
import time as ti
import json


class Rectangle:
    def __init__(self):
    # Opening JSON file
        f = open('figure.json')
    # returns JSON object as
    # a dictionary
        data = json.load(f)
    # Iterating through the json
    # list
        save = data["figures"]
        rectangle_x1 = save[3]['x1']
        rectangle_y1 = save[3]['y1']
        rectangle_x2 = save[3]['x2']
        rectangle_y2 = save[3]['y2']
        rectangle_x3 = save[3]['x3']
        rectangle_y3 = save[3]['y3']
        rectangle_x4 = save[3]['x4']
        rectangle_y4 = save[3]['y4']
        
        x = np.array([rectangle_x1,rectangle_x2,rectangle_x3,rectangle_x4,rectangle_x1])
        y = np.array([rectangle_y1,rectangle_y2,rectangle_y3,rectangle_y4,rectangle_y1])
        
        plt.plot(x, y,ms = 20)

        