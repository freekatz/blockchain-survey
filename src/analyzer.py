#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   analyzer.py
@Desc    :   
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/08/14 20:14       1uvu           1.0         
"""
from collections import Counter
import pandas as pd
import numpy as np
import json
import copy
import re

from utils import stem, similar_replace, remove_chore
from plot import cloud_plot, bar_plot
"""
1. 每个话题词对应一个出现频率（所有），再分别对每年的话题词统计频率（每年） 1
2. 每年对应多个论文，一个论文对应多个话题词（根据 1 扫描整个数据集的话题，即可找出对应话题所属的文章，对于一年时，只需额外规定下年份即可）
结合 1，2 可画出每年 + 所有的话题词频率排行榜，及参考论文 1 中的图二
3. 每个话题词对应一个出现引用量（所有），再分别对每年的话题词统计引用量（每年） 1
结合 2，3 可画出画出每年 + 所有的话题词频率排行榜，及类似论文 1 中的图二
4. 根据话题引用量和频率可生成词云（每年和所有） 1
"""


# TODO: 20200902 以上分析 + 代码重新组织，完成初始版本

def topics_ranking(topics: pd.Series, opt="freq", args=None) -> {}:
    """
    
    :param topics: topics series
    :param opt: 'freq' means frequency or 'cite'
    :param args: a dict like {"base": None, "year": None}, base is cite or None, and year series
    :return:
    """
    rtn = {
        "all_rank": None,
        "items": [
        
        ]
    }

    rtn_item = {
                "year": "",
                "rank": {}
            }

    year = args["year"]
    base = args["base"]
    
    if opt == "freq":
        # all freq rank
        single_topics = []
        for t in topics:
            if pd.isna(t):
                single_topics += ["NaN"]
            else:
                single_topics += re.split(",", t)
        all_rank = dict(Counter(single_topics))
        rtn["all_rank"] = all_rank
        # freq rank year by year
        year_set = set(year)
        for y in year_set:
            item = copy.deepcopy(rtn_item)
            item["year"] = y
            s_topics = []
            for _y, _t in zip(year, topics):
                if _y == y:
                    if pd.isna(_t):
                        s_topics += ["NaN"]
                    else:
                        s_topics += re.split(",", _t)
            _rank = dict(Counter(s_topics))
            item["rank"] = _rank
            rtn["items"].append(item)
        
    elif opt == "cite":
        # if topics nan, then pass
        # merge => {"topic", cite}
        all_rank = {}
        for t, c in zip(topics, base):
            if not pd.isna(t):
                for tt in re.split(",", t):
                    if tt in all_rank.keys():
                        all_rank[tt] += int(c)
                    else:
                        all_rank[tt] = int(c)
        rtn["all_rank"] = all_rank
        # freq rank year by year
        year_set = set(year)
        for y in year_set:
            item = copy.deepcopy(rtn_item)
            item["year"] = y
            _rank = {}
            for _y, _t, _c in zip(year, topics, base):
                if _y == y:
                    if not pd.isna(_t):
                        for _tt in re.split(",", _t):
                            if _tt in _rank.keys():
                                _rank[_tt] += int(_c)
                            else:
                                _rank[_tt] = int(_c)
            item["rank"] = _rank
            rtn["items"].append(item)
        pass
    else:
        raise Exception("Invalid option string.")
    
    return rtn


if __name__ == '__main__':
    df = pd.read_excel("./out/all-preprocessed.xlsx")
    
    opt = "freq"

    res = topics_ranking(
        df["topics"],
        opt,
        {
            "base": None,
            "year": df["year"]
        }
    )
    # opt = "cite"
    #
    # res = topics_ranking(
    #     df["topics"],
    #     opt,
    #     {
    #         "base": df["cite"],
    #         "year": df["year"]
    #     }
    # )

    rank = res["all_rank"]
    f = open("./out/rank/%s/txt/all_rank.txt" % opt, "w", encoding="utf-8")
    i = 1
    for topic in sorted(rank.items(), key=lambda x: x[1], reverse=True):
        f.write(f"({i}) {topic[0]}: {topic[1]} \n")
        # print(f"({i}) {topic[0]}: {topic[1]}")
        i += 1
    f.close()
    # plot
    cloud_plot(rank, "./out/rank/%s/cloud/all_wordcloud.png" % opt)
    bar_plot(rank, "./out/rank/%s/bar/all_bar.png" % opt)
    for i in range(len(res["items"])):
        _item = res["items"][i]
        _rank = _item["rank"]
        f = open("./out/rank/%s/txt/%s_rank.txt" % (opt, _item["year"]), "w", encoding="utf-8")
        i = 1
        for topic in sorted(_rank.items(), key=lambda x: x[1], reverse=True):
            f.write(f"({i}) {topic[0]}: {topic[1]} \n")
            # print(f"({i}) {topic[0]}: {topic[1]}")
            i += 1
        f.close()
        # plot
        cloud_plot(_rank, "./out/rank/%s/cloud/%s_wordcloud.png" % (opt, _item["year"]))
        bar_plot(_rank, "./out/rank/%s/bar/%s_bar.png" % (opt, _item["year"]))
