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

nameAliases =  {'datetime': 'DateTime',
                'date': 'Date',
                'time': 'Time',
                'pressure': 'PressAir',
                'press': 'PressAir',
                'prs': 'PressAir',
                'pair': 'PressAir',
                'pressureair': 'PressAir',
                'airpressure': 'PressAir',
                'pressair': 'PressAir',
                'tair': 'TempAir',
                'temperatureair': 'TempAir',
                'airtemperature': 'TempAir',
                'tempair': 'TempAir',
                # 'temp': 'TempAir',
                'relativehumidity': 'HumidityAir',
                'airhumidity': 'HumidityAir',
                'hu': 'HumidityAir',
                'rh': 'HumidityAir',
                'solareye': 'LightLX',
                'lightlx': 'LightLX',
                'solarradiationflow': 'LightLX',
                'solaruv': 'LightUV',
                'uv': 'LightUV',
                'wind': 'WindSpeed',
                'fi': 'WindDir',
                'precipitation': 'Precipitation',
                'rain': 'Precipitation',
                'lat': 'Latitude',
                'latitude': 'Latitude',
                'lon': 'Longitude',
                'long': 'Longitude',
                'longitude': 'Longitude',

                'ekv1temp': 'TempEqu1',
                'tempds1': 'TempEqu1',
                'temperatureequ1': 'TempEqu1',
                'temperatureds1': 'TempEqu1',
                'ekv2temp': 'TempEqu2',
                'tempds2': 'TempEqu2',
                'temperatureequ2': 'TempEqu2',
                'temperatureds2': 'TempEqu2',
                'ekv3temp': 'TempEqu3',
                'tempds3': 'TempEqu3',
                'temperatureequ3': 'TempEqu3',
                'temperatureds3': 'TempEqu3',
                'ekv4temp': 'TempEqu4',
                'tempds4': 'TempEqu4',
                'temperatureequ4': 'TempEqu4',
                'temperatureds4': 'TempEqu4',
                
                'waterflow1': 'WaterFlow1',
                'waterflow2': 'WaterFlow2',
                'waterflow3': 'WaterFlow3',
                'waterflow4': 'WaterFlow4',
                'waterflowequ1': 'WaterFlow1',
                'waterflowequ2': 'WaterFlow2',
                'waterflowequ3': 'WaterFlow3',
                'waterflowequ4': 'WaterFlow4',

                'flowair': 'AirFlow',
                'airflow': 'AirFlow',
                'co2picarro': 'vCO2',
                'picarroco2': 'vCO2',
                'co2dry': 'vCO2',
                'ch4picarro': 'vCH4',
                'picarroch4': 'vCH4',
                'ch4dry': 'vCH4',
                'h2opicarro': 'vH2O',
                'picarroh2o': 'vH2O',
                'speed': 'Speed',
                'course': 'Course',
                'channel': 'Channel',
                'fluonxred': 'FluoNxRed',
                'nxr': 'FluoNxRed',
                'fluonxgreen': 'FluoNxGrn',
                'nxg': 'FluoNxGrn',
                'fluonxblue': 'FluoNxBlu',
                'nxb': 'FluoNxBlu',
                'fluokfared': 'FluoKfaRed',
                'kfar': 'FluoKfaRed',
                'fluokfagreen': 'FluoKfaGrn',
                'kfag': 'FluoKfaGrn',
                'fluokfablue': 'FluoKfaBlu',
                'kfab': 'FluoKfaBlu',
                'comment': 'Comments',
                'cco2air': 'cCO2air',
                'pco2air': 'pCO2air',
                'vco2air': 'vCO2air',
                'cch4air': 'cCH4air',
                'pch4air': 'pCH4air',
                'vch4air': 'vCH4air',
                'cco2wtr': 'cCO2wtr',
                'pco2wtr': 'pCO2wtr',
                'vco2wtr': 'vCO2wtr',
                'cch4wtr': 'cCH4wtr',
                'pch4wtr': 'pCH4wtr',
                'vch4wtr': 'vCH4wtr',
                'cco2sur': 'cCO2sur',
                'pco2sur': 'pCO2sur',
                'vco2sur': 'vCO2sur',
                'cch4sur': 'cCH4sur',
                'pch4sur': 'pCH4sur',
                'vch4sur': 'vCH4sur',
                'cco2bot': 'cCO2bot',
                'pco2bot': 'pCO2bot',
                'vco2bot': 'vCO2bot',
                'cch4bot': 'cCH4bot',
                'pch4bot': 'pCH4bot',
                'vch4bot': 'vCH4bot',
                'cco2all': 'cCO2all',
                'pco2all': 'pCO2all',
                'vco2all': 'vCO2all',
                'cch4all': 'cCH4all',
                'pch4all': 'pCH4all',
                'vch4all': 'vCH4all',
                'dpco2': 'dpCO2',
                'dpch4': 'dpCH4',               
               }

def convert_names(colnames: list) -> list:
    res = []
    for name in colnames:
        _name = name.replace('_','')
        _name = _name.replace('-','')
        _name = _name.lower()
        if _name in nameAliases.keys():
            name = (nameAliases[_name])
        res.append(name)
    return res
    
temy4dbNames=['Date', 'Time', 'DateUTC', 'TimeUTC', 'latitude', 'longitude', 'speed', 'course', 'solar_altitude', 'solar-azimuth',
       'temperature_air', 'pressure_air', 'relative-humidity_air', 'precipitation', 'solar_eye', 'solar_uv',
       'co2_picarro', 'co2_picarro_max', 'co2_picarro_min', 'ch4_picarro', 'ch4_picarro_max', 'ch4_picarro_min', 'h2o_picarro', 'co2_licor', 'h2o_licor', 'o2_water', 'o2_water_temperature',
       'ph', 'temperature_water', 'temperature_equ_1', 'temperature_equ_2', 'temperature_equ_3', 'temperature_equ_4', 'flow_water', 'flow_air', 'channel', 'flag',
       'fluo_nx_red', 'fluo_nx_green', 'fluo_nx_blue', 'fluo_kfa_red', 'fluo_kfa_green', 'fluo_kfa_blue', # 'comment',
       'water_flow_1', 'water_flow_2', 'water_flow_3', 'water_flow_4',
       'temperature_ds_1', 'temperature_ds_2', 'temperature_ds_3', 'temperature_ds_4', 'temperature_ds_5', 'temperature_ds_6', 'temperature_ds_7'
      ]

cols2db_list = ['dateSec', 'pCO2_bot', 'pCO2_sur', 'pCO2_air', 'TEMP_DS3', 'AIR_PRESSURE']

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
                   7: 'TEMP_DS7',
                   }

WATER_FLOW_COLS = {1: 'WATER_FLOW_1',
                   2: 'WATER_FLOW_2',
                   3: 'WATER_FLOW_3',
                   4: 'WATER_FLOW_4',
                   7: 'WATER_FLOW_7',
                   }

CO2PicarroScaut_cor = (0.961, 2.962)
CH4PicarroScaut_cor = (1.015, 0.003)

# tempEqu1_cor = {"k": 1.0, "b": 0.45}
# tempEqu2_cor = {"k": 1.0, "b": -0.2}

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
points = {
    'MRT': (51.7858, 104.2187),
    'SLZ': (51.5020, 104.2310),
    'TOL': (51.7886, 104.6142),
    'SNZ': (51.4795, 104.6225),
    'LST': (51.8479, 104.8710),  # corrected 21/12/2024
    'TNH': (51.5659, 105.1352),
    'KDL': (51.9160, 105.2240),
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
    'MUJ': (54.8603, 108.9041),  # corrected 21/12/2024
    'URB': (54.7874, 109.6234),  # cape Urbikan (Urbikan river mouth (54.8121, 109.6432))
    'KOT': (55.0386, 109.1098),
    'AMN': (55.0497, 109.7726),
    'BKL': (55.3568, 109.1998),
    'TRL': (55.2888, 109.7589),
    'TYA': (55.6012, 109.3482),
    'NMN': (55.5403, 109.8162),
    '12km KLT': (51.6776, 103.8712),
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

def get_coor(name):
    return points[name]  

def get_center(a_b):
    a = get_coor(a_b[0])
    b = get_coor(a_b[1])
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    
intersects = {
    2: ('MRT', 'SLZ'),
    3: ('LST', 'TNH'),
    4: ('KDL', 'MSH'),
    6: ('KYA', 'KHR'),
    7: ('ANG', 'SUH'),
    8: ('VRT', 'BLD'),
    9: ('UHN', 'TNK'),
    11: ('HBY', 'KRS'),
    13: ('SOL', 'USH'),
    14: ('ZVR', 'SOS'),
    15: ('ELH', 'DAV'),
    16: ('CHR', 'KBN'),
    17: ('MUJ', 'URB'),
    18: ('KOT', 'AMN'),
    19: ('BKL', 'TRL'),
    20: ('TYA', 'NMN'),
}

central = {
    1: ('12km KLT', '12km KLT'),
    2: ('MRT', 'SLZ'),
    2.3: ('mid IVA_MUR', 'mid IVA_MUR'),
    2.7: ('mTSG', 'mTSG'),  ## nearest most visited
    3: ('LST', 'TNH'),
    4: ('KDL', 'MSH'),
    4.5: ('vlk SML', 'vlk SML'),
    5: ('md PES', 'md PES'),
    6: ('KYA', 'KHR'),
    6.5: ('mid GLY_KKY', 'mid GLY_KKY'),
    7: ('ANG', 'SUH'),
    8: ('VRT', 'BLD'),
    9: ('UHN', 'TNK'),
    10: ('7km IZM', '7km IZM'),
    11: ('HBY', 'KRS'),
    12: ('mACR', 'mACR'),
    13: ('SOL', 'USH'),
    14: ('md ZVR_SOS', 'md ZVR_SOS'),
    15: ('ELH', 'DAV'),
    16: ('CHR', 'KBN'),
    16.5: ('MUJ', 'URB'),
    17: ('KOT', 'AMN'),
    18: ('BKL', 'TRL'),
    19: ('TYA', 'NMN'),
    20: ('7km NZA', '7km NZA'),
}

