# -*- coding: utf-8 -*-
# @Time     : 2018/11/14 21:48
# @Author   : Run 
# @File     : coordinates.py
# @Software : PyCharm


import json
import os


CITY_COORDS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))


def load_city_cp():
    """
    Load the city center point coordinate dataset into the dictionary.
    :return:
    """
    with open(os.path.join(CITY_COORDS_FILE_PATH, 'city_center_point_coordinates.json'), encoding="utf8") as file:
        return json.load(file)


def load_city_polygon():
    """
    Load the city polygon coordinate dataset into the dictionary.
    :return:
    """
    with open(os.path.join(CITY_COORDS_FILE_PATH, 'city_polygon_coords.json'), encoding="utf8") as file:
        return json.load(file)
