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
from settings import *


# todo refactor this function
def topics_analysis(topics: pd.Series, opt="freq", args=None) -> {}:
    """
    
    :param topics: topics series
    :param opt: 'freq' means frequency or 'cite', as the basis of topics ranking
    :param args: a dict like {"base": None, "year": None}, base is cite or None, and year series
    :return: like the following dict struct, the all is all topics,
    a tuple list like [(<topics str>, <freq or cites>), (...), ...],
    and the items contain 5 years 2016-2020's topics rank
    """
    rtn = {
        "all": None,
        "years": [
        
        ]
    }
    
    rtn_year = {
        "year": "",
        "items": {}
    }
    
    year_list = args["year"]
    base_list = args["base"]
    
    if opt == "freq":
        # all freq rank
        all_topics = []
        for t in topics:
            if pd.isna(t):
                all_topics += ["nothing"]
            else:
                all_topics += re.split(",", t)
        all = dict(Counter(all_topics))
        rtn["all"] = all
        # freq rank year by year
        year_set = set(year_list)
        for y in year_set:
            year = copy.deepcopy(rtn_year)
            year["year"] = y
            year_topics = []
            for _y, _t in zip(year_list, topics):
                if _y == y:
                    if pd.isna(_t):
                        year_topics += ["nothing"]
                    else:
                        year_topics += re.split(",", _t)
            items = dict(Counter(year_topics))
            year["items"] = items
            rtn["years"].append(year)
    
    elif opt == "cite":
        # if topics nan, then pass
        # merge => {"topic", cite}
        all = {"nothing": 0}
        for b, t in zip(base_list, topics):
            if pd.isna(t):
                all["nothing"] += int(b)
            else:
                for tt in re.split(",", t):
                    if tt in all.keys():
                        all[tt] += int(b)
                    else:
                        all[tt] = int(b)
        rtn["all"] = all
        # freq rank year by year
        year_set = set(year_list)
        for y in year_set:
            year = copy.deepcopy(rtn_year)
            year["year"] = y
            items = {"nothing": 0}
            for _y, _t, _b in zip(year_list, topics, base_list):
                if _y == y:
                    if pd.isna(_t):
                        items["nothing"] += int(_b)
                    else:
                        for _tt in re.split(",", _t):
                            if _tt in items.keys():
                                items[_tt] += int(_b)
                            else:
                                items[_tt] = int(_b)
            year["items"] = items
            rtn["years"].append(year)
        pass
    else:
        raise Exception("Invalid option string.")
    
    return rtn


def topics_vector(df: pd.DataFrame, security_topics: list) -> dict:
    rtn_topic = {}
    origin_topics = df["topics"].tolist()
    urls = df["url"].tolist()
    topics = [(u, re.split(",", str(o))) for u, o in zip(urls, origin_topics)]
    for s_topic in security_topics:
        for topic in topics:
            if s_topic in topic[1]:
                if s_topic not in rtn_topic.keys():
                    rtn_topic[s_topic] = [[topic[0]], [topic[1]]]
                else:
                    rtn_topic[s_topic][0].append(topic[0])
                    rtn_topic[s_topic][1].append(topic[1])
    ul = []
    for k in rtn_topic.keys():
        ul += rtn_topic[k][0]
        for t in rtn_topic[k][1]:
            try:
                t.remove(k)
            except:
                pass
            try:
                t.remove('')
            except:
                pass
            try:
                t.remove('nothing')
            except:
                pass
    jf = open(analyzer_output_dir + "/security.json", "w")
    js = json.dumps(rtn_topic)
    jf.write(js)
    jf.close()
    us = set(ul)
    ddf = df[df['url'].isin(us)]
    ddf.to_excel(analyzer_output_dir = "/all-security.xlsx", index=False)
    df1 = pd.DataFrame(columns=["title", "year", "abstract", "url", "topics"])
    df1["title"] = ddf["title"]
    df1["year"] = ddf["year"]
    df1["abstract"] = ddf["abstract"]
    df1["url"] = ddf["url"]
    df1["topics"] = ddf["topics"]

    df1.to_html(analyzer_output_dir + "/security.htm")
    return rtn_topic


def format(res: dict) -> pd.DataFrame:
    all = res["all"]
    df = pd.DataFrame(index=list(all.keys()), columns=["all"])
    df["all"] = list(all.values())
    
    years = res["years"]
    items = res["all"]
    for year_item in years:
        _year_items = year_item["items"]
        _year = year_item["year"]
        _y = []
        for t in items.keys():
            if t in _year_items.keys():
                _y.append(items[t])
            else:
                _y.append(0)
        df[str(_year)] = _y
    return df


def analyzer_pipeline(df: pd.DataFrame, opt: str):
    if opt == "freq":
        base = None
    elif opt == "cite":
        base = df["cite"]
    else:
        base = None
    res = topics_analysis(
        df["topics"],
        opt,
        {
            "base": base,
            "year": df["year"]
        }
    )
    
    ddf = format(res)
    ddf.to_excel(analyzer_output_dir + "/all-%s.xlsx" % opt)
    return ddf


if __name__ == '__main__':
    df = pd.read_excel("./out/all-preprocessed.xlsx")
    s = open("./res/security.txt", "r")
    topics_vector(df, [l.strip() for l in s.readlines()])
    
    # options = ["freq", "cite"]
    # for opt in options:
    #     analyzer_pipeline(df, opt)
