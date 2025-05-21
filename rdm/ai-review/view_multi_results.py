#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
查看多文件处理结果
"""

import pandas as pd

# 读取结果文件
df = pd.read_excel('员工访问统计_多文件.xlsx')

# 打印结果
print(df)
