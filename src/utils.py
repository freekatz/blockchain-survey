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

from settings import *


def remove_chore(string: str) -> str:
    if len(string) <= 1 or type(string) is not str:
        return string
    s = string.strip()
    if s[0] == " " or s[0] == "-":
        s = s[1:]
    if s[-1] == " ":
        s = s[:-1]
    s = re.sub(r"\(.*\)", "", s)
    s = re.sub(r"\[(.*)]", "", s)
    return s


# todo update similar.txt
def similar_replace(string) -> str:
    words = re.split(",", string)
    similar_items = open(similar_replace_path, "r", encoding="utf-8").readlines()
    # print(similar_items)
    
    ws = words
    for item in similar_items:
        if "//" in item[:2]:
            continue
        i = 0
        item = item.strip()
        s_list = re.split("==", item)
        
        for w in words:
            if w != "" and w in s_list:
                ws[i] = s_list[0]
            
            i += 1
    s = ",".join(set(ws))
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


def df_rank(df: pd.DataFrame, col: str) -> dict:
    ddf = df.sort_values(col)
    rank = {}
    for topic, n in zip(ddf.index, ddf[col]):
        # if type(topic) is not str: continue
        rank[topic] = n
    
    return rank


def df_coincide(df: pd.DataFrame, cols: list, labels: list) -> pd.DataFrame:
    """
    
    :param labels:
    :param df:
    :param cols: the coincide of cols
    :return:
    """
    ddf = df[cols][~df.isin(labels)].dropna(axis=0)
    return df[df.index.isin(ddf.index)]


def isInter(a,b):
    result = list(set(a)&set(b))
    if result:
        return True
    else:
        return False


if __name__ == '__main__':
    pwd = output_root_dir + "/last"  # 获取文件目录
    target = output_root_dir + '/all-last.xlsx'
    try:
        os.remove(target)
    except:
        pass
    merge(pwd, target)
