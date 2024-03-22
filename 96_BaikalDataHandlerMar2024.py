#!/usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from sqlalchemy import create_engine
from sqlalchemy.sql import text

import baikalfunctions as bfunc
import scheme_mar2023 as scheme
import mytools
import mysecure

import time

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100

# pd.set_option('display.min_rows', 100)
plt.style.use('dark_background')   # try another styles: 'classic'
plt.rcParams['figure.figsize'] = [15, 5]
# plt.subplots_adjust(top=1, left=0, right=1, bottom=0)

saveImgPath = 'G:\\1_Data1\\96_BaikalMar2024\\'
saveDataPath = 'G:\\1_Data1\\96_BaikalMar2024\\'
serverPath = 'C:\\xampp\\htdocs\\img\\'

host = "192.168.3.53"
# host = 'localhost'
tableName = "mar2024"

engine = create_engine(f"mysql+pymysql://{mysecure.user}:{mysecure.password}@{host}:3306/baikal")
# req = f"select * from {tableName} where DateTime > ADDDATE((SELECT DATETIME FROM {tableName} ORDER BY DATETIME DESC LIMIT 1), INTERVAL -24 hour);"
req = f"select * from {tableName}"

while(True):
    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(req))


    df = pd.DataFrame(query.fetchall())

    df.rename(columns=scheme.NAME_CONV_BAS, inplace=True)
    df.sort_values(by='DateTime', inplace=True)
    df.reset_index(inplace=True, drop=True)

    ### remove service variables
    df.drop([x for x in df.columns if x.lower().endswith('err')], axis='columns', inplace=True, errors='ignore')
    df.drop([x for x in df.columns if x.lower().endswith('max')], axis='columns', inplace=True, errors='ignore')
    df.drop([x for x in df.columns if x.lower().endswith('min')], axis='columns', inplace=True, errors='ignore')
    df.drop([x for x in df.columns if x.lower().startswith('pump')], axis='columns', inplace=True, errors='ignore')
    df.drop(['HumidityAir', ], axis='columns', inplace=True, errors='ignore')

    # ### Correction data
    ## gether/apply specific variables
    ### data corrections
    df['LightLX'] = df['LightLX'] * scheme.solar_cor[0] + scheme.solar_cor[1]
    df['LightUV'] = df['LightUV'] * scheme.solar_uv_cor[0] + scheme.solar_uv_cor[1]
    df['PressAir'] = bfunc.pressConvert(df['PressAir'])
    df['PressAir'] = df['PressAir'] * scheme.press_cor[0] + scheme.press_cor[1]

    ### servise data corrections
    df['TempEqu1'] = df['TempEqu1'] * scheme.tempEqu1_cor[0] + scheme.tempEqu1_cor[1]
    df['TempEqu2'] = df['TempEqu2'] * scheme.tempEqu2_cor[0] + scheme.tempEqu2_cor[1]
    df['TempEqu3'] = df['TempEqu3'] * scheme.tempEqu3_cor[0] + scheme.tempEqu3_cor[1]

    df['AirFlow'] = df['AirFlow'] * scheme.airflow_cor[0] + scheme.airflow_cor[1]

    df['WaterFlowEqu1'] = df['WaterFlowEqu1'] * scheme.waterflowEqu1_cor[0] + scheme.waterflowEqu1_cor[1]
    df['WaterFlowEqu2'] = df['WaterFlowEqu2'] * scheme.waterflowEqu2_cor[0] + scheme.waterflowEqu2_cor[1]
    df['WaterFlowEqu3'] = df['WaterFlowEqu3'] * scheme.waterflowEqu3_cor[0] + scheme.waterflowEqu3_cor[1]

    chnl = 'Channel'
    if not chnl in df.columns:
        df[chnl] = 0
    if 'V1_state' in df.columns:
        df.loc[df.V1_state == 1, chnl] = 1
        df.loc[df.V2_state == 1, chnl] = 2
        df.loc[df.V3_state == 1, chnl] = 3
        df.loc[df.V4_state == 1, chnl] = 4
        df.loc[df.V5_state == 1, chnl] = 5
        df.loc[df.V6_state == 1, chnl] = 6

    v_state_list = list(scheme.CHANNEL_COLS.values())
    df.drop(v_state_list, inplace=True, errors='ignore')


    # ###  Remove bad data
    # List of accidental cases to filter data (see notes)
    filter_list = [{'date_start': '01.03.2024 00:00', 'date_stop': '19.03.2024 12:00', 'cols': [x for x in df.columns], 'fill_with': np.NaN},   # Picarro is not ready
                   {'date_start': '21.03.2024 15:26', 'date_stop': '21.03.2024 15:32', 'cols': ['TempEqu1', 'WaterFlowEqu1'], 'fill_with': np.NaN},   # Water flow meter replaced
                  ]

    for cycle in filter_list:
        for col in cycle['cols']:
            date_start = pd.to_datetime(cycle['date_start'], dayfirst=True)
            date_stop = pd.to_datetime(cycle['date_stop'], dayfirst=True)
            df.loc[(df['DateTime'] > date_start) & (df['DateTime'] < date_stop), col] = cycle['fill_with']


    cols = ['FluoNxRed', 'FluoNxGrn', 'FluoNxBlu', 'FluoKfaRed', 'FluoKfaGrn', 'FluoKfaBlu']
    for col in cols:
        df.loc[df[col] <= 0, col] = np.NaN

    cols = ['WaterFlowEqu1', 'WaterFlowEqu2', 'WaterFlowEqu3', 'WaterFlowEqu4', 'AirFlow']
    for col in cols:
        df.loc[df[col] <= 0, col] = np.NaN



    ch_v = 'Chn_valid'
    df[ch_v] = 1
    for deep in range(1, 7):
        df.loc[df[chnl] != df[chnl].shift(deep), ch_v] = 0

    ## Air concentration interpolate
    df['vCO2air'] = df['vCO2'][(df[chnl] == 6) & (df[ch_v] == 1)]
    df['vCH4air'] = df['vCH4'][(df[chnl] == 6) & (df[ch_v] == 1)]
    for col in ['vCO2air', 'vCH4air',]:
        df[col] = df[col].rolling(3).mean()

    df['vCO2air'].interpolate(method='values', inplace=True)
    df['vCH4air'].interpolate(method='values', inplace=True)  ## `time` method mb better
    df['pCO2air'] = df['vCO2air'] * df['PressAir']  # mkatm
    df['pCH4air'] = df['vCH4air'] * df['PressAir']  # mkatm
    df['pCO2'] = df['vCO2'] * df['PressAir']
    df['pCH4'] = df['vCH4'] * df['PressAir']

    # ## RECOVERY !!!

    df['DateSec'] = df['DateTime'].astype('int64') //10**9
    df['dTSec'] = df['DateSec'] - df['DateSec'].shift(1)
    dt = df['dTSec'] / 60   ## delta time, min
    ch_v = 'Chn_valid'

    # #### recovery `CO2/CH4`, channel `1` (bottom in mar 2024)
    equ_vol = scheme.equ_walltube_param['equ_vol']  # equivalent equ volume, l
    equ_cap = scheme.equ_walltube_param['equ_cap']  # equilibrator capacity
    wtr_flow_min = scheme.equ_walltube_param['water_flow_min']

    t_wtr = df['TempEqu1']
    t_air = t_wtr
    wtr_flow = df['WaterFlowEqu1']
    air_flow = df['AirFlow']

    ### CO2 water
    vGasEqu = df['vCO2'][(df[chnl] == 1) & (df[ch_v] == 1) & (wtr_flow > wtr_flow_min)]
    solubility = bfunc.getSolubility(t_wtr, 'CO2')
    density = bfunc.getDensity(t_air, df['PressAir'], 'CO2')
    cGasAir = df['pCO2air'] / 1000000 * density
    pGasEquAir = vGasEqu * df['PressAir']  # uatm
    cGasEquAir = pGasEquAir * density / 1000000  # g/l
    tau = equ_vol/(air_flow+wtr_flow*equ_cap*solubility/density)
    eternal = (cGasEquAir-cGasEquAir.shift(1)*np.exp(-1*dt/tau))/(1-np.exp(-1*dt/tau))
    cGasWtr = (eternal*(wtr_flow*equ_cap*solubility/density+air_flow)-air_flow*cGasAir)/(wtr_flow*equ_cap)
    df['cCO2bot'] = cGasWtr * 1000     # mg/l
    df['pCO2bot'] = cGasWtr * 1000000 / solubility  # mkatm

    ### CH4 water
    vGasEqu = df['vCH4'][(df[chnl] == 1) & (df[ch_v] == 1) & (wtr_flow > wtr_flow_min)]
    solubility = bfunc.getSolubility(t_wtr, 'CH4')
    density = bfunc.getDensity(t_air, df['PressAir'], 'CH4')
    cGasAir = df['pCH4air'] / 1000000 * density
    pGasEquAir = vGasEqu * df['PressAir']
    cGasEquAir = pGasEquAir * density / 1000000  # g/l
    tau = equ_vol/(air_flow+wtr_flow*equ_cap*solubility/density)
    eternal = (cGasEquAir-cGasEquAir.shift(1)*np.exp(-1*dt/tau))/(1-np.exp(-1*dt/tau))
    cGasWtr = (eternal*(wtr_flow*equ_cap*solubility/density+air_flow)-air_flow*cGasAir)/(wtr_flow*equ_cap)
    df['cCH4bot'] = cGasWtr * 1000000000    # ng/l
    df['pCH4bot'] = cGasWtr * 1000000 / solubility  # mkatm

    # #### recovery `CO2/CH4`, channel `2` (surface in mar 2024)
    t_wtr = df['TempEqu2']
    t_air = t_wtr
    wtr_flow = df['WaterFlowEqu2']

    ### CO2 water
    vGasEqu = df['vCO2'][(df[chnl] == 2) & (df[ch_v] == 1) & (wtr_flow > wtr_flow_min)]
    solubility = bfunc.getSolubility(t_wtr, 'CO2')
    density = bfunc.getDensity(t_air, df['PressAir'], 'CO2')
    cGasAir = df['pCO2air'] / 1000000 * density
    pGasEquAir = vGasEqu * df['PressAir']
    cGasEquAir = pGasEquAir * density / 1000000  # g/l
    tau = equ_vol/(air_flow+wtr_flow*equ_cap*solubility/density)
    eternal = (cGasEquAir-cGasEquAir.shift(1)*np.exp(-1*dt/tau))/(1-np.exp(-1*dt/tau))
    cGasWtr = (eternal*(wtr_flow*equ_cap*solubility/density+air_flow)-air_flow*cGasAir)/(wtr_flow*equ_cap)
    df['cCO2sur'] = cGasWtr * 1000     # mg/l
    df['pCO2sur'] = cGasWtr * 1000000 / solubility  # mkatm

    ### CH4 water
    vGasEqu = df['vCH4'][(df[chnl] == 2) & (df[ch_v] == 1) & (wtr_flow > wtr_flow_min)]
    solubility = bfunc.getSolubility(t_wtr, 'CH4')
    density = bfunc.getDensity(t_air, df['PressAir'], 'CH4')
    cGasAir = df['pCH4air'] / 1000000 * density
    pGasEquAir = vGasEqu * df['PressAir']
    cGasEquAir = pGasEquAir * density / 1000000  # g/l
    tau = equ_vol/(air_flow+wtr_flow*equ_cap*solubility/density)
    eternal = (cGasEquAir-cGasEquAir.shift(1)*np.exp(-1*dt/tau))/(1-np.exp(-1*dt/tau))
    cGasWtr = (eternal*(wtr_flow*equ_cap*solubility/density+air_flow)-air_flow*cGasAir)/(wtr_flow*equ_cap)
    df['cCH4sur'] = cGasWtr * 1000000000    # ng/l
    df['pCH4sur'] = cGasWtr * 1000000 / solubility  # mkatm

    ## rolling average is applied inplace. Be cafelly, run this cell **ONCE**

    for col in ['cCO2sur', 'cCO2bot', 'pCO2sur', 'pCO2bot', 'cCH4sur', 'pCH4sur', 'cCH4bot', 'pCH4bot']:
        df.loc[df[col] == np.inf , col] = np.nan
        df.loc[df[col] == -np.inf , col] = np.nan
        df.loc[df[col] <= 0 , col] = np.nan
        df[col] = df[col].rolling(4, center=True).mean()

    # ## Generate charts for server
    count_recent = 30000

    plt.rcParams['figure.figsize'] = [15, 4]
    fig, ax = plt.subplots()
    ax.set_title('CO2, mkatm')
    ax.set_ylim(100, 600)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2'], '-', c='#444', alpha=0.3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2sur'], 'g.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2bot'], 'r.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2air'], 'c.', alpha=0.3, markersize=2)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m %H:%M'))
    fig.savefig(serverPath+'pCO2wtr_vs_time.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 960
    plt.rcParams['figure.figsize'] = [5, 4]
    fig, ax = plt.subplots()
    ax.set_title('CO2, mkatm')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2'], '-', c='#888', alpha=0.3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2sur'], 'g.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2bot'], 'r.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCO2air'], 'c.', alpha=0.3, markersize=2)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    fig.savefig(serverPath+'pCO2wtr_vs_time_3h.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 30000
    plt.rcParams['figure.figsize'] = [15, 4]
    fig, ax = plt.subplots()
    ax.set_title('CH4, mkatm')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4'], '-', c='#444', alpha=0.3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4bot'], 'r.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4sur'], 'g.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4air'], 'c.', alpha=0.3, markersize=3)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m %H:%M'))
    fig.savefig(serverPath+'pCH4wtr_vs_time.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 960
    plt.rcParams['figure.figsize'] = [5, 4]
    fig, ax = plt.subplots()
    ax.set_title('CH4, mkatm')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4'], '-', c='#888', alpha=0.3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4bot'], 'r.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4sur'], 'g.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['pCH4air'], 'c.', alpha=0.3, markersize=3)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    fig.savefig(serverPath+'pCH4wtr_vs_time_3h.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 30000
    plt.rcParams['figure.figsize'] = [15, 4]
    fig, ax = plt.subplots()
    ax.set_title('temp water, grad C')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['TempEqu1'], 'r.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['TempEqu2'], 'g.', alpha=0.3, markersize=3)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m %H:%M'))
    fig.savefig(serverPath+'tempWtr_vs_time.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 30000
    plt.rcParams['figure.figsize'] = [15, 4]
    fig, ax = plt.subplots()
    ax.set_title('Water flow, l/min')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['WaterFlowEqu1'], 'r.', alpha=0.3, markersize=3)
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['WaterFlowEqu2'], 'g.', alpha=0.3, markersize=3)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m %H:%M'))
    fig.savefig(serverPath + 'waterFlow_vs_time.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 30000
    plt.rcParams['figure.figsize'] = [15, 4]
    fig, ax = plt.subplots()
    ax.set_title('Solar, W/m2')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['LightLX'], 'r.', alpha=0.3, markersize=3)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m %H:%M'))
    fig.savefig(serverPath + 'Solar_vs_time.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 30000
    plt.rcParams['figure.figsize'] = [15, 4]
    fig, ax = plt.subplots()
    ax.set_title('SeaLevel, mm')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['METEO_LEVEL'], 'r.', alpha=0.3, markersize=3)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m %H:%M'))
    fig.savefig(serverPath + 'SeaLevel_vs_time.png', bbox_inches='tight')
    plt.close(fig=fig)

    count_recent = 30000
    plt.rcParams['figure.figsize'] = [15, 4]
    fig, ax = plt.subplots()
    ax.set_title('Pressure, mm Hg')
    ax.plot(df.tail(count_recent).DateTime, df.tail(count_recent)['PressAir']*760, 'r.', alpha=0.3, markersize=3)
    ax.grid(True, c='#555', alpha=0.8, linewidth=1, linestyle='--')
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m %H:%M'))
    fig.savefig(serverPath + 'PressAir_vs_time.png', bbox_inches='tight')
    plt.close(fig=fig)

    for _ in range(1799, -1, -1):
        print('\b\b\b\b', sep='', end='')
        print(_, sep='', end='')
        time.sleep(1)
    print('!', sep='')
    time.sleep(1)