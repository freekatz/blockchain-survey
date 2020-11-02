#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   filter.py
@Desc    :
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/09/02 14:51       1uvu           0.0.1
"""
import re
import pandas as pd

from configs import *
from settings import *


def filter_auto(df: pd.DataFrame) -> pd.DataFrame:
    ddf = df.copy(deep=True)
    titles = df["title"].tolist()

    # a_titles = []
    # for p in allow_patterns:
    #     for t in titles:
    #         if re.search(p, t) is not None:
    #             a_titles.append(t)
    # ddf = ddf[ddf["title"].isin(a_titles)]

    d_titles = []
    for p in deny_patterns:
        for t in titles:
            if re.search(p, t) is not None:
                d_titles.append(t)
    ddf = ddf[~ddf["title"].isin(d_titles)]
    return ddf


def filter_manual():
    df = pd.read_excel(preprocess_output_dir + "/all-preprocessed.xlsx")
    
    ddf = pd.read_excel(filter_output_manual_dir + "/all-nf.xlsx")
    
    return df[df["title"].isin(ddf["title"])]


def filter_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # ddf = filter_auto(df)

    ddf = filter_manual()
    return ddf


if __name__ == '__main__':
    pass
    # df = pd.read_excel(preprocess_output_dir + "/all-preprocessed.xlsx")
    #
    # ddf = pd.read_excel(filter_output_manual_dir + "/all-nf.xlsx")
    #
    # df[df["title"].isin(ddf["title"])].to_excel(filter_output_manual_dir + "/all-nf.xlsx", index=False)
    # df[df["title"].isin(ddf["title"])].to_excel(output_root_dir + "/all-nf.xlsx", index=False)


