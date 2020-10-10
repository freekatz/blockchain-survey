#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pipeline.py
@Desc    :
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/09/02 14:58       1uvu           0.0.1
"""
import pandas as pd

from preprocess import preprocess_pipeline
from filter import filter_pipeline
from analyzer import analyzer_pipeline
from plot import plot_pipeline
from utils import drop_nan

"""
crawler.py 1
filter.py 0
preprocess.py 1
analyzer.py 1
plot.py doing...
"""

if __name__ == '__main__':
    filter_pipeline()
    
    df = pd.read_excel("./out/all.xlsx")
    ddf = preprocess_pipeline(df)
    ddf.to_excel("./out/all-preprocessed.xlsx", index=False, encoding="utf-8")
    
    options = ["freq", "cite"]
    for opt in options:
        dddf = analyzer_pipeline(ddf, opt)
        dff = drop_nan(dddf)
        plot_pipeline(dff, opt)
