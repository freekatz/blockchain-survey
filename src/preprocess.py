#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   preprocess.py
@Desc    :
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/09/02 14:41       1uvu           0.0.1
"""
import texthero as hero
import nltk.stem as ns
import pandas as pd
import numpy as np
import re

from utils import stem, similar_replace, remove_chore


def preprocess_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # drop duplicates
    # date2year
    # fill na and modify invalid value
    # topics normalize
    ddf = df.copy()
    ddf["year"] = year(ddf)
    ddf = fill(ddf)
    ddf = drop(ddf)
    ddf["topics"] = norm(ddf)
    return ddf


def drop(df: pd.DataFrame) -> pd.DataFrame:
    """
    
    :param df:
    :return:
    :notice: if a series has many na or same values, don't use this func, such as many '0',
        because it maybe rm data lines but no duplicated
    """
    ddf = df.copy(deep=False)
    ddf = ddf.drop_duplicates(["abstract"]).drop_duplicates(["url"]).drop_duplicates(["title"])
    # don't drop nan here
    return ddf


def year(df: pd.DataFrame) -> pd.Series:
    ys = []
    for _y in df["year"]:
        year = str(_y).strip()
        if "-" in year and not re.search("[a-z|A-Z]", year):
            y = re.split("-", year)[0]
        else:
            y = re.split(" ", year)[-1]
        ys.append(y)
    return pd.Series(ys)


def fill(df: pd.DataFrame) -> pd.DataFrame:
    """
    
    :param df:
    :return:
    :notice: only 'cite' series be filled by '0', others use 'nothing' to fill
    """
    cite = []
    for c in df["cite"]:
        if pd.isna(c):
            cite.append("0")
        else:
            cite.append(str(re.split(" ", str(c))[0]))
    ddf = df.copy(deep=False)
    ddf["cite"] = pd.Series(cite)
    
    return ddf


def norm(df: pd.DataFrame) -> pd.Series:
    ddf = df.copy(deep=False)
    lemmatizer = ns.WordNetLemmatizer()
    topics = []
    for t_item, o_item in zip(ddf["topics"], ddf["origin"]):
        # ieee topics select
        if o_item == "ieee":
            if "IEEE" in t_item:
                ts = re.split(",", re.search("IEEE Keywords:(.*?);", t_item).groups()[0])
            elif "Author" in t_item:
                ts = re.split(",", re.split(":", t_item)[-1])
            else:
                ts = re.split(",", re.search("INSPEC: Controlled Indexing:(.*?);", t_item).groups()[0])
        else:
            ts = re.split(",", str(t_item))
            
        # topic of one paper process
        ts = hero.remove_html_tags(hero.lowercase(pd.Series(ts)))
        topic = []
        for t in ts:
            t.replace(" - ", "-")
            if len(re.split("and", t)) == 2 and "-" not in t:
                topic += re.split("and", t)
                continue
            if len(re.split("/", t)) == 2:
                topic += re.split("/", t)
                continue
            if "blockchain" in t and len(re.split(" ", t)) >= 2:
                t = re.split(" ", t)[-1]
            if t != "":
                topic.append(t.replace("\xa0", ""))
        topics.append(",".join([similar_replace(stem(remove_chore(t), lemmatizer)) for t in topic]))
        # topics.append(",".join([stem(remove_chore(t), lemmatizer) for t in topic]))
    return pd.Series(topics)


if __name__ == '__main__':
    df = pd.read_excel("./out/all.xlsx")
    
    ddf = preprocess_pipeline(df)
    
    ddf.to_excel("./out/all-preprocessed.xlsx", index=False, encoding="utf-8")
