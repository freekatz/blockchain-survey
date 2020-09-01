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
import texthero as hero
import nltk.stem as ns
import pandas as pd
import numpy as np
import json
import re

from utils import *

"""
1. 每个话题词对应一个出现频率（所有），再分别对每年的话题词统计频率（每年）
2. 每年对应多个论文，一个论文对应多个话题词
结合 1，2 可画出每年 + 所有的话题词频率排行榜，及参考论文 1 中的图二
3. 每个话题词对应一个出现引用量（所有），再分别对每年的话题词统计引用量（每年）
结合 2，3 可画出画出每年 + 所有的话题词频率排行榜，及类似论文 1 中的图二
4. 根据话题引用量和频率可生成词云（每年和所有）
"""
# TODO: 20200902 以上分析 + 代码重新组织，完成初始版本

# fetch topics
df = pd.read_excel("./out/all-filled-na.xlsx")
topic_items = df["topics"]
topics = []
i = 0
for t_item in topic_items:
    o_item = df["origin"][i]
    if o_item == "ieee":
        if "Author" in t_item:
            ts = re.split(",", re.split(":", t_item)[-1])
        elif "IEEE" in t_item:
            ts = re.split(",", re.search("IEEE Keywords:(.*?);", t_item).groups()[0])
        else:
            ts = re.split(",", re.search("INSPEC: Controlled Indexing:(.*?);", t_item).groups()[0])
    else:
        ts = re.split(",", str(t_item))
    for t in ts:
        t.replace(" - ", "-")
        if len(re.split("and", t)) == 2 and "-" not in t:
            topics += re.split("and", t)
            continue
        if len(re.split("/", t)) == 2:
            topics += re.split("/", t)
            continue
        if "lockchain" in t and len(re.split(" ", t)) >= 2:
            t = re.split(" ", t)[-1]
        if t != "":
            topics.append(t.replace("\xa0", ""))

    i += 1

# lowercase etc. preprocess
s = pd.Series(topics)
s = hero.lowercase(s)
s = hero.remove_html_tags(s)

# normalize
lemmatizer = ns.WordNetLemmatizer()
ws = list(s)
ws_copy = list(s)
topics = []
for w in ws:
    topics.append(similar_replace(stem(remove_chore(w), lemmatizer)))

# ranking
topics_rank = dict(Counter(topics))

js = json.dumps(topics_rank)
with open("./out/topics_rank.json", "w") as f:
    f.write(js)
import wordcloud

# 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
w = wordcloud.WordCloud(
    width=1000,height=700,
    background_color='white',
    font_path='msyh.ttc'
)

# 调用词云对象的generate方法，将文本传入
w.generate_from_frequencies(topics_rank)

# 将生成的词云保存为output2-poem.png图片文件，保存到当前文件夹中
w.to_file('./out/topics-word-cloud.png')

f = open("./out/topics_rank.txt", "w", encoding="utf-8")
i = 1
for topic in sorted(topics_rank.items(), key=lambda x: x[1], reverse=True):
    f.write(f"({i}) {topic[0]}: {topic[1]} \n")
    # print(f"({i}) {topic[0]}: {topic[1]}")
    i += 1
f.close()

# # # rm titles
# #
# # """
# # B/based
# # P/powered
# # B/blockchain-
# # E/enabled
# # """
# ts = []
# with open("./out/titles.txt", "r", encoding="utf-8") as f:
#     for t in f.readlines():
#         if "Enabled" not in t:
#             ts.append(t)
#
# f.close()
# with open("./out/titles.txt", "w", encoding="utf-8") as f:
#     for t in ts:
#         f.write(t)

# df = pd.read_excel("./out/all-test.xlsx")
# f = open("./out/titles.txt", "r", encoding="utf-8")
# titles = [s.strip() for s in f.readlines()]
#
# # i=0
# # for t in df["title"]:
# #     print(t + ": " + titles[i])
# #     print(t in titles)
# #     i+=1
# df1 = df[df['title'].isin(titles)]
#
# df1.to_excel("./out/all-filtered.xlsx", index=False)

# df = pd.read_excel("./out/all-filtered.xlsx")
# #
# df1 = pd.DataFrame(columns=["title", "cite", "url"])
# df1["title"] = df["title"]
# df1["cite"] = df["cite"]
# df1["url"] = df["url"]
# print(df1)
#
# df1.to_html("./out/tmp.htm", encoding="utf-8")

# # index filter
# df = pd.read_excel("./out/all-filtered.xlsx")
# with open("./out/index.txt", "r", encoding="utf-8") as f:
#     indexs = [int(i.strip()) for i in f.readlines()]
#
#     titles = []
#     for i in range(len(df["title"])):
#         if i not in indexs:
#             titles.append(df["title"][i])
#
#     df1 = df[df["title"].isin(titles)]
#
#     print(df1)
#
#     df1.to_excel("./out/all-filtered-3.xlsx", encoding="utf-8", index=False)

# df = pd.read_excel("./out/all-filtered.xlsx")
#
# print(df["abstract"].duplicated())
#
# ddf = df.drop_duplicates(["abstract"])
#
# print(ddf)
#
# ddf.to_excel("./out/all-filtered-1.xlsx", encoding="utf-8", index=False)

# df1 = pd.read_excel("./out/all-1.xlsx")
# df2 = pd.read_excel("./out/all-2.xlsx")
#
# for i in range(len(df2)):
#     if df2["origin"][i] == "ieee":
#         df1["topics"][i] = df2["topics"][i]
#         df1["publisher"][i] = df2["publisher"][i]
#         df1["cite"][i] = df2["cite"][i]
#         df1["authors"][i] = df2["authors"][i]
#         df1["abstract"][i] = df2["abstract"][i]
#
# df1.to_excel("./out/all.xlsx", encoding="utf-8", index=False)
