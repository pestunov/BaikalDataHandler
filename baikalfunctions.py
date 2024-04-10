# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:41:57 2021

@author: Phil
"""

import pandas as pd
import numpy as np

IDEAL_GAS_MOLAR_VOLUME = 22.4          # l/mol
NORM_PRESS = 101325                     # Pa
NORM_TEMP_K = 273.13                    # grad K
R = 8.314462                            # J/(mol*K)
MOLAR_MASS = {'co2': 44, 'ch4': 16}     # g/mol

R_EARTH = 6371.0088  # (2 * R_Equator + 1 * R_Pole) / 3


class Baikalfunctions:

    def __init__(self):
        self.temperature = None
        self.pressure = None

    def pressConvert(self):
        """ Convert input value to pressure [atm]
        ranges of input values:
            0..3 -> atm
            3..300 -> kPa
            300..2000 -> mmHg
            >2000 -> Pa
        """

        try:
            press_ref = press.mean()
        except AttributeError:
            press_ref = press

        if press_ref <= 2:  # press in atm
            return press
        if press_ref <= 200:  # press in kPa
            return press * 1000 / physic.NORM_PRESS
        if press_ref <= 2000:  # press in mmHg """
            return press / 760
        if press_ref > 50000:  # press in Pa
            return press / physic.NORM_PRESS
        print('pressConvert: unknown press format')
        return press


""" add columns to df with names 'c'+DefName and 'p'+DefName filled with
    recovered values in [g/l] and [uatm] accordingly """

def equToWtrRecovery(datetime, v_gas_equ, v_gas_air, t_wtr, press, v_air, v_wtr, equ_param, gas_type='CO2'):
    # !!!
    dt = datetime.shift(1) - datetime  # time delta to int of minutes
    equ_vol = equ_param['equ_vol']  # equivalent equ volume, l
    equ_eff = equ_param['equ_eff']  # equilibrator capacity
    print('Equ volume = {}, equ capasity = {}'.format(equ_vol, equ_eff))

    sol = getSolubility(t_wtr, gas_type)
    t_air = t_wtr
    # !!!
    den = getDensity(t_air, None, gas_type)
    press = pressConvert(press)

    # !!!
    cGasAir = vGasAir.median()*0.000001*density*press  # g/l

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


def interpolatee(df, colname):
    ''' Fill skipped data '''
    if str(type(df.index)) == "<class 'pandas.core.indexes.datetimes.DatetimeIndex'>":
        method = 'time'
    else:
        method = 'linear'
    return df[colname].interpolate(method=method, axis='index', inplace=False)


def pressConvert(press):
    """ Convert input value to pressure [atm]
    ranges of input values:
        0..3 -> atm
        3..300 -> kPa
        300..2000 -> mmHg
        >2000 -> Pa
    """

    try:
        press_ref = press.mean()
    except AttributeError:
        press_ref = press

    if press_ref <= 2:  # press in atm
        return press
    if press_ref <= 200:  # press in kPa
        return press * 1000 / physic.NORM_PRESS
    if press_ref <= 2000:  # press in mmHg """
        return press / 760
    if press_ref > 50000:  # press in Pa
        return press / physic.NORM_PRESS
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
        return temp + physic.NORM_TEMP_K
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
        molar_mass = physic.MOLAR_MASS[gas.lower()]
    except KeyError:
        print('getSolubility: wrong gas identification')
        return 0
    norm_density = molar_mass/physic.IDEAL_GAS_MOLAR_VOLUME

    _temp = temperatureConvert(temp)
    _temp -= physic.NORM_TEMP_K  # to gradC
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
    press - air pressure, atm
    gas - str of gases name, default 'CO2', [CH4]
    output:
    float number means density [g/l]"""
    if press is None:
        _press = 1
    else:
        _press = pressConvert(press)

    _temp = temperatureConvert(temp)
    try:
        molar_mass = physic.MOLAR_MASS[gas.lower()]
    except KeyError:
        print('wrong gas identification')
        return None
    return molar_mass/physic.IDEAL_GAS_MOLAR_VOLUME * \
           _press * physic.NORM_TEMP_K/_temp


def get_len(x, y):
    return np.sqrt(x * x + y * y)


def get_ang(x: float, y: float) -> any:
    length = get_len(x, y)
    if length == 0:
        return None
    ang = np.atan2(x, -y) * 180 / math.pi
    return (ang + 270) % 360


def navigate(lat_cur: float, long_cur: float, lat_goal: float, long_goal: float) -> tuple:
    d_lat = lat_goal - lat_cur
    d_long = long_goal - long_cur
    lat_dist = d_lat * dist_1deg
    long_dist = d_long * dist_1deg * math.cos(lat_cur)
    dist = get_len(lat_dist, long_dist)
    direct = get_ang(lat_dist, long_dist)
#    print(dist, direct)
    return direct, dist



def mtest():
    # test solubility
    for tt in range(0, 30, 1):
        print('{:.1f}\t{:.4f}\t{:.4f}'.format(tt,
              getSolubility(tt, 'cO2'),
              getSolubility(tt, 'ch4')), end=' ')
        a = getDensity(temp=tt, press=760, gas='ch4')
        print('{:.2f}'.format(a))


if __name__ == '__main__':
    mtest()
    pass
