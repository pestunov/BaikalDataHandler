# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 10:40:45 2020

@author: Phil
"""

import pandas as pd
import numpy as np
import datetime as dt


PATH = r'./data/'
FILE = 'dec19hourly.csv'
FULLPATH = ''.join([PATH, FILE])
print(FULLPATH)
rowsToSkip = list(range(2,1000))
df = pd.read_csv(FULLPATH,
                 index_col='DateTime',
                 header=0,
                 skiprows=list(range(2,2000)),
                 na_values=['--'],
                 parse_dates=['DateTime'],
                 decimal=',',
                 usecols=['DateTime','vCO2air','PICARRO_CO2'],
                 nrows=1000,
                 )

df = df[df.index.notna()]

df['time'] = df.index.time

dr = pd.date_range(start=df.index.min().date(),
                   end=df.index.max().date()+dt.timedelta(days=1),
                   freq='H')[:-1].to_pydatetime()

