# -*- coding: utf-8 -*-
# @Time     : 2018/11/14 21:48
# @Author   : Run 
# @File     : coordinates.py
# @Software : PyCharm


import json
import os


CITY_POLYGON_COORDS_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '\\city_polygon_coords.json'

with open(CITY_POLYGON_COORDS_FILE_PATH, encoding="utf8") as file:
    geoJson = json.load(file)  # 各省的县市及直辖市的行政区的geoJson格式数据