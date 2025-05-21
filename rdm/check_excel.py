#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
检查Excel文件结构
"""

import pandas as pd

# 读取IP信息Excel文件
df = pd.read_excel('IP信息.xlsx')

# 打印列名和前几行数据
print("列名:", df.columns.tolist())
print("\n前5行数据:")
print(df.head())
