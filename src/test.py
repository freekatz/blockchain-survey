#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   test.py
@Desc    :
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/08/31 16:03       1uvu           0.0.1
"""
import pandas as pd
import copy

from settings import out_data
from crawler import *

def topics(out):
    arxiv = ArxivCrawler()
    springer = SpringerCrawler()
    acm = AcmCrawler()
    science_direct = ScienceDirectCrawler()
    ieee = IeeeCrawler()
    out["topics"] = ""
    out["publisher"] = ""
    out["cite"] = ""

    # cite update
    origin = out["origin"]
    if origin == "arxiv":
        # arxiv.detail(out)
        pass
    elif origin == "springer":
        # springer.detail(out)
        pass
    elif origin == "acm":
        # acm.detail(out)
        pass
    elif origin == "science_direct":
        # science_direct.detail(out)
        pass
    elif origin == "ieee":
        ieee.detail(out)
        # pass
    else:
        raise Exception("Unknown Origin.")
    
    print(out)

if __name__ == '__main__':
    df = pd.read_excel("./out/all-filtered.xlsx")
    target_path = "./out/all-ieee.xlsx"
    crawler = Crawler()
    output = []
    a = 0
    i = 1
    for origin, url in zip(df["origin"][a:], df["url"][a:]):
        print(origin + ":" + url)
        out = copy.deepcopy(out_data)
        out["origin"] = origin
        out["url"] = url
        topics(out)
        i += 1
        print(i)
        output.append(out)
        crawler.save(output, target_path)