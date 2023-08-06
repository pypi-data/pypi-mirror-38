#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import numpy as np
import pandas as pd
from demo_project_test_time.test_module.test_main import abc

df = pd.DataFrame({"id": [1001, 1002, 1003, 1004, 1005, 1006],
                   "date": pd.date_range('20130102', periods=6),
                   "city": ['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
                   "age": [23, 44, 54, 32, 34, 32],
                   "category": ['100-A', '100-B', '110-A', '110-C', '210-A', '130-F'],
                   "price": [1200, np.nan, 2133, 5433, np.nan, 4432]},
                  columns=['id', 'date', 'city', 'category', 'age', 'price'])


def test():
    print("hello world!")
    print('The time is:', time.time())
    print(df.shape)
    abc()


if __name__ == '__main__':
    test()
