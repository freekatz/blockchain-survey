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


# # # rm titles auto
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

# # # rm titles manual
# df = pd.read_excel("./out/all-filtered.xlsx")
# #
# df1 = pd.DataFrame(columns=["title", "cite", "url"])
# df1["title"] = df["title"]
# df1["cite"] = df["cite"]
# df1["url"] = df["url"]
# print(df1)
#
# df1.to_html("./out/tmp.htm", encoding="utf-8")


# # index filter based manual
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


def filter_pipeline():
    pass
