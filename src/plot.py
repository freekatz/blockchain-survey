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
from matplotlib import ticker
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
    plt.cla()


def bar_hop_plot(df: pd.DataFrame, opt: str, height: float, step: int):
    target = plot_output_dir + "/bar-hop-%s.png" % opt
    
    df.plot.bar(y=df.columns[1:], stacked=True)
    
    if opt == "freq":
        if is_survey:
            title = "Literature Frequency Rank about Blockchain Survey"
        else:
            title = "Literature Frequency Rank about Blockchain Security"
    else:
        if is_survey:
            title = "Literature Cite Rank about Blockchain Survey"
        else:
            title = "Literature Cite Rank about Blockchain Security"
    ax = plt.gca()
    ax.set_title(title, fontsize=13)
    ax.legend(loc='best', fontsize=8, ncol=6)
    plt.xticks(fontsize=6, horizontalalignment='left', rotation=320)
    # plt.yticks(np.arange(0, height, step), fontsize=8)
    
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600
    plt.tight_layout()
    plt.grid(axis="y", linestyle=":", linewidth=0.8)
    plt.savefig(target)
    plt.cla()


def line_plot(df: pd.DataFrame, labels: list):
    ddf = df[df.index.isin(labels)].T
    _, ax = plt.subplots()
    

    if is_survey:
        title = "Topic Line about Blockchain Survey"
    else:
        title = "Topic Line  about Blockchain Security"

    # Be sure to only pick integer tick locations.
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.style.use('ggplot')
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    for l in labels:
        plt.plot(ddf.index,  # x轴数据
                 ddf[l],  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=2,  # 折线宽度
                 # color='steelblue',  # 折线颜色
                 marker='o',  # 折线图中添加圆点
                 markersize=4,  # 点的大小
                 markeredgecolor='black',  # 点的边框色
                 markerfacecolor='brown',  # 点的填充色
                 )
    plt.xticks(fontsize=8, horizontalalignment='left', rotation=320)  # 改变x轴文字值的文字大小
    plt.ylabel('Frequency')
    plt.legend(loc='upper left', fontsize=8, ncol=1, labels=labels)
    plt.title(title, fontsize=13)
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600
    plt.tight_layout()
    plt.grid(axis="y", linestyle=":", linewidth=0.8)
    plt.savefig(plot_output_dir + "/topics line.png")
    plt.cla()
    

def bar_hop_plot2(df: pd.DataFrame, col: str, target: str, labels: list) -> (dict, set):
    # target re match

    d = pd.DataFrame(index=labels, columns=["all", "relevant", "no_relevant"])
    items = df[col]
    all = []
    relevant = []
    no_relevant = []

    sec = set()
    for l in labels:
        number = [0, 0]
        for it in items:
            if it is not np.nan:
                ts = [i.strip() for i in re.split(",", it)]
                if l in ts:
                    number[0] = number[0] + 1
                    if target in ts:
                        sec.add(it)
                        number[1] = number[1] + 1
                        # print(f"========\n{l} | {target}: {it}")
        all.append(number[0])
        relevant.append(number[1])
        no_relevant.append(number[0] - number[1])
    d["all"] = all
    d["relevant"] = relevant
    d["no_relevant"] = no_relevant
    print(len(sec))
    dd = d.sort_values("all")
    
    dd.plot.bar(y=d.columns[1:], stacked=True)
    
    title = "Literature Frequency Rank Relevant Security [Security Number: %s]" % (str(len(sec)))

    ax = plt.gca()
    ax.set_title(title, fontsize=13)
    ax.legend(loc='best', fontsize=8, ncol=6)
    plt.xticks(fontsize=6, horizontalalignment='left', rotation=320)
    # plt.yticks(np.arange(0, height, step), fontsize=8)
    
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['savefig.dpi'] = 600
    plt.tight_layout()
    plt.grid(axis="y", linestyle=":", linewidth=0.8)
    plt.savefig(plot_output_dir + "/bar-hop-freq-2.png")
    plt.cla()

    rtn = {}
    ls = labels.tolist()
    ls.remove(target)
    for it in items:
        if it in sec:
            ts = [i.strip() for i in re.split(",", it)]
            for l in ls:
                if l in rtn.keys():
                    if l in ts:
                        rtn[l] += 1
                else:
                    rtn[l] = 0
    return rtn, sec


def pie_plot(d: dict, total: int, th: float):
    sum = np.sum(list(d.values()))
    nth_index = []
    others = 0
    for (l, n) in d.items():
        if int(n) < th * sum / 100:
            others += int(n)
            nth_index.append(l)
    # print(np.sum(list(d.values())))
    for l in nth_index:
        d.pop(l)
    # print(np.sum(list(d.values())))
    d["others"] = others
    relevant = d.values()
    labels = [i + ": " + str(r) for (i, r) in d.items()]
    patches, l_text, p_text = plt.pie(list(relevant), labels=labels, autopct='%.2f', radius=1, startangle=90)

    for t in p_text:
        t.set_size(9)

    for t in l_text:
        t.set_size(7)

    plt.axis('equal')
    title = "Topics Pie Relevant Security [Number: %s, Total: %s]" % (str(total), str(sum))
    plt.title(title, fontsize=13)
    plt.tight_layout()
    plt.savefig(plot_output_dir + "/pie-freq.png")
    plt.cla()



def test(df: pd.DataFrame, opt: str):
    cols = ["2015", "2016", "2017", "2018", "2019", "2020"]
    labels = ["0"]
    ddf = df_coincide(df, cols, labels)
    
    ddf = ddf.sort_values("all", ascending=False)
    ddf.to_html(plot_output_dir + "./%s-coincide.htm" % opt, index=True)


def test1(df):
    cols = ["2015", "2016", "2017", "2018", "2019", "2020"]
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
    if opt == "cite":
        height = 5000
        step = 250
    else:
        height = 60
        step = 12
    
    cols = ["all", "2016", "2017", "2018", "2019", "2020"]
    limit = 15
    sort_col = "all"
    ddf = df[cols].sort_values(sort_col)[0 - limit:]
    
    bar_hop_plot(ddf, opt, height, step)
    # test(df, opt)
    # test1(df)
    if opt == "freq":
        if is_survey:
            d = pd.read_excel(preprocess_output_dir + "/all-pp.xlsx")
            col = "topics"
            target = "security"
            labels = ddf.sort_values(sort_col)[0 - limit:].index
            rtn, sec = bar_hop_plot2(d, col, target, labels)
            pie_plot(rtn, len(sec), 3.0)
            labels = [target, "cryptography", "consensus protocol", "network"]
            pass
        else:
            labels = ["cryptography", "mine", "consensus protocol", "solidity", "network", "formal approach"]
        line_plot(ddf[cols[1:]], labels)


# todo plot 可指定年份时间段
if __name__ == '__main__':

    options = ["freq", "cite"]
    for opt in options:
        df = pd.read_excel(analyzer_output_dir + '/all-%s.xlsx' % opt, index_col=0)
        plot_pipeline(df, opt)
