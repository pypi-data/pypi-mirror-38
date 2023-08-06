# -*- coding: utf-8 -*-
# @Time     : 2018/11/14 16:35
# @Author   : Run 
# @File     : color_map.py
# @Software : PyCharm


from pyecharts.chart import Chart
from pyecharts_plus.datasets.coordinates import geoJson
from pyecharts.datasets.coordinates import _load_coordinates
import re
from pyecharts import utils


class ColorMap(Chart):
    """
    <<< 城市色彩图 >>>
    省细化到县市，直辖市细化到行政区，根据数值或分组为其着色。并支持根据名称自动匹配坐标添加标记点及label。
    """

    def __init__(self, title="", subtitle="", **kwargs):
        """

        :param title:
        :param subtitle:
        :param kwargs:
        """

        self.style = {
            'title_pos': 'center',
            'title_top': '#fff',
            # 'background_color': '#404a59',
            'width': '100%',
            'height': 600
        }
        for key in kwargs:
            value = kwargs.get(key)
            if value is not None:
                self.style[key] = value
        super(ColorMap, self).__init__(title, subtitle, **self.style)

        # toolbox
        self._option["toolbox"] = {
            "show": True,
            "orient": "vertical",
            "left": "95%",
            "top": "top",
            "feature": {
                "saveAsImage": {
                    "show": True,
                    "title": "\u4e0b\u8f7d\u56fe\u7247"
                }
            }
        }

        # legend
        self._option["legend"] = {
            "orient": 'vertical',
            "left": 'left',
            "top": "center",
            "data":[]
        }

        # init series
        self._option["series"] = []

        self.geoJson = geoJson  # 各省的县市及直辖市的行政区的geoJson格式数据
        self.valid_city_set = set([x['properties']['name'] for x in geoJson['features']])
        # self.invalid_cities = None
        self.valid_city_dict_from_pyecharts = _load_coordinates()

    def add_map(self,
                data_df,
                city_col=0, value_col=None, group_col=None,
                ):
        """
        todo 暂未找到在tooltip中展示更多维度扩展信息的方法
        :param data_df:
        :param city_col:
        :param value_col: 如果不为None，则以该列数值添加连续的visualMap，并在tooltip中进行展示。 todo
        :param group_col: 如果不为None，则以该列分组添加离散的visualMap，并在visualMap中展示每个分组的名字
        :return:
        """
        # check params
        if value_col is None and group_col is None:
            raise Exception("please choose value_col or group_col")

        # 数据去重
        data_df = data_df.drop_duplicates().reset_index(drop=True)

        # 调整数据列顺序
        col_list = [city_col, value_col or group_col]
        data_df = data_df.iloc[:, col_list]

        # filter invalid cities
        temp = list(set(data_df.iloc[:, 0].tolist()) - self.valid_city_set)
        if len(temp) > 0:
            print("[add_map]无效的城市或区域名称有:", temp)
        data_df = data_df[data_df.iloc[:, 0].isin(self.valid_city_set)]

        if value_col is not None:  # todo
            pass
        else:
            group_list = data_df.iloc[:, 1].unique().tolist()
            group_num = len(group_list)
            group_dict = dict(zip(group_list, range(group_num)))
            # visualMap
            pieces = [{'min': i, 'max': i, 'label': name} for i, name in enumerate(group_list)]
            self._option['visualMap'] = [
                {
                    'show': True,
                    'showLabel': True,
                    'left': 'right',
                    'top': 'center',
                    'seriesIndex': [len(self._option['series'])],
                    'type': 'piecewise',
                    'min': 0,
                    'max': group_num - 1,
                    'pieces': pieces,
                    'calculable': True,
                    'inRange': {
                        # 'color': ['#3B5077', '#031525']  # 蓝黑
                        # 'color': ['#ffc0cb', '#800080']  # 红紫
                        # 'color': ['#3C3B3F', '#605C3C']  # 黑绿
                        # 'color': ['#0f0c29', '#302b63', '#24243e']  # 黑紫黑
                        # 'color': ['#23074d', '#cc5333']  # 紫红
                        'color': ['lightskyblue', 'yellow', 'orangered']  # 蓝红
                        # 'color': ['#00467F', '#A5CC82']  # 蓝绿
                        # 'color': ['white', '#1488CC', '#2B32B2']  # 浅蓝
                        # 'color': ['#00467F', '#A5CC82']  # 蓝绿
                        # 'color': ['#00467F', '#A5CC82']  # 蓝绿
                        # 'color': ['#00467F', '#A5CC82']  # 蓝绿
                        # 'color': ['#00467F', '#A5CC82']  # 蓝绿
                    }
                }
            ]
            # series
            data_df.iloc[:, 1] = data_df.iloc[:, 1].apply(group_dict.get)
            data = [{'name': data_df.iloc[i, 0], 'value': int(data_df.iloc[i, 1])} for i in range(len(data_df))]
            self._option['series'].append(
                {
                    'type': 'map',
                    'mapType': 'chinacity',
                    'roam': True,
                    'label': {
                        'normal': {
                            'show': False
                        },
                        'emphasis': {
                            'show': True
                        }
                    },
                    'data': data,
                    "showLegendSymbol": False
                }
            )

    def add_pin(self, name, data, is_symbol_display=False, is_label_display=True):
        """
        scatter似乎不支持自定义地图，所以通过markPoint的方式添加一些标记点
        :param name: legend中显示的名称
        :param data: [{ "name": name, "coords": [lgt, lat]}, ...}
        :param is_symbol_display: 是否显示图标
        :param is_label_display: 是否显示label
        :return:
        """
        self._option["legend"]["data"].append(name)
        temp = {
            "name": name,
            "type": "map",
            "mapType": "chinacity",
            "roam": True,
            'label': {
                'normal': {
                    'show': False
                },
                'emphasis': {
                    'show': True
                }
            },
            "markPoint": {
                "symbolSize": 30,
                "data": data
            }
        }
        # symbol
        if not is_symbol_display:
            temp["markPoint"]["itemStyle"] = {
                "color": "rgb(0, 0, 0, 0)"
            }
        # label
        if is_label_display:
            temp["markPoint"]["label"] = {
                "normal": {
                    "show": True,
                    "formatter": "{b}",
                    "color": "rgb(0, 0, 0)",
                    "fontWeight": "bold",
                    "fontSize": 20
                }
            }
        #
        self._option["series"].append(temp)

    def add_city_pin(self, name, city_list, is_symbol_display=False, is_label_display=True):
        """
        传入一列城市名，自动匹配坐标，以markPoint的形式在地图上进行展现
        :param name: 在legend中显示的名称
        :param city_list:
        :param is_symbol_display: 是否显示图标
        :param is_label_display: 是否显示label
        :return:
        """
        # filter invalid cities
        temp = list(set(city_list) - set(self.valid_city_dict_from_pyecharts))
        if len(temp) > 0:
            print("[add_city_pin]无效的城市或区域名称有:", temp)
        #
        data = []
        for city in city_list:
            if city in self.valid_city_dict_from_pyecharts:
                data.append(
                    {
                        "name": city,
                        "coord": self.valid_city_dict_from_pyecharts[city]
                    }
                )
        #
        self.add_pin(name, data, is_symbol_display, is_label_display)

    def render(self, path="render.html", template_name="simple_chart.html", object_name="chart", **kwargs):
        """
        重写了父类的该函数
        :param path:
        :param template_name:
        :param object_name:
        :param kwargs:
        :return:
        """
        super(ColorMap, self).render(path, "simple_chart.html", "chart", **kwargs)
        with open(path, 'r', encoding="utf-8") as file:
            cont = file.read()

        # 导入自定义地图的geoJson，并注册该地图
        pos1 = re.search("<body>\n\s*<div id=", cont).span()[0] + 7
        cont = cont[: pos1] + """<script type="text/javascript">\n    var geoJson = {0};\n""".format(self.geoJson) + \
                              """    echarts.registerMap('chinacity', geoJson);\n</script>\n""" + cont[pos1:]

        # 使图表全屏显示
        try:
            pos2 = re.search("<html>", cont).span()[1] - 1
            cont = cont[: pos2] + ' style="height: 100%"' + cont[pos2:]
            pos2 = re.search("<body>", cont).span()[1] - 1
            cont = cont[: pos2] + ' style="height: 100%; margin: 0"' + cont[pos2:]
            pos3, pos4 = re.search('style="width:.*?;height:.*?;"', cont).span()
            cont = cont[: pos3] + ' style="width: 100%; height: 100%;"' + cont[pos4:]
        except:
            pass

        # 保存修改后的html文件
        utils.write_utf8_html_file(path, cont)
















