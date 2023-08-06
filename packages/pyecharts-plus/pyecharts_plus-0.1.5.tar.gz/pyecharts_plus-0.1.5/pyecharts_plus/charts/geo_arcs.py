# -*- coding: utf-8 -*-
# @Time     : 2018/11/9 14:22
# @Author   : Run 
# @File     : geo_arcs.py
# @Software : PyCharm


from pyecharts import GeoLines
import re
from pyecharts import utils
from pyecharts_plus.datasets.coordinates import load_city_cp


class GeoArcs(GeoLines):
    """
    <<< 地理坐标系线图 >>>
    相比于pyecharts中提供的GeoLines，只是预设了一套样式，改动了添加数据的方式，过滤了无法画出的城市，润色了保存的html文件。
    todo 1.摆脱对pyecharts中父类GeoLines的函数add的依赖，直接操作self._option来实现目的 2. 完善tooltip的显示
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
            'background_color': '#404a59',
            'width': '100%',
            'height': 600
        }
        for key in kwargs:
            value = kwargs.get(key)
            if value is not None:
                self.style[key] = value

        super(GeoArcs, self).__init__(title, subtitle, **self.style)

        # toolbox todo 置于函数add_data内
        self._option["toolbox"] = {
            "show": True,
            "orient": "vertical",
            "left": "95%",
            "top": "center",
            "feature": {
                "saveAsImage": {
                    "show": True,
                    "title": "\u4e0b\u8f7d\u56fe\u7247"
                }
            }
        }

        #
        self.valid_city_dict = load_city_cp()
        # self.invalid_cities = None

    def add_coordinate(self, name, longitude, latitude):
        """
        重写父类的方法
        Add a geo coordinate for a position.
        :param name: The name of a position
        :param longitude: The longitude of coordinate.
        :param latitude: The latitude of coordinate.
        :return:
        """
        self._coordinates.update({name: [longitude, latitude]})
        self.valid_city_dict.update({name: [longitude, latitude]})

    def add_arcs(self,
                 data_df,
                 from_col=0, to_col=1, legend_col=None,
                 **kwargs):
        """

        :param data_df:
        :param from_col:
        :param to_col:
        :param legend_col:
        :param kwargs:
        :return:

        :notes:
            1. 只使用一次该函数添加所有数据，多次调用的话，并未编写和之前去重的功能
        """
        # 数据去重
        data_df = data_df.drop_duplicates().reset_index(drop=True)

        # 调整数据列顺序
        if legend_col is None:
            col_list = [from_col, to_col]
        else:
            col_list = [from_col, to_col, legend_col]
        data_df = data_df.iloc[:, col_list]

        # filter invalid cities
        temp = list(set(data_df.iloc[:, 0].tolist() + data_df.iloc[:, 1].tolist()) - set(self.valid_city_dict))
        if len(temp) > 0:
            print("[add_arcs]无效的城市或区域名称有:", temp)
        data_df = data_df[data_df.iloc[:, 0].isin(self.valid_city_dict) & data_df.iloc[:, 1].isin(self.valid_city_dict)]

        #
        style_geo = {
            'geo_effect_symbol': 'plane',
            'geo_effect_symbolsize': 15,
            'is_label_show': True,
            'label_color': ['#a6c84c', '#ffa022', '#46bee9', '#077F9D', '#0CAAF3', '#1A8C82', '#1C6FD4',
                            '#2788FF', '#3B4CD0', '#45B194', '#584389', '#745CD9', '#7A574A', '#8DBD5E',
                            '#8E323D', '#AC4343', '#AC62C7', '#B4665C', '#C85948', '#DC5FDA', '#E4B324',
                            '#FFA324'],
            'label_formatter': '{b}',
            'label_pos': 'right',
            'label_text_color': '#eee',
            'legend_pos': 'left',
            'legend_top': 'center',
            'legend_orient': 'vertical',
            'legend_text_color': '#eee',
            'line_curve': 0.2,
            'line_opacity': 0.6
        }
        for key in kwargs:
            value = kwargs.get(key)
            if value is not None:
                style_geo[key] = value

        if legend_col is None:
            self.add("", list(zip(data_df.iloc[:, 0], data_df.iloc[:, 1])), **style_geo)  #
        else:
            groups = data_df.groupby(data_df.columns[2])
            for legend, df in groups:
                self.add(legend, list(zip(df.iloc[:, 0], df.iloc[:, 1])), **style_geo)

    def add_scatter(self, name, data, is_label_display=False):
        """
        添加一组effect scatter
        :param name: legend中显示的名称
        :param data: [{"name": name, "value": [lgt, lat, ...]}, ...]
        :param is_label_display: 是否显示label
        :return:
        """
        temp = {
            "name": name,
            "type": "effectScatter",
            "coordinateSystem": "geo",
            "symbol": "circle",
            "symbolSize": 12,
            "rippleEffect": {
                "brushType": "stroke",
                "period": 4,
                "scale": 5
            },
            "showEffectOn": "render",
            "data": data
        }
        if is_label_display:
            temp["label"] = {
                "normal": {
                    "show": True,
                    "position": "top",
                    "formatter": "{b}",
                    "textStyle": {
                        "fontSize": 12
                    }
                }
            }
        self._option["series"].append(temp)
        # legend
        if "legend" not in self._option:
            self._option["legend"] = {
                "show": True,
                "orient": "vertical",
                "left": "left",
                "top": "center",
                "data": [],
                "textStyle": {
                    "color": "#eee",
                    "fontSize": 12
                },
                "selectedMode": "multiple"
            }
        self._option["legend"][0]["data"].append(name)

    def add_city_scatter(self, name, city_list, is_label_display=False):
        """
        传入一列城市名，自动匹配坐标，添加effect scatter
        :param name: 在legend中显示的名称
        :param city_list:
        :param is_label_display: 是否显示label
        :return:
        """
        # filter invalid cities
        temp = list(set(city_list) - set(self.valid_city_dict))
        if len(temp) > 0:
            print("[add_city_scatter]无效的城市或区域名称有:", temp)
        #
        data = []
        for city in city_list:
            if city in self.valid_city_dict:
                data.append(
                    {
                        "name": city,
                        "value": self.valid_city_dict[city]
                    }
                )
        #
        self.add_scatter(name, data, is_label_display)

    def render(self, path="render.html", template_name="simple_chart.html", object_name="chart", **kwargs):
        """
        将图表保存成html文件，默认占满屏幕
        :param path:
        :param template_name:
        :param object_name:
        :param kwargs:
        :return:
        """

        super(GeoLines, self).render(path, "simple_chart.html", "chart", **kwargs)
        with open(path, 'r', encoding="utf-8") as file:
            cont = file.read()

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
