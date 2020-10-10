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
                single_topics += [np.nan]
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
                        s_topics += [np.nan]
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


def analyzer_pipeline(df: pd.DataFrame, opt: str):
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
    ddf.to_excel("./out/rank/all-ranking-%s.xlsx" % opt)
    return ddf


if __name__ == '__main__':
    df = pd.read_excel("./out/all-preprocessed.xlsx")
    
    options = ["freq", "cite"]
    for opt in options:
        analyzer_pipeline(df, opt)
