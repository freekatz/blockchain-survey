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
from plot import plot_pipeline

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
    :param opt: 'freq' means frequency or 'cite', as the basis of topics ranking
    :param args: a dict like {"base": None, "year": None}, base is cite or None, and year series
    :return: like the following dict struct, the all_rank is all topics rank,
    a tuple list like [(<topics str>, <freq or cites>), (...), ...],
    and the items contain 5 years 2016-2020's topics rank
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


def format(res: dict) -> pd.DataFrame:
    rank = res["all_rank"]
    df = pd.DataFrame(index=list(rank.keys()), columns=["all"])
    df["all"] = list(rank.values())
    
    rank_items = res["items"]
    year_rank = []
    for item in rank_items:
        year_rank = []
        _rank = item["rank"]
        _year = item["year"]
        _r = []
        for t in rank.keys():
            if t in _rank.keys():
                _r.append(_rank[t])
            else:
                _r.append(0)
        df[str(_year)] = _r
    return df


if __name__ == '__main__':
    df = pd.read_excel("./out/all-preprocessed.xlsx")
    
    options = ["freq", "cite"]
    for opt in options:
        if opt == "freq":
            base = None
        elif opt == "cite":
            base = df["cite"]
        else:
            base = None
        res = topics_ranking(
            df["topics"],
            opt,
            {
                "base": base,
                "year": df["year"]
            }
        )
        
        ddf = format(res)
        print(ddf)
        ddf.to_excel("./out/rank/all-analyzed-%s.xlsx" % opt)
