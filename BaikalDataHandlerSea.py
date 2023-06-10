import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.sql import text

import baikalfunctions as bfunc
import scheme_mar2023 as scheme


plt.style.use('dark_background')   # try another styles: 'classic'
plt.rcParams['figure.figsize'] = [15, 5]

saveImgPath = 'C:\\xampp\\htdocs\\img\\'

obrisData = "G:/1_Data1/obris/obris.dat"
obris = pd.read_csv(obrisData,
                    header=0,
                    na_values='--',
                    sep='\t',
                    decimal=',',
                    )

allMethaneData = "G:/1_Data1/sea/AllSeaGisOut.txt"
colNames = ['i', 'long', 'lat', 'cCH4wtr']
allMethane_df = pd.read_csv(allMethaneData,
                            index_col=0,
                            sep='\t',
                            skiprows=[0, 1, 2],
                            usecols=[0, 1, 2, 3],
                            header=None,
                            names=colNames,
                            )

# host = 192.168.3.53
host = 'localhost'
tableName = "jun2023sea"

engine = create_engine(f"mysql+pymysql://root:oceana1777@{host}:3306/baikal")
#req = f"select * from {tableName} where DateTime > ADDDATE((SELECT DATETIME FROM {tableName} ORDER BY " \
#      f"DATETIME DESC LIMIT 1), INTERVAL -24 hour);"
while True:
    req = f"select * from {tableName}"

    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(req))
    df = pd.DataFrame(query.fetchall())

    df.rename(columns=scheme.NAME_CONV_BAS, inplace=True)
    df.sort_values(by='DateTime', inplace=True)
    df.reset_index(inplace=True, drop=True)

    ## gether/apply specific variables
    ### data corrections
    df['vCO2'] = df['vCO2'] * scheme.CO2PicarroScaut_cor[0] + scheme.CO2PicarroScaut_cor[1]
    df['vCH4'] = df['vCH4'] * scheme.CH4PicarroScaut_cor[0] + scheme.CH4PicarroScaut_cor[1]
    df['LightLX'] = df['LightLX'] * scheme.solar_cor[0] + scheme.solar_cor[1]
    df['LightUV'] = df['LightUV'] * scheme.solar_uv_cor[0] + scheme.solar_uv_cor[1]
    df['PressAir'] = bfunc.pressConvert(df['PressAir'])
    df['PressAir'] = df['PressAir'] * scheme.press_cor[0] + scheme.press_cor[1]

    ### servise data corrections
    df['TempEqu1'] = df['TempEqu1'] * scheme.tempEqu1_cor_m[0] + scheme.tempEqu1_cor_m[1]
    df['TempEqu2'] = df['TempEqu2'] * scheme.tempEqu2_cor_m[0] + scheme.tempEqu2_cor_m[1]
    df['TempEqu3'] = df['TempEqu3'] * scheme.tempEqu3_cor_m[0] + scheme.tempEqu3_cor_m[1]

    df['AirFlow'] = df['AirFlow'] * scheme.airflow_cor_m[0] + scheme.airflow_cor_m[1]
    df['WaterFlowEqu1'] = df['WaterFlowEqu1'] * scheme.waterflowEqu1_cor_m[0] + scheme.waterflowEqu1_cor_m[1]
    df['WaterFlowEqu2'] = df['WaterFlowEqu2'] * scheme.waterflowEqu2_cor_m[0] + scheme.waterflowEqu2_cor_m[1]
    df['WaterFlowEqu3'] = df['WaterFlowEqu3'] * scheme.waterflowEqu3_cor_m[0] + scheme.waterflowEqu3_cor_m[1]


    chnl = 'channel'
    if not chnl in df.columns:
        df[chnl] = 0
    df[chnl] = 0
    df.loc[df.V1_state == 1, chnl] = 1
    df.loc[df.V2_state == 1, chnl] = 2
    df.loc[df.V3_state == 1, chnl] = 3
    df.loc[df.V4_state == 1, chnl] = 4
    df.loc[df.V5_state == 1, chnl] = 5
    df.loc[df.V6_state == 1, chnl] = 6

    ch_v = 'chn_valid'
    if not ch_v in df.columns:
        df[ch_v] = 1
    df[ch_v] = 1
    for deep in range(1, 7):
        df.loc[df[chnl] != df[chnl].shift(deep), ch_v] = 0


    df['vCO2air'] = df['vCO2'][(df['channel'] == 6) & (df[ch_v] == 1)]
    df['vCH4air'] = df['vCH4'][(df['channel'] == 6) & (df[ch_v] == 1)]
    df['vCO2air'].fillna(method='ffill', axis='index', inplace=True)
    df['vCH4air'].fillna(method='ffill', axis='index', inplace=True)
    df['pCO2air'] = df['vCO2air'] * df['PressAir']  # mkatm
    df['pCH4air'] = df['vCH4air'] * df['PressAir']  # mkatm


    plt.rcParams['figure.figsize'] = [15, 5]
    fig, axs = plt.subplots(2, 1)

    axs[0].set_title('CO2 air, ppm')
    axs[0].plot(df.DateTime, df['vCO2'], '-', c='dimgray')
    axs[0].plot(df.DateTime, df['vCO2air'], 'r-')

    axs[1].set_title('CH4 air, ppm')
    axs[1].set_ylim(1.75, 2.5)
    axs[1].plot(df.DateTime, df['vCH4'], '-', c='dimgray')
    axs[1].plot(df.DateTime, df['vCH4air'], 'b-')

    fig.savefig(saveImgPath+'cAir_vs_time.png')
    plt.close(fig)


    ## RECOVERY HERE !!!
    equ_vol = scheme.equ_seatube_param['equ_vol']  # equivalent equ volume, l
    equ_cap = scheme.equ_seatube_param['equ_cap']  # equilibrator capacity
    df['DateSec'] = df['DateTime'].astype('int64')//10**9
    df['dTSec'] = df['DateSec'] - df['DateSec'].shift(1)
    dt = df['dTSec'] / 60   ## delta time, min
    t_wtr = df['TempEqu1']
    t_air = t_wtr
    air_flow = df['AirFlow']
    wtr_flow = df['WaterFlowEqu1']


    ### CO2 water
    df['vCO2equ1'] = df['vCO2'][(df['channel'] == 1) & (df[ch_v] == 1)]
    solubility = bfunc.getSolubility(df['TempEqu1'], 'CO2')

    density = bfunc.getDensity(t_air, df['PressAir'], 'CO2')
    cGasAir = df['pCO2air'] / 1000000 * density
    pGasEquAir = df['vCO2equ1'] * df['PressAir']
    cGasEquAir = pGasEquAir * density / 1000000  # g/l

    tau = equ_vol/(air_flow+wtr_flow*equ_cap*solubility/density)
    eternal = (cGasEquAir-cGasEquAir.shift(1)*np.exp(-1*dt/tau))/(1-np.exp(-1*dt/tau))
    cGasWtr = (eternal*(wtr_flow*equ_cap*solubility/density+air_flow)-air_flow*cGasAir)/(wtr_flow*equ_cap)
    df['cCO2wtr'] = cGasWtr * 1000     # mg/l
    df['pCO2wtr'] = cGasWtr * 1000000 / solubility  # mkatm


    ### CH4 water
    df['vCH4equ1'] = df['vCH4'][(df['channel'] == 1) & (df[ch_v] == 1)]
    solubility = bfunc.getSolubility(df['TempEqu1'], 'CH4')

    density = bfunc.getDensity(t_air, df['PressAir'], 'CH4')
    cGasAir = df['pCH4air'] / 1000000 * density
    pGasEquAir = df['vCH4equ1'] * df['PressAir']
    cGasEquAir = pGasEquAir * density / 1000000  # g/l

    tau = equ_vol/(air_flow+wtr_flow*equ_cap*solubility/density)
    eternal = (cGasEquAir-cGasEquAir.shift(1)*np.exp(-1*dt/tau))/(1-np.exp(-1*dt/tau))
    cGasWtr = (eternal*(wtr_flow*equ_cap*solubility/density+air_flow)-air_flow*cGasAir)/(wtr_flow*equ_cap)
    df['cCH4wtr'] = cGasWtr * 1000000000    # ng/l
    df['pCH4wtr'] = cGasWtr * 1000000 / solubility  # mkatm

    for col in ['cCO2wtr', 'pCO2wtr', 'cCH4wtr', 'pCH4wtr']:
        df.loc[df[col] == np.inf, col] = np.nan
        df.loc[df[col] == -np.inf, col] = np.nan
        df.loc[df[col] <= 0, col] = np.nan

    df['pCO2'] = df['vCO2'] * df['PressAir']

    plt.rcParams['figure.figsize'] = [15, 5]
    fig, ax = plt.subplots()
    ## ax.set_xlim(pd.to_datetime('05.06.2023 18:00:00', dayfirst=True), pd.to_datetime('05.06.2023 19:00:00', dayfirst=True))
    ax.set_title('CO2 water, mkatm')
    ax.set_ylim(200, 600)
    ax.plot(df.DateTime, df['pCO2'], '-', c='dimgray')
    ax.plot(df.DateTime, df['pCO2wtr'], 'r-')
    ax.plot(df.DateTime, df['pCO2air'], 'b-')
    fig.savefig(saveImgPath+'pCO2wtr_vs_time.png')
    plt.close(fig)


    df['pCH4'] = df['vCH4'] * df['PressAir']

    plt.rcParams['figure.figsize'] = [15, 5]
    fig, ax = plt.subplots()
    ax.set_title('CH4 water, mkatm')
    # ax.set_xlim(pd.to_datetime('06.06.2023 10:00:00', dayfirst=True), pd.to_datetime('06.06.2023 19:00:00', dayfirst=True))
    ax.set_ylim(0, 100)
    ax.plot(df.DateTime, df['pCH4'], '-', c='dimgray')
    ax.plot(df.DateTime, df['pCH4wtr'], 'b-')
    fig.savefig(saveImgPath+'pCH4wtr_vs_time.png')
    plt.close(fig)


    df.dropna(axis='index', subset=['Longitude', 'Latitude', 'cCH4wtr'], inplace=True)

    cCH4lim = 700
    df.loc[df.cCH4wtr > cCH4lim, 'cCH4wtr'] = cCH4lim
    allMethane_df.loc[allMethane_df.cCH4wtr > cCH4lim, 'cCH4wtr'] = cCH4lim


    cCH4wtrlog_all = np.log(allMethane_df['cCH4wtr'])
    cCH4wtrlog = np.log(df['cCH4wtr'])

    plt.rcParams['figure.figsize'] = [10, 14]
    fig, ax = plt.subplots()
    #ax.set_xlim(106.2, 109.4)
    #ax.set_ylim(52, 55)

    ax.plot(obris['long'], obris['lat'], 'b-')
    ax.scatter(x='long', y='lat', c=cCH4wtrlog_all, s=60, marker='o', linewidth=0, cmap='rainbow', alpha=0.06, data=allMethane_df, )
    ax.scatter(df['Longitude'], df['Latitude'], c=cCH4wtrlog, s=30, marker='o', linewidth=0, cmap='rainbow', alpha=0.4,)
    fig.savefig(saveImgPath+'CH4wtrSpatialJun2023.png')
    plt.close(fig)

    ## Detailed color map

    cCH2lim_top = 700
    df.loc[df.cCH4wtr > cCH2lim_top, 'cCH4wtr'] = cCH2lim_top
    allMethane_df.loc[allMethane_df.cCH4wtr > cCH2lim_top, 'cCH4wtr'] = cCH2lim_top
    cCH2lim_bot = 0
    df.loc[df.cCH4wtr < cCH2lim_bot, 'cCH4wtr'] = np.NaN
    allMethane_df.loc[allMethane_df.cCH4wtr < cCH2lim_bot, 'cCH4wtr'] = np.NaN

    df.dropna(axis='index', subset=['Longitude', 'Latitude', 'cCH4wtr'], inplace=True)

    cCH4wtrlog_all = np.log(allMethane_df['cCH4wtr'])
    cCH4wtrlog = np.log(df['cCH4wtr'])

    plt.rcParams['figure.figsize'] = [10, 12]
    fig, ax = plt.subplots()

    d_lat_lim = 0.4  # +/- degree
    d_long_lim = 0.6  # +/- degree
    cur_coordinates = [float(df.tail(1).loc[:, 'Longitude']), float(df.tail(1).loc[:, 'Latitude'])]
    ax.set_xlim(cur_coordinates[0] - d_long_lim, cur_coordinates[0] + d_long_lim)
    ax.set_ylim(cur_coordinates[1] - d_lat_lim, cur_coordinates[1] + d_lat_lim)

    ax.plot(obris['long'], obris['lat'], 'b-')
    ax.scatter(x='long', y='lat', c=cCH4wtrlog_all, s=50, marker='o', linewidth=0, cmap='rainbow', alpha=0.1,
               data=allMethane_df, )
    ax.scatter(df['Longitude'], df['Latitude'], c=cCH4wtrlog, s=30, marker='o', linewidth=0, cmap='rainbow',
               alpha=0.4, )
    ax.scatter(cur_coordinates[0], cur_coordinates[1], c='white', s=30, marker='+', alpha=1,)
    fig.savefig(saveImgPath + 'CH4wtrSpatialJun2023_detailed.png', transparent=True)
    plt.close(fig)
    '''
    df.to_csv('1.txt')
    
    '''
    for _ in range(60):
        print('.', end='')
        time.sleep(10)
    print('!')