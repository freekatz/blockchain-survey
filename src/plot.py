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

from utils import df_coincide, df_rank
from settings import *


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


def bar_rank_plot(rank: dict, target: str, limit=10):
    # style define
    sns.set(style="darkgrid")
    f1, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlabel(re.search("/(.*?)/bar", target).groups()[0], fontsize=20)
    ax.set_ylabel('topic', fontsize=20, color='r')
    ax.set_title(re.search("/(.*?)_bar_rank.png", target).groups()[0])
    
    _rank = copy.deepcopy(rank)
    _rank = sorted(_rank.items(), key=lambda it: it[1], reverse=True)
    
    x = [int(v[1]) for v in _rank[:limit]]
    y = [k[0] for k in _rank[:limit]]
    sns.barplot(x=x, y=y, color="c", orient="h", estimator=median, palette="Blues_d")
    f1.savefig(target, dpi=100, bbox_inches='tight')


def bar_hop_plot(df: pd.DataFrame, opt: str, limit: int, sort_col: str, height: float, step: int):
    target = plot_output_dir + "/bar-hop-%s.png" % opt
    
    ddf = df.sort_values(sort_col)[0 - limit:]
    ddf.plot.bar(y=ddf.columns[1:], stacked=True)
    
    ax = plt.gca()
    ax.set_title(opt, fontsize=18)
    ax.legend(loc='best', fontsize=12, ncol=4)
    plt.xticks(fontsize=6, horizontalalignment='left', rotation=320)
    # plt.yticks(np.arange(0, height, step), fontsize=8)
    
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600
    plt.tight_layout()
    plt.grid(axis="y", linestyle=":", linewidth=0.5)
    plt.savefig(target)


def test(df: pd.DataFrame, opt: str):
    cols = ["2015", "2016", "2017", "2018", "2019", "2020"]
    labels = ["0"]
    ddf = df_coincide(df, cols, labels)
    
    ddf = ddf.sort_values("all", ascending=False)
    ddf.to_html(plot_output_dir + "./%s-coincide.htm" % opt, index=True)
    
    
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
    #     p1 = plot_output_dir + "/%s/txt/" % opt
    #     p2 = plot_output_dir + "/%s/cloud/" % opt
    #     p3 = plot_output_dir + "/%s/bar/" % opt
    #     path = [p1, p2, p3]
    #     for p in path:
    #         if not os.path.exists(p):
    #             os.makedirs(p)
    #
    #     txt_rank(rank, p1 + "%s_rank.txt" % col)
    #     word_cloud_plot(rank, p2 + "%s_word_cloud.png" % col)
    #     bar_rank_plot(rank, p3 + "%s_bar_rank.png" % col)
    #
    # if opt == "cite":
    #     height = 5000
    #     step = 250
    # else:
    #     height = 800
    #     step = 50
    # bar_hop_plot(df, opt, 15, "all", height, step)
    # # bar_hop_plot(df, plot_output_dir + "/bar-hop-%s.png" % opt, 30, "all", 0, 0)
    
    test(df, opt)
    # test1(df)


if __name__ == '__main__':
    options = ["freq", "cite"]
    for opt in options:
        df = pd.read_excel(analyzer_output_dir + '/all-%s.xlsx' % opt, index_col=0)
        plot_pipeline(df, opt)
