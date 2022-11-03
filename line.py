from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import turtle as t
import time as ti
import json


class Line:
    def __init__(self):
    # Opening JSON file
        f = open('figure.json')
    # returns JSON object as
    # a dictionary
        data = json.load(f)
    # Iterating through the json
    # list
        save = data["figures"]
        line_x1 = save[2]['x1']
        line_y1 = save[2]['y1']
        line_x2 = save[2]['x2']
        line_y2 = save[2]['y2']
        
        x = np.array([line_x1,line_x2])
        y = np.array([line_y1,line_y2])

        plt.plot(x, y)

        # plt.show()