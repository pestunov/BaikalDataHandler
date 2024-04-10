"""
    Variables for BALO (shore and mobile)
    started: March 2023 shore campaign
    edited: June 2023
    """

""" chart_index -- chart number on page
    index_x -- col index for x-axis
    caption_x -- x-axis caption
    unit_x -- x-axis units caption
    index_y -- col index for y-axis
    caption_y -- y-axis caption
    unit_y -- y-axis units caption
    is_datetime -- 1: date or 0: num ???
    chart_type --  'dot', 'line', 'polygon'
    chart_size -- petit, 3+ grand
    chart_color -- any color name
"""

NAME_CONV_BAS = {'date_time': 'DateTime',
                 'DATETIME': 'DateTime',
                 'Pair': 'PressAir',
                 'pressure_air': 'PressAir',
                 'AIR_PRESSURE': 'PressAir',
                 'Tair': 'TempAir',
                 'temperature_air': 'TempAir',
                 'AIR_TEMPERATURE': 'TempAir',
                 'relative_humidity_air': 'HumidityAir',
                 'AIR_HUMIDITY': 'HumidityAir',
                 'Hu': 'HumidityAir',
                 'solar_eye': 'LightLX',
                 'LIGHT_LX': 'LightLX',
                 'solar_uv': 'LightUV',
                 'UV': 'LightUV',
                 'Wind': 'WindSpeed',
                 'Fi': 'WindDir',
                 'precipitation': 'Precipitation',
                 'RAIN': 'Precipitation',
                 'latitude': 'Latitude',
                 'LATITUDE': 'Latitude',
                 'longitude': 'Longitude',
                 'LONGITUDE': 'Longitude',
                 'temperature_equ_1': 'TempEqu1',
                 'EKV_1_TEMP': 'TempEqu1',
                 'TEMP_DS1': 'TempEqu1',
                 'temperature_equ_2': 'TempEqu2',
                 'EKV_2_TEMP': 'TempEqu2',
                 'TEMP_DS2': 'TempEqu2',
                 'temperature_equ_3': 'TempEqu3',
                 'EKV_3_TEMP': 'TempEqu3',
                 'TEMP_DS3': 'TempEqu3',
                 'temperature_ds_1': 'TempEqu1',
                 'temperature_ds_2': 'TempEqu2',
                 'temperature_ds_3': 'TempEqu3',
                 'temperature_ds_4': 'TempEqu4',
                 'water_flow_1': 'WaterFlowEqu1',
                 'WATER_FLOW_1': 'WaterFlowEqu1',
                 'water_flow_2': 'WaterFlowEqu2',
                 'WATER_FLOW_2': 'WaterFlowEqu2',
                 'water_flow_3': 'WaterFlowEqu3',
                 'WATER_FLOW_3': 'WaterFlowEqu3',
                 'water_flow_4': 'WaterFlowEqu4',
                 'WATER_FLOW_4': 'WaterFlowEqu4',
                 'flow_air': 'AirFlow',
                 'AIR_FLOW': 'AirFlow',
                 'co2_picarro': 'vCO2',
                 'picarro_co2': 'vCO2',
                 'PICARRO_CO2': 'vCO2',
                 'CO2_dry': 'vCO2',
                 'PICARRO_CO2_err': 'vCO2Err',
                 'co2_picarro_min': 'vCO2min',
                 'co2_picarro_max': 'vCO2max',
                 'ch4_picarro': 'vCH4',
                 'picarro_ch4': 'vCH4',
                 'PICARRO_CH4': 'vCH4',
                 'CH4_dry': 'vCH4',
                 'PICARRO_CH4_err': 'vCH4Err',
                 'ch4_picarro_min': 'vCH4min',
                 'ch4_picarro_max': 'vCH4max',
                 'h2o_picarro': 'vH2O',
                 'picarro_h2o': 'vH2O',
                 'PICARRO_H2O': 'vH2O',
                 'PICARRO_H2O_err': 'vH2OErr',
                 'speed': 'Speed',
                 'SPEED': 'Speed',
                 'course': 'Course',
                 'COURSE': 'Course',
                 'channel': 'Channel',
                 'fluo_nx_red': 'FluoNxRed',
                 'NX_R': 'FluoNxRed',
                 'fluo_nx_green': 'FluoNxGrn',
                 'NX_G': 'FluoNxGrn',
                 'fluo_nx_blue': 'FluoNxBlu',
                 'NX_B': 'FluoNxBlu',
                 'fluo_kfa_red': 'FluoKfaRed',
                 'KFA_R': 'FluoKfaRed',
                 'fluo_kfa_green': 'FluoKfaGrn',
                 'KFA_G': 'FluoKfaGrn',
                 'fluo_kfa_blue': 'FluoKfaBlu',
                 'KFA_B': 'FluoKfaBlu',
                 'comment': 'Comments'

                 }

cols2db_list = ['dateSec', 'pCO2_bot', 'pCO2_sur', 'pCO2_air', 'TEMP_DS3', 'AIR_PRESSURE']

scheme_cols = ['chart_index',
               'index_x', 'index_y',
               'is_datetime',
               'chart_type', 'chart_size', 'chart_color',
               'caption_x', 'caption_y',
               ]
scheme_l = [
    [0, 0, 1, 1, 'dot', 2, 'red', 'DateTime', 'vCO2_bot'],
    [0, 0, 2, 1, 'dot', 2, 'blue', '', 'vCO2_sur'],
    [0, 0, 3, 1, 'dot', 2, 'cyan', '', 'vCO2_air, mkatm'],
    [1, 0, 4, 1, 'dot', 2, 'red', 'DateTime', 'Twtr_bot'],
    [1, 0, 4, 1, 'dot', 2, 'blue', '', 'Twtr_sur, grad'],
]

names = {'prs': 'AIR_PRESSURE',
         'press': 'AIR_PRESSURE'}


GAS_INIT_COLS = {'co2': 'PICARRO_CO2',
                 'ch4': 'PICARRO_CH4',
                 }

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

# Te_meteo sensors correction coefs
solar_cor = (0.011432, 0)
solar_uv_cor = (2.193e-04, 0)
press_cor = (1.0, 0)    # actual for `Atm` units

# BALO equipment corrections coefs
tempEqu1_cor = (1.0, 0.45)
tempEqu2_cor = (1.0, -0.2)
tempEqu3_cor = (1.0, 0.0)       # need corrections
waterflowEqu1_cor = (1.0, 0.0)  # need corrections
waterflowEqu2_cor = (1.0, 0.0)  # need corrections
waterflowEqu3_cor = (1.0, 0.0)  # need corrections
airflow_cor = (0.963, -0.121)   # need corrections


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
                      'equ_cap': 0.4,  # equilibrator capacity -- water fraction that totally react with air
                      'water_flow_min': 3,  # big error if lower, l/min
                      }

# actual 2022
equ_seatube_param = {'equ_vol': 0.8,  # equivalent equilibrator volume, l
                     'equ_cap': 0.25,  # equilibrator capacity -- water fraction that totally react with air
                     'water_flow_min': 2,  # big error if lower, l/min
                     }

equ_yellow_param = {'equ_vol': 9.3,  # equivalent equilibrator volume, l
                    'equ_cap': 0.25,  # equilibrator capacity
                    'water_flow_min': 2,  # big error if lower, l/min
                    }

### Geo values

intersects = {1: ('MRT', 'SLZ'),
              2: ('TOL', 'SNZ'),
              3: ('LST', 'TNH'),
              4: ('KDL', 'MSH'),
              5: ('KYA', 'KHR'),
              6: ('GLY', 'KKY'),
              7: ('ANG', 'SUH'),
              8: ('VRT', 'BLD'),
              9: ('UHN', 'TNK'),
              10: ('IZM', 'LSV'),
              11: ('HBY', 'KRS'),
              12: ('SOL', 'USH'),
              13: ('ZVR', 'SOS'),
              14: ('ELH', 'DAV'),
              15: ('CHR', 'KBN'),
              16: ('MUJ', 'URB'),
              17: ('KOT', 'AMN'),
              18: ('BKL', 'TRL'),
              19: ('TYA', 'NMN'),
              }

shore_points = {'MRT': (51.78577, 104.2187),
                'SLZ': (51.5020, 104.23098),
                'TOL': (51.7886, 104.6142),
                'SNZ': (51.4795, 104.6225),
                'LST': (51.8401, 104.8861),
                'TNH': (51.5659, 105.1352),
                'KDL': (51.916, 105.224),
                'MSH': (51.6437, 105.5295),
                'KYA': (52.4184, 105.8793),
                'KHR': (52.2732, 106.2526),
                'GLY': (52.5627, 106.1882),
                'KKY': (52.3643, 106.4414),
                'ANG': (52.7738, 106.5823),
                'SUH': (52.5629, 107.1321),
                'VRT': (52.9968, 106.9362),
                'BLD': (52.5965, 107.2894),
                'UHN': (53.0731, 107.4076),
                'TNK': (52.7169, 107.6569),
                'IZM': (53.2333, 107.7357),
                'LSV': (53.0997, 108.2587),
                'HBY': (53.4117, 107.7930),
                'KRS': (53.3013, 108.6380),
                'SOL': (54.0123, 108.2477),
                'USH': (53.8644, 108.6331),
                'ZVR': (54.2956, 108.5005),
                'SOS': (54.1836, 109.5274),
                'ELH': (54.5384, 108.6623),
                'DAV': (54.3680, 109.4713),
                'CHR': (54.6124, 108.7431),
                'KBN': (54.6233, 109.5046),
                'MUJ': (54.8508, 108.9124),
                'URB': (54.7874, 109.6234),  # cape Urbikan (Urbikan river mouth (54.8121, 109.6432))
                'KOT': (55.0386, 109.1098),
                'AMN': (55.0497, 109.7726),
                'BKL': (55.3568, 109.1998),
                'TRL': (55.2888, 109.7589),
                'TYA': (55.6012, 109.3482),
                'NMN': (55.5403, 109.8162),
                }


points = {'12km KLT': (51.6776, 103.8712),
          'mid IVA_MUR': (51.6467, 104.4306),
          'mTSG': (51.6066, 104.7331),
          '7km BKT': (51.8429, 105.1030),
          'vlk BIG': (51.8764, 105.5480),
          'vlk SML': (51.9197, 105.6383),
          'md PES': (52.2318, 105.8016),
          'mind BGL': (52.4743, 106.1156),
          '7km IZM': (53.1937, 107.8054),
          'mid MMR': (53.242, 107.2259),
          'out MMR': (53.4436, 107.6734),
          'out BRG': (53.4030, 108.5527),
          'mBRG': (53.4523, 108.7395),
          'mACR': (53.6322, 108.1234),
          'mCHV': (53.7491, 109.1264),
          'md ZVR_SOS': (54.2824, 108.7399),
          '7km NZA': (55.7174, 109.6249),
          'mid GLY_KKY': (52.469, 106.2914),
          '3km DAV': (54.3795, 109.4233),
          'BALO': (51.900, 105.064),
          }