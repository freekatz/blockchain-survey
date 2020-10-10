#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   utils.py    
@Desc    :   
@Project :   src
@Contact :   1uvu.zhang@gmail.com
@License :   (C)Copyright 2018-2020, 1UVU.COM
@WebSite :   1uvu.com
@Modify Time           @Author        @Version
------------           -------        --------
2020/08/14 19:30       1uvu           1.0         
"""
import nltk.stem as ns
import pandas as pd
import numpy as np
import os
import re


def remove_chore(string) -> str:
    s = re.sub(r"\(.*\)", "", string.strip())
    s = re.sub(r"\[.*\]", "", s)
    return s


def similar_replace(string) -> str:
    words = re.split(",", string)
    similar_items = open("./res/similar.txt", "r", encoding="utf-8").readlines()
    # print(similar_items)
    
    ws = words
    for item in similar_items:
        if item[0] == "#": continue
        i = 0
        item = item.strip()
        s_list = re.split("==", item)
        
        for w in words:
            if w in s_list:
                ws[i] = s_list[0]
            
            i += 1
    
    s = ",".join(ws)
    return s


def stem(string, lemmatizer: ns.WordNetLemmatizer) -> str:
    if string == "pos": return string
    words = re.split(" ", string)
    
    ws = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, 'n')
        ws.append(lemma)
    
    s = " ".join([lemmatizer.lemmatize(word, 'v') for word in ws])
    return s


def merge(pwd: str, target: str):
    # 将文件读取出来放一个列表里面
    # 新建列表，存放文件名
    file_list = []
    
    # 新建列表存放每个文件数据(依次读取多个相同结构的Excel文件并创建DataFrame)
    dfs = []
    
    for root, dirs, files in os.walk(pwd):  # 第一个为起始路径，第二个为起始路径下的文件夹，第三个是起始路径下的文件。
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)  # 使用os.path.join(dirpath, name)得到全路径
            df = pd.read_excel(file_path)  # 将excel转换成DataFrame
            dfs.append(df)
    
    # 将多个DataFrame合并为一个
    df = pd.concat(dfs, sort=False)
    
    # 写入excel文件，不包含索引数据
    df.to_excel(target, index=False)


def drop_nan(df: pd.DataFrame) -> pd.DataFrame:
    ddf = df.dropna().drop(axis=0, index=["nothing", "nan"])
    return ddf

def df_rank(df: pd.DataFrame, col: str) -> dict:
    ddf = df.sort_values(col)
    rank = {}
    for topic, n in zip(ddf.index, ddf[col]):
        # if type(topic) is not str: continue
        rank[topic] = n
        
    return rank


def df_coincide(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    
    :param df:
    :param cols: the coincide of cols
    :return:
    """
    ddf = df[cols][~df.isin(["0"])].dropna()
    df = df[df.index.isin(ddf.index)]
    return df

if __name__ == '__main__':
    pwd = './out/tmp/'  # 获取文件目录
    target = './out/all-2.xlsx'
    merge(pwd, target)
