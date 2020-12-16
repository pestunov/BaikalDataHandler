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

<<<<<<< HEAD
=======
# read and parse csv file
>>>>>>> 0b96cdc43cad653360a621cb3e0934e5c01fee09
df = pd.read_csv(FULLPATH,
                 index_col='DateTime',
                 header=0,
                 skiprows=list(range(2, 2000)),
                 na_values=['--'],
                 parse_dates=['DateTime'],
                 decimal=',',
                 usecols=['DateTime', 'vCO2air', 'PICARRO_CO2'],
                 nrows=1000,  # remove after debugin
                 )

# comment if not debug
df = df[df.index.notna()]

# sort dataframe by datetime
# df.sort_values(by='DateTime', inplace=True)

# add "time" column
df['time'] = df.index.time

# create date range from first day thru last one
dr = pd.date_range(start=df.index.min().date(),
                   end=df.index.max().date()+dt.timedelta(days=1),
                   freq='30T')[:-1].to_pydatetime()

dfh = pd.DataFrame()
# building statistic tables from source data

for ii in range(2, len(dr)-2, 2):
    print(dr[ii-1], ' = ', dr[ii], ' = ', dr[ii+1])
#    dft = df.loc[dr[ii-1]:dr[ii+1],['vCO2air']]

# dr = dr.astype(str)
# yy = df[dr[45]:dr[46]].mean()

# dfh = df.resample(dr).mean()
