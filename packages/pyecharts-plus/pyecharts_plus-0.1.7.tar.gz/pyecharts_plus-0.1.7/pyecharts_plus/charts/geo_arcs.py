# -*- coding: utf-8 -*-
# @Time     : 2018/11/9 14:22
# @Author   : Run 
# @File     : geo_arcs.py
# @Software : PyCharm


from pyecharts.chart import Chart
import re
from pyecharts import utils
from pyecharts_plus.datasets.coordinates import load_city_cp


class GeoArcs(Chart):
    """
    <<< 地理坐标系线图 >>>
    geo + scatter + lines + effect scatter
    """

    def __init__(self, title="", subtitle="",
                 geo_roam=True, is_toolbox_show=True, map_style="clear",
                 **kwargs):
        """

        :param title:
        :param subtitle:
        :param geo_roam: 地图是否可缩放，默认可以
        :param is_toolbox_show: 是否显示toolbox，默认显示，只包含下载图片的功能
        :param map_style: 地图的视觉风格，默认为clear
            clear: 清晰
            mist: 迷雾迷雾再迷雾
        :param kwargs:
        """
        # 预设画布的样式
        chart_style = {
            'background_color': '#404a59',
            'title_pos': 'center',
            'width': '100%',
            'height': 600
        }
        for key in kwargs:  # 可传入父类Chart接收的其他参数
            value = kwargs.get(key)
            if value is not None:
                chart_style[key] = value
        super(GeoArcs, self).__init__(title, subtitle, **chart_style)

        # toolbox
        if is_toolbox_show:
            self._option["toolbox"] = {
                "show": True,
                "orient": "vertical",
                "left": "95%",
                "top": "center",
                "feature": {
                    "saveAsImage": {
                        "show": True,
                        "title": "下载图片"
                    }
                }
            }
        else:
            self._option["toolbox"] = {}

        # geo
        self._option["geo"] = {
            "roam": bool(geo_roam),
            "map": "china",
            "itemStyle": {
                "normal": {
                    "areaColor": "#323c48",
                    "borderColor": "#111"
                },
                "emphasis": {
                    "areaColor": "#2a333d"
                }
            },
            "label": {
                "emphasis": {
                    "show": True,
                    "textStyle": {
                        "color": "#eee"
                    }
                }
            }
        }
        if map_style == "clear":
            self._option["geo"]["itemStyle"]["normal"]["borderColor"] = "#111"
        elif map_style == "mist":
            self._option["geo"]["itemStyle"]["normal"]["borderColor"] = '#404a59'
        else:
            raise Exception("invalid parameter map_style:", map_style)

        # init series
        self._option["series"] = []

        # init legend
        self._option["legend"] = {
            "show": False,
            "data": [],
            "orient": "vertical",
            "left": "left",
            "top": "center",
            "textStyle": {
                "fontSize": 12,
                "color": "#eee"
            },
            "selectedMode": "multiple"
        }

        # color
        self._option["color"] = [
            '#a6c84c', '#ffa022', '#46bee9', '#1A8C82', '#1C6FD4',
            '#2788FF', '#3B4CD0', '#45B194', '#584389', '#745CD9', '#7A574A', '#8DBD5E',
            '#8E323D', '#AC4343', '#AC62C7', '#B4665C', '#C85948', '#DC5FDA', '#E4B324',
            '#FFA324', '#077F9D', '#0CAAF3']

        # 城市中心点坐标
        self.city_cp_dict = load_city_cp()

    def add_arcs(self,
                 data_df,
                 from_col=0, to_col=1, legend_col=None,
                 fly_symbol="plane", fly_symbol_size=15, fly_symbol_color="#fff",
                 is_tail_show=True, tail_size=3, tail_color=None,
                 is_label_show=True):
        """

        :param data_df:
        :param from_col:
        :param to_col:
        :param legend_col:
        :param fly_symbol: 飞行特效的图标
            plane: 飞机。我已开始怀念你的美丽，在飞机挣扎着冲上天之后。
            arrow: 箭头
            circle
            rect
            roundRect
            triangle
            diamond
            pin
            arrow
        :param fly_symbol_size: 飞行特效图标的大小
        :param fly_symbol_color: 飞行特效图标的颜色
        :param is_tail_show: 飞行特效是否带有绚烂的长尾
        :param tail_size: 长尾特效的粗细
        :param tail_color: 长尾特效的色彩，如果不特别传入的话，和geo特效图标色彩保持一致
        :param is_label_show: 是否显示点的label，默认显示

        :notes:
            1. 尽量事先处理完全部要添加的数据，只调用一次该函数，多次调用可能会因为数据重复或矛盾造成意想不到的错误
        """
        # 图标样式库
        symbol_dict = {
            "plane": 'path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z'
        }
        symbol_dict.update({x: x for x in ['arrow', 'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow']})
        fly_symbol = symbol_dict[fly_symbol]

        # 调整数据列顺序
        col_list = [from_col, to_col] if legend_col is None else [from_col, to_col, legend_col]
        data_df = data_df.iloc[:, col_list]
        data_df.columns= ['from', 'to'] if legend_col is None else ['from', 'to', 'type']

        # 数据去重
        data_df = data_df.drop_duplicates().reset_index(drop=True)

        # filter invalid cities
        temp = list(set(data_df.iloc[:, 0].tolist() + data_df.iloc[:, 1].tolist()) - set(self.city_cp_dict))
        if len(temp) > 0:
            print("[add_arcs]无效的城市或区域名称有:", temp)
        data_df = data_df[data_df.iloc[:, 0].isin(self.city_cp_dict) & data_df.iloc[:, 1].isin(self.city_cp_dict)].reset_index(drop=True)

        # add coordinates
        data_df['from_coords'] = data_df['from'].apply(self.city_cp_dict.get)
        data_df['to_coords'] = data_df['to'].apply(self.city_cp_dict.get)

        # tooltip
        def tooltip_formatter1(params):
            results_str = params.data["fromName"] + ' > ' + params.data["toName"]
            return results_str
        #
        def tooltip_formatter2(params):
            results_str = '<div style="border-bottom: 1px solid rgba(255,255,255,.3); ' \
                          'font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' + \
                          params.seriesName + '</div>' + \
                          params.data["fromName"] + ' > ' + params.data["toName"]
            return results_str

        #
        if legend_col is None:
            # lines
            data1 = []
            for i in range(len(data_df)):
                data1.append(
                    {
                        "fromName": data_df.loc[i, "from"],
                        "toName": data_df.loc[i, "to"],
                        "coords": [data_df.loc[i, "from_coords"], data_df.loc[i, "to_coords"]]
                    }
                )
            if is_tail_show:
                if tail_color is None:
                    tail_color = fly_symbol_color
                self._option["series"].append(
                    {
                        "type": 'lines',
                        "zlevel": 1,
                        "effect": {
                            "show": True,
                            "period": 6,
                            "trailLength": 0.7,
                            "color": tail_color,
                            "symbolSize": tail_size
                        },
                        "lineStyle": {
                            "normal": {
                                "width": 0,
                                "curveness": 0.2
                            }
                        },
                        "data": data1
                    }
                )
            self._option["series"].append(
                {
                    "type": 'lines',
                    "zlevel": 2,
                    "symbol": ['none', 'arrow'],
                    "effect": {
                        "show": True,
                        "period": 6,
                        "trailLength": 0,
                        "symbol": fly_symbol,
                        "symbolSize": fly_symbol_size,
                        "color": fly_symbol_color,
                    },
                    "lineStyle": {
                        "normal": {
                            "width": 1,
                            "opacity": 0.6,
                            "curveness": 0.2
                        }
                    },
                    "data": data1,
                    "tooltip": {
                        "formatter": tooltip_formatter1
                    }
                }
            )
            # scatter
            data2 = []
            for city in set(data_df['from'].unique().tolist() + data_df['to'].unique().tolist()):
                data2.append(
                    {
                        "name": city,
                        "value": self.city_cp_dict[city]
                    }
                )
            self._option["series"].append(
                {
                    "type": "scatter",
                    "coordinateSystem": "geo",
                    "zlevel": 2,
                    "label": {
                        "normal": {
                            "show": is_label_show,
                            "textStyle": {
                                "fontSize": 12,
                                "color": "#eee"
                            },
                            "position": "right",
                            "formatter": "{b}"
                        }
                    },
                    "tooltip": {
                        "formatter": "{b}"
                    },  # todo
                    "symbolSize": 10,
                    "data": data2
                }
            )
        else:
            # legend
            self._option["legend"]["show"] = True
            self._option["legend"]["data"] += data_df.type.unique().tolist()

            # series
            groups = data_df.groupby('type')
            for legend, df in groups:
                # lines
                data1 = []
                for i in range(len(df)):
                    data1.append(
                        {
                            "fromName": df.iloc[i]["from"],
                            "toName": df.iloc[i]["to"],
                            "coords": [df.iloc[i]["from_coords"], df.iloc[i]["to_coords"]]
                        }
                    )
                if is_tail_show:
                    if tail_color is None:
                        tail_color = fly_symbol_color
                    self._option["series"].append(
                        {
                            "name": legend,
                            "type": 'lines',
                            "zlevel": 1,
                            "effect": {
                                "show": True,
                                "period": 6,
                                "trailLength": 0.7,
                                "color": tail_color,
                                "symbolSize": tail_size
                            },
                            "lineStyle": {
                                "normal": {
                                    "width": 0,
                                    "curveness": 0.2
                                }
                            },
                            "data": data1
                        }
                    )
                self._option["series"].append(
                    {
                        "name": legend,
                        "type": 'lines',
                        "zlevel": 2,
                        "symbol": ['none', 'arrow'],
                        "effect": {
                            "show": True,
                            "period": 6,
                            "trailLength": 0,
                            "symbol": fly_symbol,
                            "symbolSize": fly_symbol_size,
                            "color": fly_symbol_color,
                        },
                        "lineStyle": {
                            "normal": {
                                "width": 1,
                                "opacity": 0.6,
                                "curveness": 0.2
                            }
                        },
                        "data": data1,
                        "tooltip": {
                            "formatter": tooltip_formatter2
                        }
                    }
                )
                # scatter
                data2 = []
                for city in set(df['from'].unique().tolist() + df['to'].unique().tolist()):
                    data2.append(
                        {
                            "name": city,
                            "value": self.city_cp_dict[city]
                        }
                    )
                self._option["series"].append(
                    {
                        "name": legend,
                        "type": "scatter",
                        "coordinateSystem": "geo",
                        "zlevel": 2,
                        "label": {
                            "normal": {
                                "show": is_label_show,
                                "textStyle": {
                                    "fontSize": 12,
                                    "color": "#eee"
                                },
                                "position": "right",
                                "formatter": "{b}"
                            }
                        },
                        "tooltip": {
                            "formatter": "{b}"
                        },  # todo
                        "symbolSize": 10,
                        "data": data2
                    }
                )

    def add_scatter(self, name, data, is_label_show=False):
        """
        添加一组effect scatter
        :param name: legend中显示的名称
        :param data: [{"name": name, "value": [lgt, lat, ...]}, ...]
        :param is_label_show: 是否显示label
        :return:
        """
        temp = {
            "name": name,
            "type": "effectScatter",
            "coordinateSystem": "geo",
            "symbol": "circle",
            "symbolSize": 13,
            "rippleEffect": {
                "brushType": "stroke",
                "period": 4,
                "scale": 5
            },
            "showEffectOn": "render",
            "tooltip": {
                "formatter": "{b}"
            },
            "data": data
        }
        if is_label_show:
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
        self._option["legend"]["data"].append(name)

    def add_city_scatter(self, name, city_list, is_label_show=False):
        """
        传入一列城市名，自动匹配坐标，添加effect scatter
        :param name: 在legend中显示的名称
        :param city_list:
        :param is_label_show: 是否显示label
        :return:
        """
        # filter invalid cities
        temp = list(set(city_list) - set(self.city_cp_dict))
        if len(temp) > 0:
            print("[add_city_scatter]无效的城市或区域名称有:", temp)
        #
        data = []
        for city in city_list:
            if city in self.city_cp_dict:
                data.append(
                    {
                        "name": city,
                        "value": self.city_cp_dict[city]
                    }
                )
        #
        self.add_scatter(name, data, is_label_show)

    def render(self, path="render.html", template_name="simple_chart.html", object_name="chart", **kwargs):
        """
        将图表保存成html文件，默认占满屏幕
        :param path:
        :param template_name:
        :param object_name:
        :param kwargs:
        :return:
        """

        super(GeoArcs, self).render(path, "simple_chart.html", "chart", **kwargs)
        with open(path, 'r', encoding="utf-8") as file:
            cont = file.read()

        # 导入地图js
        pos1 = re.search("<body>\n\s*<div id=", cont).span()[0] + 7
        cont = cont[: pos1] + \
        """<script type="text/javascript" src="http://echarts.baidu.com/gallery/""" + \
        """vendors/echarts/map/js/china.js"></script>\n""" + cont[pos1:]

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
