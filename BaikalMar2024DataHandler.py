

import time
import datetime as dt

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import re

import sys
import myscifunc
import mytools
from mysecure import DB_BAIKAL_LOCAL_PASS, DB_BAIKAL_REMOTE_PASS, DB_BAIKAL_REMOTE_LOGIN


## reading data from db 
tableName = "mar2023"
SQL_PARAM_DICT = {# 'host': '192.168.3.49',
                  'host': '192.168.193.80',
                  'user': DB_BAIKAL_REMOTE_LOGIN,
                  'password': DB_BAIKAL_REMOTE_PASS,
                  'db': 'baikal',
                  'port': '3306'}
SQL_PARAM_DICT_LOC = {'host': 'localhost',
                      'user': 'root',
                      'password': DB_BAIKAL_LOCAL_PASS,
                      'db': 'baikal_origin',
                      'port': '3306'}

#link = mytools.connectBase1(**SQL_PARAM_DICT_LOC)
link = mytools.connectBase1(**SQL_PARAM_DICT)
req = "select * from {tn} where DateTime > ADDDATE((SELECT DATETIME FROM {tn}     ORDER BY DATETIME DESC LIMIT 1), INTERVAL -30 day);".format(tn=tableName)
raw = pd.read_sql(sql=req,
                  con=link,
                  parse_dates=['DateTime']
                  )
link.close()
print("Good! Link closed! Read {} rows".format(len(raw)))


'''
Convert datetime into unix time: sec from 1/1/1970
add col 'dateSec' for unix time
add col 'time' for time extracted from col 'datetime'
'''
raw.sort_values(by=['DateTime'], ascending=True)
raw['date_sec'] = raw['DateTime'].astype('int64')//10**9
#raw['time'] = pd.to_datetime(raw['DateTime'], unit = 's')
raw['time'] = raw['DateTime'].dt.time
raw['dt'] = (raw['date_sec'] - raw['date_sec'].shift(1))/60  # delta time, min


'''
Devices features, corrections coefficients
Filling empty cells (easy now)
'''

#corrections coefficients
temp_DS1_cor = (1, 0)
temp_DS2_cor = (1, 0)
temp_DS3_cor = (1, 0)
wtr_flow1_cor = (1, 0)
wtr_flow2_cor = (1, 0)
solar_cor = (0.011432, 0)
solar_uv_cor = (2.193e-04, 0)
air_flow1_cor = (1.035, 0.138)
press_cor = (1, 0)

equ_walltube_param = {'equ_vol': 0.8,  # equivalent equilibrator volume, l
                      'equ_cap': 0.2,  # equilibrator capacity -- water fraction that totally react with air
                     }    

equ_yellow_param = {'equ_vol': 10,  # equivalent equilibrator volume, l
                    'equ_cap': 0.2,  # equilibrator capacity
                   }


# In[6]:


''' cols sort / mix / fill '''

### to do: [ - ] function to smart fill empty cells
def filter_data(input_data, chnl = 'V1_state', order = 3):
    ''' i do not know how tot do that'''
#    input_data[input_data > 3] = np.nan
    input_data = _remove_after_trigger(input_data, chnl, order)
    return input_data

def _remove_after_trigger(input_data, chnl, order):
    ch = pd.DataFrame(raw[chnl])
    ch['ai'] = ch[chnl]*ch[chnl].shift(order)
    input_data[ch['ai'] != 1] = np.nan
    return input_data

def fill_empty_cell(input_data):
    '''fill NA in air gas concentrations columns by upward value'''
    return input_data.fillna(method='ffill', axis = 'index')

press_cn = 'AIR_PRESSURE'
t_equ_bot_cn = 'TEMP_DS1'
t_equ_sur_cn = 'TEMP_DS2'
wtrf_equ_bot_cn = 'WATER_FLOW_1'
wtrf_equ_sur_cn = 'WATER_FLOW_2'
airf_cn = 'AIR_FLOW'
t_air_cn = 'METEO_TEMP'
rh_air_cn = 'METEO_HUM'
water_level_cn = 'METEO_LEVEL'
solar_lin_cn = 'METEO_SOLAR'
solar_cn = 'LIGHT_LX'
solar_uv_cn = 'UV'
wind_speed_cn = 'METEO_WIND_SPEED'
wind_speed_max_cn = 'METEO_WIND_SPEED_MAX'
wind_dir_cn = 'METEO_WIND_DIR'
rain_cn = 'METEO_RAIN'
lat_cn = 'LATITUDE'
long_cn = 'LONGITUDE'
fluo_nxb_cn = 'NX_B'
fluo_nxg_cn = 'NX_G'
fluo_nxr_cn = 'NX_R'
fluo_kfab_cn = 'KFA_B'
fluo_kfag_cn = 'KFA_G'
fluo_kfar_cn = 'KFA_R'

air_chnl = 'V6_state'         # ambient atmosphere inlet channel
equ_bot_chnl = 'V1_state'     # equlibrator 1 inlet channel
equ_sur_chnl = 'V2_state'     # equlibrator 2 inlet channel

cor_k, cor_b = press_cor
press = raw[press_cn] * cor_k + cor_b
press = scifunc.pressConvert(press)

t_air = raw[t_air_cn]

cor_k, cor_b = temp_DS1_cor
t_equ_bot = raw[t_equ_bot_cn] * cor_k + cor_b

cor_k, cor_b = temp_DS2_cor
t_equ_sur = raw[t_equ_sur_cn] * cor_k + cor_b

# pop air concentrations

raw['vCO2_air'] = raw['PICARRO_CO2'][raw[air_chnl] == 1]
raw['vCH4_air'] = raw['PICARRO_CH4'][raw[air_chnl] == 1]

raw['flt1'] = raw[air_chnl]*raw[air_chnl].shift(4)

vCO2_air = raw['vCO2_air']
vCO2_air.loc[raw['flt1'] != 1] = np.nan
vCO2_air.loc[vCO2_air < 200] = np.nan
vCO2_air.loc[vCO2_air > 600] = np.nan
vCH4_air = raw['vCH4_air']
vCH4_air.loc[raw['flt1'] != 1] = np.nan
vCH4_air.loc[vCH4_air < 1] = np.nan
vCH4_air.loc[vCH4_air > 6] = np.nan

pCO2_air = vCO2_air * press / scifunc.NORM_PRESS
pCH4_air = vCH4_air * press / scifunc.NORM_PRESS

# test sizes
len(raw['vCO2_air']), len(vCO2_air), len(t_air), len(t_equ_sur)
vCO2_air[13020:13048], pCO2_air[13020:13048],
plt.figure(figsize=(20, 8))
plt.plot(raw['DateTime'], pCH4_air)


# In[7]:


''' 
Create medium dataframe, based on original raw data
Fill with computed data
Keep indexes quantity
'''

med = pd.DataFrame(raw['DateTime'])
med['Time'] = med['DateTime'].dt.time
med['vCO2_air'] = vCO2_air
med['pCO2_air'] = pCO2_air
med['vCH4_air'] = vCH4_air
med['pCH4_air'] = pCH4_air
med['Press'] = press
med['Tair'] = t_air

cols_list_to_copy = ['METEO_TEMP', 'METEO_HUM', 'METEO_LEVEL', 'METEO_SOLAR',
                     'METEO_WIND_SPEED', 'METEO_WIND_SPEED_MAX', 'METEO_WIND_DIR',
                     'METEO_RAIN',
                     'AIR_TEMPERATURE',
                     'LATITUDE', 'LONGITUDE',
                     'NX_B', 'NX_G', 'NX_R', 'KFA_B', 'KFA_G', 'KFA_R',
                     'PICARRO_CO2', 'PICARRO_CH4'
                    ]

for cn in cols_list_to_copy:
    med[cn] = raw[cn]


# In[8]:


'''
gas concentration in equilibrators recovery routines
'''
def recovery(vGas_equ, vGas_air, t_equ, press, air_flow, wtr_flow, equ_param, gas = 'co2', **kwarg):
    t_wtr_equ = t_air_equ = t_equ
    sol = scifunc.getSolubility(t_wtr_equ, gas)  #g/l
    density = scifunc.getDensity(t_air_equ, None, gas)
    pGas_equ = vGas_equ * press / scifunc.NORM_PRESS  # uatm
    cGas_equ = pGas_equ * density / 1000000  # g/l
    cGas_air = vGas_air * density * press / scifunc.NORM_PRESS / 1000000  # g/l
    equ_vol = equ_param['equ_vol']
    equ_cap = equ_param['equ_cap']
    
    tau = equ_vol / (air_flow + wtr_flow * equ_cap * sol / density)
    eternal = (cGas_equ - cGas_equ.shift(1) * np.exp(-1 * raw['dt'] / tau)) / (1 - np.exp(-1 * raw['dt'] / tau))
    cGas_wtr = (eternal * (wtr_flow * equ_cap * sol / density + air_flow) - air_flow * cGas_air) / (wtr_flow * equ_cap)
    return cGas_wtr, cGas_wtr * 1000000 / sol

vCO2_air = fill_empty_cell(vCO2_air)
vCH4_air = fill_empty_cell(vCH4_air)

# air flow thru eqilibrator. Common for all equ's
cor_k, cor_b = air_flow1_cor
air_flow = raw['AIR_FLOW'] * cor_k + cor_b
med['AIR_FLOW'] = air_flow

# 1. Bottom Walltube equilibrator
chnl = 'V1_state'    # channel for 'bottom' equ's

t_equ = t_equ_bot
t_air_equ = t_equ

cor_k, cor_b = wtr_flow1_cor
wtr_flow = raw[wtrf_equ_bot_cn] * cor_k + cor_b
med['wtr_flow_bot'] = wtr_flow
med['TwtrBot'] = t_equ_bot[wtr_flow > 2]

# 1.1 CO2 bottom
vGas_equ = raw['PICARRO_CO2'][raw[chnl] == 1]
med['cCO2_bot'], med['pCO2_bot'] = recovery(vGas_equ,
                                            vCO2_air, # take an eye on this
                                            t_equ, press, air_flow, wtr_flow,
                                            equ_walltube_param, gas = 'co2')
# 1.2 CH4 bottom
vGas_equ = raw['PICARRO_CH4'][raw[chnl] == 1]
med['cCH4_bot'], med['pCH4_bot'] = recovery(vGas_equ,
                                            vCH4_air, # take an eye on this
                                            t_equ, press, air_flow, wtr_flow,
                                            equ_walltube_param, gas = 'ch4')

# 2. Surface Walltube equilibrator
chnl = 'V2_state'    # channel for 'surface' equ's

t_equ = t_equ_sur
t_air_equ = t_equ

cor_k, cor_b = wtr_flow2_cor
wtr_flow = raw[wtrf_equ_sur_cn] * cor_k + cor_b
med['wtr_flow_sur'] = wtr_flow
med['TwtrSur'] = t_equ_sur[wtr_flow > 2]

# 1.1 CO2 bottom
vGas_equ = raw['PICARRO_CO2'][raw[chnl] == 1]
med['cCO2_sur'], med['pCO2_sur'] = recovery(vGas_equ,
                                            vCO2_air, # take an eye on this
                                            t_equ, press, air_flow, wtr_flow,
                                            equ_walltube_param, gas = 'co2')
# 1.2 CH4 bottom
vGas_equ = raw['PICARRO_CH4'][raw[chnl] == 1]
med['cCH4_sur'], med['pCH4_sur'] = recovery(vGas_equ,
                                            vCH4_air, # take an eye on this
                                            t_equ, press, air_flow, wtr_flow,
                                            equ_walltube_param, gas = 'ch4')

# 3. Surface Yellow equilibrator
chnl = 'V7_state'    # channel for 'surface' equ's
t_equ = 0.5  # there is not temperature sensor on yellow equ pipe 
t_air_equ = t_equ

# there is not waterflow sensor on yellow equ pipe
# fill the new col with data from dairie
raw['water_flow_yel'] = 0
raw.loc[raw['DateTime'] > pd.to_datetime('2021-03-28 11:30'), 'water_flow_yel'] = 8
raw.loc[raw['DateTime'] > pd.to_datetime('2021-03-29 16:37'), 'water_flow_yel'] = 11
raw.loc[raw['DateTime'] > pd.to_datetime('2021-03-29 17:30'), 'water_flow_yel'] = 7.8
wtr_flow = raw['water_flow_yel']
med['water_flow_yel'] = raw['water_flow_yel']

# 1.1 CO2 bottom
vGas_equ = raw['PICARRO_CO2'][raw[chnl] == 1]
med['cCO2_sur_yel'], med['pCO2_sur_yel'] = recovery(vGas_equ,
                                            vCO2_air, # take an eye on this
                                            t_equ, press, air_flow, wtr_flow,
                                            equ_walltube_param, gas = 'co2')
# 1.2 CH4 bottom
vGas_equ = raw['PICARRO_CH4'][raw[chnl] == 1]
med['cCH4_sur_yel'], med['pCH4_sur_yel'] = recovery(vGas_equ,
                                            vCH4_air, # take an eye on this
                                            t_equ, press, air_flow, wtr_flow,
                                            equ_walltube_param, gas = 'ch4')

med['pCH4_sur_yel'].mean(), med[['DateTime', 'pCO2_sur_yel']]


# In[9]:


plt.figure(figsize=(20, 8))
plt.plot(med['DateTime'], med['pCH4_sur'])


# In[10]:


coll = med.columns
print(list(coll))


# In[11]:


file = r'D:\1_Data1\86_BaikalMar2021\handled1.txt'
med.to_csv(file, sep = '\t')
#out.to_csv(file, sep = '\t')

