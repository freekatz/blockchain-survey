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
import pandas as pd
import numpy as np
import wordcloud
import json
import copy
import re


def cloud_plot(rank: dict, target: str):
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


def bar_plot(rank: dict, target: str, limit=20):
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


def test_plot(df):
    x = df['date'].values.tolist()
    y1 = df['psavert'].values.tolist()
    y2 = df['uempmed'].values.tolist()
    y3 = df['pce'].values.tolist()
    y4 = df['pop'].values.tolist()
    mycolors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']
    columns = ['psavert', 'uempmed']
    
    # Draw Plot
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
    ax.fill_between(x, y1=y1, y2=0, label=columns[1], alpha=0.5, color=mycolors[1], linewidth=2)
    ax.fill_between(x, y1=y2, y2=0, label=columns[0], alpha=0.5, color=mycolors[0], linewidth=2)
    ax.fill_between(x, y1=y3, y2=0, label=columns[1], alpha=0.5, color=mycolors[1], linewidth=2)
    ax.fill_between(x, y1=y4, y2=0, label=columns[0], alpha=0.5, color=mycolors[0], linewidth=2)
    # Decorations
    ax.set_title('Personal Savings Rate vs Median Duration of Unemployment', fontsize=18)
    ax.set(ylim=[0, 30])
    ax.legend(loc='best', fontsize=12)
    plt.xticks(x[::50], fontsize=10, horizontalalignment='center')
    plt.yticks(np.arange(2.5, 30.0, 2.5), fontsize=10)
    plt.xlim(-10, x[-1])
    
    # Draw Tick lines
    for y in np.arange(2.5, 30.0, 2.5):
        plt.hlines(y, xmin=0, xmax=len(x), colors='black', alpha=0.3, linestyles="--", lw=0.5)
    
    # Lighten borders
    plt.gca().spines["top"].set_alpha(0)
    plt.gca().spines["bottom"].set_alpha(.3)
    plt.gca().spines["right"].set_alpha(0)
    plt.gca().spines["left"].set_alpha(.3)
    plt.show()



def plot_pipeline(df: pd.DataFrame, opt: str):
    pass
    # f = open("./out/rank/%s/txt/%s_rank.txt" % (opt, suf), "w", encoding="utf-8")
    # i = 1
    # for topic in sorted(rank.items(), key=lambda x: x[1], reverse=True):
    #     f.write(f"({i}) {topic[0]}: {topic[1]} \n")
    #     # print(f"({i}) {topic[0]}: {topic[1]}")
    #     i += 1
    # f.close()
    # # plot pipeline
    # cloud_plot(rank, "./out/rank/%s/cloud/%s_wordcloud.png" % (opt, suf))
    # bar_plot(rank, "./out/rank/%s/bar/%s_bar.png" % (opt, suf))

# 改得通用一些
# 散点图：竖轴 topics，横轴 year；竖轴 cite，横轴 topics；再来个 3D 的
# 条形图：1. topics 排行：frequency，cite；2. 每年论文数量排行：其中每一年中的论文某个话题数量



