#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   plot.py    
@Desc    :   
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/09/01 18:37       1uvu           1.0         
"""
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
from numpy import median
import json

# 散点图：竖轴 topics，横轴 year；竖轴 cite，横轴 topics；再来个 3D 的
# 条形图：1. topics 排行：frequency，cite；2. 每年论文数量排行：其中每一年中的论文某个话题数量

sns.set(style="darkgrid")
f1, ax = plt.subplots(figsize=(14, 10))
ax.set_xlabel('Frequency', fontsize=20)
ax.set_ylabel('Topic', fontsize=20, color='r')

with open("./out/topics_rank.json", "r") as f:
    js = f.read()
    topics = dict(json.loads(js))
    topics.pop("nan")
    rank = sorted(topics.items(), key=lambda item: item[1], reverse=True)
    
    _x = [int(v[1]) for v in rank[:20]]
    _y = [k[0] for k in rank[:20]]
    print(_y)
    sns.barplot(x=_x, y=_y, color="c", orient="h", estimator=median, palette="Blues_d")
    plt.show()
f.close()
f1.savefig('./out/topics-sample-rank.png', dpi=100, bbox_inches='tight')