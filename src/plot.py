#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   plot.py
@Desc    :   
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/09/01 18:37       1uvu           1.0         
"""
import matplotlib.pyplot as plt
from numpy import median
import seaborn as sns
import numpy as np
import wordcloud
import json
import copy
import re


# 改得通用一些
# 散点图：竖轴 topics，横轴 year；竖轴 cite，横轴 topics；再来个 3D 的
# 条形图：1. topics 排行：frequency，cite；2. 每年论文数量排行：其中每一年中的论文某个话题数量

def cloud_plot(rank: dict, target):
    # style define
    w = wordcloud.WordCloud(
        width=1000, height=700,
        background_color='white',
        font_path='msyh.ttc'
    )
    _rank = copy.deepcopy(rank)
    try:
        _rank.pop("NaN")
    except:
        pass
    w.generate_from_frequencies(_rank)
    w.to_file(target)


def bar_plot(rank: dict, target, limit=20):
    # style define
    sns.set(style="darkgrid")
    f1, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlabel(re.search("rank/(.*?)/bar", target).groups()[0], fontsize=20)
    ax.set_ylabel('topic', fontsize=20, color='r')
    ax.set_title(re.search("bar/(.*?)_bar.png", target).groups()[0])
    
    _rank = copy.deepcopy(rank)
    try:
        _rank.pop("NaN")
    except:
        pass
    _rank = sorted(_rank.items(), key=lambda it: it[1], reverse=True)
    
    x = [int(v[1]) for v in _rank[:limit]]
    y = [k[0] for k in _rank[:limit]]
    sns.barplot(x=x, y=y, color="c", orient="h", estimator=median, palette="Blues_d")
    f1.savefig(target, dpi=100, bbox_inches='tight')
