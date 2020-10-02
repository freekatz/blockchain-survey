#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   tests.py
@Desc    :   
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/09/01 12:08       1uvu           1.0         
"""
import nltk.stem as ns

# from utils import *
#
# lemmatizer = ns.WordNetLemmatizer()
# print(stem("new monetary economics", lemmatizer))
# print(stem("iot networkings", lemmatizer))
#
# s = similar_replace("block chain,industry 40,industry 4.0")
# print(s)

# s = "daa[s(s1)]"
# s = remove_chore(s)
# print(s)

# from dash import Dash
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html
#
# from pandas_datareader import data as web
# from datetime import datetime as dt
#
# app = Dash('Hello World', external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
#
# app.layout = html.Div([
#     dcc.Dropdown(
#         id='my-dropdown',
#         options=[
#             {'label': 'Coke', 'value': 'COKE'},
#             {'label': 'Tesla', 'value': 'TSLA'},
#             {'label': 'Apple', 'value': 'AAPL'}
#         ],
#         value='COKE'
#     ),
#     dcc.Graph(id='my-graph')
# ], style={'width': '500'})
#
#
# @app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
# def update_graph(selected_dropdown_value):
#     df = web.DataReader(
#         selected_dropdown_value,
#         'yahoo',
#         dt(2017, 1, 1),
#         dt.now()
#     )
#     return {
#         'data': [{
#             'x': df.index,
#             'y': df.Close
#         }],
#         'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
#     }
#
#
# if __name__ == '__main__':
#     app.run_server()


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Import Data
df = pd.read_excel('out/rank/all-analyzed-freq.xlsx', index_col=0)

limit = 30
ddf = df.sort_values("all")[0 - limit:]
ddf = ddf.drop(index=np.nan)
# Prepare Data
x = ddf.index.tolist()
# x = [i for i in range(30)]

vstack = []
columns = ddf.columns[1:]
for t in columns:
    yi = ddf[t].values.tolist()
    print(yi)
    vstack.append(yi)

mycolors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']
y = np.vstack(vstack)
# Plot for each column
labs = columns
ax = plt.gca()
ax.stackplot(x, y, labels=labs, colors=mycolors, alpha=0.8)

# Decorations
ax.set_title('f1', fontsize=18)
ax.set(ylim=[0, 360])
ax.legend(fontsize=10, ncol=4)
plt.xticks(x[::1], fontsize=6, horizontalalignment='left', rotation=320)
plt.yticks(np.arange(0, 360, 50), fontsize=8)
plt.xlim(x[0], x[-1])

# Lighten borders
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)

plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600
plt.grid(axis="x", linestyle=":", linewidth=0.5)
plt.tight_layout()
plt.savefig("./out/rank/f1.png")

# mycolors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']
# columns = ["all", "2016", "2017", "2018", "2019", "2020"]
#
# # Draw Plot
# # fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=300)
# ax=plt.gca()
# i = 0
# for t in columns:
#     yi = ddf[t].values.tolist()
#     ax.fill_between(x, y1=yi, y2=yi, label=columns[i], alpha=0.8, color=mycolors[i], linewidth=1)
#     i += 1
#
# # Decorations
# ax.set_title('f2', fontsize=18)
# ax.legend(loc='best', fontsize=12, ncol=4)
# plt.xticks(x[::1], fontsize=6, horizontalalignment='left', rotation=320)
# plt.yticks(np.arange(0, 360.0, 50), fontsize=8)
# plt.xlim(x[0], x[-1])
#
# # # Draw Tick lines
# # for y in np.arange(0, 150.0, 30):
# #     plt.hlines(y, xmin=0, xmax=len(x), colors='black', alpha=0.3, linestyles="--", lw=0.5)
#
# # Lighten borders
# plt.gca().spines["top"].set_alpha(0)
# plt.gca().spines["bottom"].set_alpha(.3)
# plt.gca().spines["right"].set_alpha(0)
# plt.gca().spines["left"].set_alpha(.3)
#
# plt.rcParams['figure.dpi'] = 600
# plt.rcParams['savefig.dpi'] = 600
# plt.tight_layout()
# plt.grid(axis="x", linestyle=":", linewidth=0.5)
# plt.savefig("./out/rank/f2.png")

# ddf.plot.bar(y=ddf.columns[1:], stacked=True)
#
# ax = plt.gca()
# ax.set_title('f3', fontsize=18)
# ax.legend(loc='best', fontsize=12, ncol=4)
# plt.xticks(fontsize=6, horizontalalignment='left', rotation=320)
# plt.yticks(np.arange(0, 360.0, 50), fontsize=8)
#
# plt.rcParams['figure.dpi'] = 600
# plt.rcParams['savefig.dpi'] = 600
# plt.tight_layout()
# plt.grid(axis="y", linestyle=":", linewidth=0.5)
# plt.savefig("./out/rank/f3.png")
