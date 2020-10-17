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
import os

import matplotlib.pyplot as plt
from numpy import median
import seaborn as sns
import pandas as pd
import numpy as np
import wordcloud
import json
import copy
import re

from utils import drop_nan, df_coincide


def txt_rank(rank: dict, target: str):
    f = open(target, "w", encoding="utf-8")
    i = 1
    for topic in sorted(rank.items(), key=lambda x: x[1], reverse=True):
        f.write(f"({i}) {topic[0]}: {topic[1]} \n")
        i += 1
    f.close()


def word_cloud_plot(rank: dict, target: str):
    # style define
    w = wordcloud.WordCloud(
        width=1000, height=700,
        background_color='white',
        font_path='msyh.ttc'
    )
    _rank = copy.deepcopy(rank)
    
    w.generate_from_frequencies(_rank)
    w.to_file(target)


def bar_rank_plot(rank: dict, target: str, limit=20):
    # style define
    sns.set(style="darkgrid")
    f1, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlabel(re.search("rank/(.*?)/bar", target).groups()[0], fontsize=20)
    ax.set_ylabel('topic', fontsize=20, color='r')
    ax.set_title(re.search("bar/(.*?)_bar_rank.png", target).groups()[0])
    
    _rank = copy.deepcopy(rank)
    _rank = sorted(_rank.items(), key=lambda it: it[1], reverse=True)
    
    x = [int(v[1]) for v in _rank[:limit]]
    y = [k[0] for k in _rank[:limit]]
    sns.barplot(x=x, y=y, color="c", orient="h", estimator=median, palette="Blues_d")
    f1.savefig(target, dpi=100, bbox_inches='tight')


def bar_hop_plot(df: pd.DataFrame, target: str, limit: int, sort_col: str, height: float, step: int):
    ddf = df.sort_values(sort_col)[0 - limit:]
    ddf.plot.bar(y=ddf.columns[1:], stacked=True)
    
    ax = plt.gca()
    ax.set_title('f3', fontsize=18)
    ax.legend(loc='best', fontsize=12, ncol=4)
    plt.xticks(fontsize=6, horizontalalignment='left', rotation=320)
    plt.yticks(np.arange(0, height, step), fontsize=8)
    
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600
    plt.tight_layout()
    plt.grid(axis="y", linestyle=":", linewidth=0.5)
    plt.savefig(target)


def test(df: pd.DataFrame, opt: str):
    cols = ["2017", "2018", "2019", "2020"]
    labels = ["0"]
    ddf = df_coincide(df, cols, labels)
    
    ddf = ddf.sort_values("all", ascending=False)
    ddf.to_html("./%s-coincide.htm" % opt)
    
    
def test1(df):
    cols = ["2016", "2017", "2018", "2019", "2020"]
    labels = ["bitcoin", "ethereum", "hyperledger"]
    ddf = df[cols][df.index.isin(labels)]
    ddf = df[df.index.isin(ddf.index)]
    ddf = ddf.sort_values("all", ascending=False)
    print(ddf)


def plot_pipeline(df: pd.DataFrame, opt: str):
    # for col in df.columns:
    #     rank = df_rank(df, col)
    #
    #     p1 = "./out/plot/%s/txt/" % opt
    #     p2 = "./out/plot/%s/cloud/" % opt
    #     p3 = "./out/plot/%s/bar/" % opt
    #     path = [p1, p2, p3]
    #     for p in path:
    #         if not os.path.exists(p):
    #             os.makedirs(p)
    #
    #     txt_rank(rank, p1 + "%s_rank.txt" % col)
    #     word_cloud_plot(rank, p2 + "%s_word_cloud.png" % col)
    #     bar_rank_plot(rank, p3 + "%s_bar_rank.png" % col)
    
    # if opt == "cite":
    #     height = 3000
    #     step = 200
    # else:
    #     height = 360
    #     step = 50
    # bar_hop_plot(df, "./out/rank/bar-hop-%s.png" % opt, 30, "all", height, step)
    
    test(df, opt)
    # test1(df)


# todo 代码还是要继续改，现在太慢了，结构也不行(主要是画图这里，重复的处理过程应该用一个函数自动进行)
# 散点图：竖轴 topics，横轴 year；竖轴 cite，横轴 topics；再来个 3D 的
# 条形图：1. topics 排行：frequency，cite；2. 每年论文数量排行：其中每一年中的论文某个话题数量


if __name__ == '__main__':
    options = ["freq", "cite"]
    for opt in options:
        df = pd.read_excel('out/rank/all-ranking-%s.xlsx' % opt, index_col=0)
        dff = drop_nan(df)
        plot_pipeline(dff, opt)
        