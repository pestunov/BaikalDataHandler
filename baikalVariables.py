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


MOB_NAME_CONV = {'date_time': 'DateTime',
                 'Pair': 'PressAir',
                 'pressure_air': 'PressAir',
                 'Tair': 'TempAir',
                 'temperature_air': 'TempAir',
                 'Hu': 'HumidityAir',
                 'solar_eye': 'LightLX',
                 'solar_uv': 'LightUV',
                 'Wind': 'WindSpeed',
                 'Fi': 'WindDir',
                 'latitude': 'Latitude',
                 'longitude': 'Longitude',
                 'temperature_equ_1': 'TempEqu1',
                 'temperature_equ_2': 'TempEqu2',
                 'temperature_equ_3': 'TempEqu3',
                 'water_flow_1': 'WaterFlowEqu1',
                 'water_flow_2': 'WaterFlowEqu2',
                 'water_flow_3': 'WaterFlowEqu3',
                 'flow_air': 'AirFlow',
                 'co2_picarro': 'vCO2',
                 'co2_picarro_min': 'vCO2min',
                 'co2_picarro_max': 'vCO2max',
                 'h2o_picarro': 'vH2O',
                 'ch4_picarro': 'vCH4',
                 'ch4_picarro_min': 'vCH4min',
                 'ch4_picarro_max': 'vCH4max',
                 }



GAS_INIT_COLS = {'co2': 'PICARRO_CO2', 'ch4': 'PICARRO_CH4'}
CHANNEL_COLS = {1: 'V1_state',
                2: 'V2_state',
                3: 'V3_state',
                4: 'V4_state',
                5: 'V5_state',
                6: 'V6_state',
                7: 'V7_state',
                8: 'V8_state',
                }
WATER_TEMP_COLS = {1: 'TEMP_DS1',
                   2: 'TEMP_DS2',
                   3: 'TEMP_DS3',
                   4: 'TEMP_DS4',
                   7: 'TEMP_DS1',
                   }
WATER_FLOW_COLS = {1: 'WATER_FLOW_1',
                   2: 'WATER_FLOW_2',
                   3: 'WATER_FLOW_3',
                   4: 'WATER_FLOW_4',
                   7: 'WATER_FLOW_7',
                   }

CO2PicarroScaut_cor = (0.961, 2.962)
CH4PicarroScaut_cor = (1.015, 0.003)

tempEqu1_cor = {"k": 1.0, "b": 0.45}

tempEqu2_cor = {"k": 1.0, "b": -0.2}

# Te_meteo sensors correction coefs
solar_cor = (0.011432, 0)
solar_uv_cor = (2.193e-04, 0)
press_cor = (1.0, 0)

# Mobile equipment corrections coefs
tempEqu1_cor_m = (1.0, 0.0)
tempEqu2_cor_m = (1.0, 0.0)
tempEqu3_cor_m = (1.0, 0.0)
waterflowEqu1_cor_m = (1.0, 0.0)
waterflowEqu2_cor_m = (1.0, 0.0)
waterflowEqu3_cor_m = (1.0, 0.0)
airflow_cor_m = (0.963, -0.121)  # changed 13.06.22. it was (1.035, 0.138)


# Equilibrators formfactor coefs
equ_walltube_param = {'equ_vol': 0.8,  # equivalent equilibrator volume, l
                      'equ_cap': 0.2,  # equilibrator capacity -- water fraction that totally react with air
                      'water_flow_min': 3,  # big error if lower, l/min
                     }

# actual 2021
#equ_seatube_param = {'equ_vol': 0.8,  # equivalent equilibrator volume, l
#                      'equ_cap': 0.25,  # equilibrator capacity -- water fraction that totally react with air
#                      'water_flow_min': 2,  # big error if lower, l/min
#                    }

# actual 2022
equ_seatube_param = {'equ_vol': 0.8,  # equivalent equilibrator volume, l
                      'equ_cap': 0.25,  # equilibrator capacity -- water fraction that totally react with air
                      'water_flow_min': 2,  # big error if lower, l/min
                    }


equ_yellow_param = {'equ_vol': 9.3,  # equivalent equilibrator volume, l
                    'equ_cap': 0.25,  # equilibrator capacity
                    'water_flow_min': 2,  # big error if lower, l/min
                   }

def test():
	pass

if __name__ == '__main__':
    test()
