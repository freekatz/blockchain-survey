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
from settings import *

# todo sim.txt class rule
"""
crawler.py 1
filter.py 0
preprocess.py 1
analyzer.py 1
plot.py doing...
"""

def sec():

    ori_df = pd.read_excel(output_root_dir + "/all.xlsx")

    pp_df = preprocess_pipeline(ori_df)
    pp_df.to_excel(preprocess_output_dir + "/all-preprocessed.xlsx", index=False)

    f_df = filter_pipeline(pp_df)
    f_df.to_excel(filter_output_auto_dir + "/all-no_filtered.xlsx", index=False)
    pp_df[~pp_df["title"].isin(f_df["title"])].to_excel(filter_output_auto_dir + "/all-filtered.xlsx", index=False)

    # # do filter manually
    f_df.to_excel(output_root_dir + "/all-nf.xlsx", index=False)
    pp_df[~pp_df["title"].isin(f_df["title"])].to_excel(filter_output_manual_dir + "/all-f.xlsx", index=False)

    # # f_df = pd.read_excel(filter_output_manual_dir + "/all-no_filtered.xlsx")
    options = ["freq", "cite"]
    for opt in options:
        a_df = analyzer_pipeline(f_df, opt)
        plot_pipeline(a_df, opt)


def sur():
    ori_df = pd.read_excel(output_root_dir + "/all-nf.xlsx")

    pp_df = preprocess_pipeline(ori_df)
    pp_df.to_excel(preprocess_output_dir + "/all-preprocessed.xlsx", index=False)
    pp_df.to_excel(preprocess_output_dir + "/all-pp.xlsx", index=False)
    
    options = ["freq", "cite"]
    for opt in options:
        a_df = analyzer_pipeline(pp_df, opt)
        # plot_pipeline(a_df, opt)
        
        
# survey
if __name__ == '__main__':
    if is_survey:
        sur()
    else:
        sec()
    

