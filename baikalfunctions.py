# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:41:57 2021

@author: Phil
"""

import pandas as pd
import numpy as np

IDEAL_GAS_MOLAR_VOLUME = 22.4           # l/mol
NORM_PRESS = 101325                     # Pa
NORM_TEMP_K = 273.13                    # grad K
R = 8.314462                            # J/(mol*K)
MOLAR_MASS = {'co2': 44, 'ch4': 16}     # g/mol

R_EARTH = 6372.795                      # Earth radius, km


def dist(a, b):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees,
    [0] - long,
    [1] - lat)
    """
    x1, y1, x2, y2 = map(np.radians, [a[0], a[1], b[0], b[1]])
    dx = x2 - x1
    dy = y2 - y1
    a = np.sin(dy/2)**2 + np.cos(y1) * np.cos(y2) * np.sin(dx/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    # Earth`s radius in kilometers
    km = R_EARTH * c
    return km


def geo_my_dist(a, b) -> dict:
    """
    Calculate the distance between two points
    on the earth (specified in decimal degrees)
    """
    lat1, long1, lat2, long2 = a[0], a[1], b[0], b[1]
    dlat = lat2 - lat1
    dlong = long2 - long1
    xx = 2 * math.pi * R_EARTH * dlat / 360
    yy = 2 * math.pi * R_EARTH * math.cos((lat1+lat2) / 2 / 180 * math.pi) * dlong / 360
    dist = math.sqrt(xx * xx + yy * yy)
    return {'dist': dist,
            'a_1km': (lat1+dlat/dist*1, long1+dlong/dist*1),
            'a_3km': (lat1+dlat/dist*3, long1+dlong/dist*3),
            'a_5km': (lat1+dlat/dist*5, long1+dlong/dist*5),
            'a_7km': (lat1+dlat/dist*7, long1+dlong/dist*7),
            'mid': (lat1+dlat/2, long1+dlong/2),
            'b_1km': (lat2-dlat/dist*1, long2-dlong/dist*1),
            'b_3km': (lat2-dlat/dist*3, long2-dlong/dist*3),
            'b_5km': (lat2-dlat/dist*5, long2-dlong/dist*5),
            'b_7km': (lat2-dlat/dist*7, long2-dlong/dist*7),
            }


def geo_gen_stations() -> dict:
    geo = {}
    for k, val in scheme.intersects.items():
        intersect = geo_my_dist(scheme.shore_points[val[0]], scheme.shore_points[val[1]])
        geo['3km ' + val[0]] = intersect['a_3km']
        geo['7km ' + val[0]] = intersect['a_7km']
        geo['mid ' + val[0] + '_' + val[1]] = intersect['mid']
        geo['7km ' + val[1]] = intersect['b_7km']
        geo['3km ' + val[1]] = intersect['b_3km']
    geo.update(scheme.points)
    return geo


def pressConvert(press):
    """ Convert input value to pressure [Pa]
    ranges of input values:
        0..3 -> bar
        3..300 -> kPa
        300..2000 -> mmHg
        >2000 -> Pa
    """

    try:
        press_ref = press.mean()
    except AttributeError:
        press_ref = press

    if press_ref <= 3:  # press in atm
        return press * bv.NORM_PRESS
    if press_ref <= 300:  # press in kPa
        return press * 1000
    if press_ref <= 2000:  # press in mmHg """
        return press * bv.NORM_PRESS/760
    if press_ref > 50000:  # press in Pa
        return press
    print('pressConvert: unknown press format')
    return press


def temperatureConvert(temp):
    """ Convert input value to temperature [K]
    ranges of input values:
        -200..200 -> grad C
        >200 -> grad K
    """

    try:
        temp_mean = temp.mean()
    except AttributeError:
        temp_mean = temp

    if temp_mean <= 200:  # temp in grad C
        return temp + bv.NORM_TEMP_K
    if temp_mean > 200:  # temp in grad K
        return temp


def getSolubility(temp, gas='CO2'):
    """ calculate gas solubility in water [g/l]
    input:
    temp - water temperature in degree of Celcius
    gas - str of gase's name, default 'CO2', [CH4]
    output:
    float number means solubility as Vol of gas per Vol of water  g/l
    """
    try:
        molar_mass = bv.MOLAR_MASS[gas.lower()]
    except KeyError:
        print('getSolubility: wrong gas identification')
        return 0
    norm_density = molar_mass/bv.IDEAL_GAS_MOLAR_VOLUME

    _temp = temperatureConvert(temp)
    _temp -= bv.NORM_TEMP_K  # to gradC
    if gas.lower() == 'co2':
        return (0.1588+1.528*np.exp(-_temp/26.598))*norm_density
    if gas.lower() == 'ch4':
        return (0.0194+0.038*np.exp(-_temp/21.873))*norm_density
    else:
        print('wrong gas identification')
    return None


def getDensity(temp, press, gas='CO2'):
    """ calculate gas density [g/l]
    input:
    temp - gas temperature in degree of Celcius
    press - air pressure, Pa
    gas - str of gase's name, default 'CO2', [CH4]
    output:
    float number means density [g/l]"""
    if press is None:
        _press = bv.NORM_PRESS
    else:
        _press = pressConvert(press)

    _temp = temperatureConvert(temp)
    try:
        molar_mass = bv.MOLAR_MASS[gas.lower()]
    except KeyError:
        print('2wrong gas identification')
        return 0
    res = molar_mass/bv.IDEAL_GAS_MOLAR_VOLUME * \
        _press/bv.NORM_PRESS * bv.NORM_TEMP_K/_temp
    return res


def equToWtrRecovery(df,
                     chnl=1,
                     out_col_name='defName',
                     gas='CO2',
                     equ_type='equ_2020'):
    """ add columns to df with names 'c'+DefName and 'p'+DefName filled with
    recovered values in [g/l] and [uatm] accordingly """
    try:
        equ_gas_init_col = bv.GAS_INIT_COLS[gas.lower()]
        wtr_temp = WATER_TEMP_COLS[chnl]
        wtr_flow = WATER_FLOW_COLS[chnl]
    except KeyError:
        print('wrong gas identification')
        return 0

    vGasEqu = df[equ_gas_init_col][df[CHANNEL_COLS[chnl]] == 1]
    vGasAir = df[equ_gas_init_col][df[CHANNEL_COLS[CHNL_AIR]] == 1]

    wtrtemp = df[wtr_temp]
    airtemp = df[wtr_temp]
    df['_tempwf'] = df[wtr_flow][df[wtr_flow] >= EQU_PARAM[equ_type]['water_flow_min']]
    wtrflow = df['_tempwf']*1

    dt = 1  # ******************* time delta to int of minutes ****************

    equ_vol = EQU_PARAM[equ_type]['equ_vol']  # equivalent equ volume, l
    equ_eff = EQU_PARAM[equ_type]['equ_eff']  # equilibrator capacity
    print('{} {}'.format(equ_vol, equ_eff))


    air_flow_k = 1.035
    air_flow_b = 0.138
    air_flow = df['AIR_FLOW']*air_flow_k+air_flow_b

    solubility = getSolubility(wtrtemp, gas)
    density = getDensity(airtemp, None, gas)
    press = pressConvert(df[PRESS_COL])

    cGasAir = vGasAir.median()*0.000001*density*press/NORM_PRESS  # g/l

    pGasEqu = vGasEqu*press/NORM_PRESS
    cGasEqu = pGasEqu*density*0.000001  # g/l

    tau = equ_vol/(air_flow+wtrflow*equ_eff*solubility/density)
    eternal = (cGasEqu-cGasEqu.shift(1)*np.exp(-1*dt/tau))/(1-np.exp(-1*dt/tau))
    cGasWtr = (eternal*(wtrflow*equ_eff*solubility/density+air_flow)-air_flow*cGasAir)/(wtrflow*equ_eff)
    temp_col_name = 'c'+out_col_name
    df[temp_col_name] = cGasWtr
    print(temp_col_name)
    temp_col_name = 'p'+out_col_name
    df[temp_col_name] = cGasWtr*1000000/solubility
    print(temp_col_name)

def test():
    # test solubility
    for _ in range(0,30,1):
        print('{:.1f}\t{:.4f}\t{:.4f}'.format(_,
              getSolubility(_, 'cO2'),
              getSolubility(_, 'ch4')), end=' ')
        a = getDensity(temp=_, press=760, gas='ch4')
        print('{:.2f}'.format(a))

if __name__ == '__main__':
    test()
    s = getSolubility(3,'ch4')
