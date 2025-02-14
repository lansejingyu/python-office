#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: excel.py
# Mail: 1957875073@qq.com
# Created Time:  2022-4-25 10:17:34
# Description: 有关 excel 的自动化操作
#############################################

from faker import Faker
import pandas as pd
from alive_progress import alive_it

from utils import pandas_mem


def fake2excel(columns=('name',), rows=1, language='zh_CN', path='./fake2excel.xlsx'):
    """
    @Author & Date  : CoderWanFeng 2022/5/13 0:12
    @Desc  : columns:list，每列的数据名称，默认是名称
            rows：多少行，默认是1
            language：什么语言，可以填english，默认是中文
            path：输出excel的位置，有默认值
    """
    # 可以选择英语
    if language.lower() == 'english':
        language = 'en_US'
    # 开始造数
    fake = Faker(language)
    excel_columns = []
    for column in alive_it(columns):
        excel_columns.append([eval(f"fake.{column}()", {"fake": fake}) for _ in range(rows)])

    # 用pandas，将模拟数据，写进excel里面
    writer = pd.ExcelWriter(path)
    data = pd.DataFrame(excel_columns, index=columns).T
    try:
        data = pandas_mem.reduce_pandas_mem_usage(data)
    except AttributeError:  # without .dtype attribute
        pass
    data.to_excel(writer, index=False)
    writer.save()
