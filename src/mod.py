#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   mod.py
@Desc    :   添加新功能
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/12/29 17:22       1uvu           0.0.1
"""
import pandas as pd
import re

from settings import *
from utils import *

path = '/all-nf.xlsx'
df = pd.read_excel(output_root_dir + "/all-nf.xlsx")
title_items = df['title']
topics_items = df['topics']

labels = [
    'security', 'privacy', 'performance',
    'interoperability', 'regulation',
    'governance', 'usability'
]

title_list = []
tag_list = []
for title, topics in zip(title_items, topics_items):
    # if type(topics) != type(''):
    #     continue
    topics = similar_replace(topics)
    
    topics_list = re.split(',', topics)
    _tag = []
    f = False
    for key in labels:
        if key in topics:
            f = True
            _tag.append(key)
            print(_tag, topics_list)
    if f:
        title_list.append(title)
        tag_list.append(','.join(_tag))

tag_list = [l for l in tag_list if l != '']
title_list = list(set(title_list))
print(tag_list)
print(len(title_list))
print(len(tag_list))

ddf = df[df['title'].isin(title_list)]
ddf['tags'] = tag_list

dddf = pd.DataFrame(columns=['tags', 'title', 'topics', 'abstract'])
dddf['tags'] = tag_list
dddf['title'] = list(ddf['title'])
dddf['topics'] = list(ddf['topics'])
dddf['abstract'] = list(ddf['abstract'])

ddf.to_excel(analyzer_output_dir + '/spp.xlsx', index=False)
dddf.to_html(analyzer_output_dir + '/spp.htm', index=True)

