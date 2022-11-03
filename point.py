from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import turtle as t
import time as ti
import json


class Point:
    def __init__(self):      

        f = open('figure.json')

        data = json.load(f)

        save = data["figures"]
        point_x = save[0]['x']
        point_y = save[0]['y']

        plt.plot(point_x,point_y, marker = 'o', ms = 10, mec = 'r', mfc = 'r')
        
        # plt.show()    