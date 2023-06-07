# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:11:35 2019

Empty File
@author: Phil
This is a data logger script. It takes data from various sources (s.a. UDP,
Serial etc. Anyones can write routines to handle their own data).
Data are collected in pandas dataframe to be written to database
for each minutes or any period you want)
"""

import socket
import time
import re
import pandas as pd

import mytools

def mfloat(input):
    return input

season = "jun2023sea"

sql_param_dict = {'host': 'localhost',
                  'user': 'root',
                  'password': 'oceana1777',
                  'db': 'baikal',
                  'port': '3306'}

state_list = ['V1_state', 'V2_state', 'V3_state',
              'V4_state', 'V5_state', 'V6_state',
              'V7_state', 'V8_state', 'V0_state']

#host = '192.168.0.14'
#host = '192.168.1.33'
host = '192.168.3.108'
port = 60000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1)
s.bind((host, port))

column_names_list = []
data = pd.Series()
cycleNum = 0
cycle = True

try:
    comport = serial.Serial(port="COM6",
                            baudrate=115200,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=0.1)
    print('Serial connected')
except serial.SerialException:
    print('Serial connection failed or already connected')
finally:
    pass

while cycle:
#    time.sleep(0.01)
    cycleNum += 1
    if cycleNum > 100:
        cycleNum = 0
    # Serial attemption
        try:
            line = comport.read(5000)
            line = str(line)
            lines = re.findall(r'METEO_\w+:[0-9\.-]+',line)
            for line in lines:
                line = re.split(':',line)
                if len(line) == 2:
                    if line[0] in data:
                        data[line[0]].append(float(line[1]))
                        print('s', sep='', end='')

                    else:
                        data[line[0]] = [float(line[1])]
                        print('S', sep='', end='')

        except:
            print('x', sep='', end='')
        finally:
            pass

# UDP attemption

    try:
        message, address = s.recvfrom(1024)
        #print('Data from address %s' % str(address))
        #print(address, message)
        message = str(message)
        message = re.sub(r'^(b\')', '', message)
#        message = re.sub(r'(\\r\\n\')$', '', message, 0, re.MULTILINE)
        message = re.sub(r'[\\r\\n\']', '', message, 0, re.MULTILINE)
        if re.search('=', message):
            message = re.split('=', message)#, maxsplit=0)
            if len(message) == 2:
                message[1]=re.sub(r'[^0-9\.\-]','',message[1])
                if message[0] in data:
                    try:
                        data[message[0]].append(float(message[1]))
                        print('.',sep='',end='')
                    except:
                        print('e',sep='',end='')
                else:
                    try:
                        data[message[0]] = [float(message[1])]
                        print(',', sep='',end='')
                    except:
                        print('e', sep='',end='')
    except socket.timeout:
        print('?', sep='', end='')

    state_changes = 0
    for item in state_list:
        if item in data:
            temp_list = pd.Series(data[item])
            state_changes = + temp_list.std()

    loctime = time.localtime()

#    if loctime.tm_sec == 0 or loctime.tm_sec == 30 or state_changes > 0:
    if loctime.tm_sec == 0 or state_changes > 0:
        time.sleep(1.001)
        # data line ready
        # create new dictionary to record to db
        res_data_dict = {'DateTime': time.strftime('%d.%m.%Y %H:%M:%S', loctime)}

        for item in data.index:
            ser = pd.Series(data[item])
            # print(item, ser.mean(), item+'_ER', ser.std())
            res_data_dict.update({item: ser.mean(), item + '_err': ser.std()})

        print(res_data_dict)
        link = mytools.connectBase1(**sql_param_dict)
        #cursor = link.cursor()

        mytools.writeDictToDB(myDict=res_data_dict,
                              cursor=link,
                              baseName='baikal',
                              tableName=season)
        link.close()
#       init variables
        res_data_dict = {}
        data = pd.Series()

#        cycle = False

