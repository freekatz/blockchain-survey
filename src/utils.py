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
import pandas as pd
import os

def merga():
    # 将文件读取出来放一个列表里面
    
    pwd = './out/tf/'  # 获取文件目录
    
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
    df = pd.concat(dfs)
    
    # 写入excel文件，不包含索引数据
    df.to_excel('./out/tf/all.xlsx', index=False)
    
if __name__ == '__main__':
    merga()