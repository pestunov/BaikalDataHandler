# -*- coding: utf-8 -*-
"""
My tools set
Author: PestDima
Date of Creation: 17/12/2019

Pathes and tools to work with data files, data base
Format date and time from/to text, databeses timestamps

"""

import os
import sys
import re

import pymysql

from datetime import datetime

posibleDateTimeColName = ["datetime", "date_time"]
posibleDateTimeUTCColName = ["datetimeutc", "datetime_utc",
                             "date_time_utc", "utc"]
posibleDateColName = ["date", "дата"]
posibleTimeColName = ["time", "время"]
posibleNotesColName = ["notes", "comments", "coments", "коментарии"]
posibleDateTimeFormates = ["%d.%m.%Y %H:%M:%S", "%d.%m.%y %H:%M:%S",
                           "%d/%m/%Y %H:%M:%S", "%d/%m/%y %H:%M:%S",
                           "%Y-%m-%d %H:%M:%S", "%y-%m-%d %H:%M:%S",
                           "%d.%m.%Y %H:%M", "%d.%m.%y %H:%M",
                           "%d/%m/%Y %H:%M", "%d/%m/%y %H:%M",
                           "%Y-%m-%d %H:%M", "%y-%m-%d %H:%M"]


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def connectBase(**kwarg):
    """    Connect to database using 'pymysql' module
    input: dictionary contain 'host', 'user', 'password' and 'db' as database
    output: link to db
    """
    print("Connecting to DB using pymysql...")
    try:
        conn = pymysql.connect(host=kwarg.pop('host', 'localhost'),
                               user=kwarg.pop('user', 'user'),
                               password=kwarg.pop('password', 'password'),
                               db=kwarg.pop('db', 'database')
                               )
    except Exception:
        print("Connection fail")
        sys.exit()
    print("Connected!")
    return conn


def mySQLQuery(cursor, query):
    # print(f"query: {query}")
    query = re.sub(r'[,;\s]+$', '', query)
    query += ';'
    return cursor.execute(query)


def _insertDictToDB(datadict, cursor, basename, tablename):
    isdata = False
    sqlRequest = "insert ignore into {}.{}".format(basename, tablename)
    sqlRequest += " set DateTime = '{}';".format(_searchDateTime(datadict))
    mySQLQuery(cursor, sqlRequest)
    sqlRequest = "update {}.{} set ".format(basename, tablename)
    for keyss in set(datadict.keys()):
        if keyss.lower() in posibleDateTimeColName:
            continue
        if keyss.lower() in posibleDateTimeUTCColName:
            continue
        if keyss.lower() in posibleDateColName:
            continue
        if keyss.lower() in posibleTimeColName:
            continue
        if keyss.lower() in posibleNotesColName:
            sqlRequest += "Comments='{}', ".format(datadict[keyss])
            continue
        if is_float(datadict[keyss]):
            sqlRequest += "{}={}, ".format(keyss, datadict[keyss])
            isdata = True
            continue
    if isdata:
        sqlRequest = re.sub(r'[,\s]+$', '', sqlRequest)
        sqlRequest += " where DateTime = '{}';".format(_searchDateTime(datadict))
        mySQLQuery(cursor, sqlRequest)


def _searchDateTime(_dict):
    ar1 = []
    for el in _dict.keys():
        if el.lower() in posibleDateTimeColName:
            ar1.append(el)
    if len(ar1) >= 1:
        str_date_time = _dict[ar1[0]]
        if len(ar1) > 1:
            print('too many DateTime columns in the table')
        return _correctDateTimeStr(str_date_time)
    ar1 = []
    for el in _dict.keys():
        if el.lower() in posibleDateColName:
            ar1.append(el)
    ar2 = []
    for el in _dict.keys():
        if el.lower() in posibleTimeColName:
            ar2.append(el)
    if (len(ar1) >= 1) and (len(ar2) >= 1):
        str_date_time = "{} {}".format(_dict[ar1[0]], _dict[ar2[0]])
        return _correctDateTimeStr(str_date_time)
    str_date_time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    print("can't find any date columns. Use current date {}".format(str_date_time))
    return str_date_time


def _correctDateTimeStr(sampleStr):
    global posibleDateTimeFormates
    format1st = posibleDateTimeFormates[0]
    try:
        obj_date_time = datetime.strptime(sampleStr, format1st)
    except ValueError:
        for dtformat in posibleDateTimeFormates:
            try:
                obj_date_time = datetime.strptime(sampleStr, dtformat)
                posibleDateTimeFormates.remove(dtformat)
                posibleDateTimeFormates.insert(0, dtformat)
                print("DateTime {}, => {}".format(sampleStr, dtformat))
                break
            except ValueError:
                obj_date_time = datetime.now()
    res_str = datetime.strftime(obj_date_time, "%Y-%m-%d %H:%M:%S")
    return res_str


def _createTable(cols_list, cursor, baseName, tableName):
    sqlRequest = f"CREATE TABLE if not exists {baseName}.{tableName} (DateTime DATETIME \
    NOT NULL DEFAULT CURRENT_TIMESTAMP, "
    sqlRequest += " Comments VARCHAR(800) NULL DEFAULT NULL, "
    sqlRequest += " PRIMARY KEY (DateTime)) COLLATE='utf8mb4_bin'\
                    ENGINE = MyISAM;"
    mySQLQuery(cursor, sqlRequest)
    _addColsToBD(cols_list, cursor, baseName, tableName)


def _addColsToBD(cols_list, cursor, baseName, tableName):
    sqlRequest = f"show columns from {baseName}.{tableName};"
    mySQLQuery(cursor, sqlRequest)
    bd_cols_list = cursor.fetchall()
    bd_cols_list = list(elem[0] for elem in bd_cols_list)
    cols_list.append('DateTime')
    cols_list.append('Comments')
    cols_to_add = []
    for el in cols_list:
        if el not in bd_cols_list:
            cols_to_add.append(el)

    sqlRequest = "ALTER TABLE {}.{} ".format(baseName, tableName)
    for colName in cols_to_add:
        if colName == 'DateTime':
            sqlRequest += 'add DateTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, '
            continue
        if colName == 'Comments':
            sqlRequest += 'add Comments VARCHAR(800) NULL DEFAULT NULL, '
            continue
        if colName.lower() in posibleDateTimeColName:
            continue
        if colName.lower() in posibleDateTimeUTCColName:
            continue
        if colName.lower() in posibleDateColName:
            continue
        if colName.lower() in posibleTimeColName:
            continue
        if colName.lower() in posibleNotesColName:
            continue
        sqlRequest += "add {cn} FLOAT NULL DEFAULT NULL, ".format(cn=colName)
    mySQLQuery(cursor, sqlRequest)


def readFile(fullpath):
    ''' return list of each file's strings '''
    with open(fullpath, 'r') as file:
        f = file.read()
        res_list = f.split('\n')
    return res_list


def writeDictToDB(myDict, cursor, baseName, tableName):
    cols_list = list(myDict.keys())
    _createTable(cols_list, cursor, baseName, tableName)
    _insertDictToDB(myDict, cursor, baseName, tableName)


def getDictFilesSizebyMask(path, mask):
    res_files_list = dict()
    dir_files_list = os.listdir(path)   # list all files in path dir
    for f in dir_files_list:
        if (re.search(mask, f)):
            fsize = os.path.getsize(path+"\\"+f)
            f = f.lower()
            res_files_list[f] = fsize
    return res_files_list


def getFilesListbyMask(path, mask):
    res_files_list = []
    dir_files_list = os.listdir(path)   # list all files in path dir
    for f in dir_files_list:
        if (re.search(mask, f)):
            f = f.lower()
            res_files_list.append(f)
    return res_files_list


def insertFileToDB(file_path, cursor, basename, tablename, separator):
    data_list = readFile(file_path)
    print("Filling Data to Database.....")
    title = data_list.pop(0)
    title = re.sub(r'^[\s]+', '', title)
    title = re.sub(r'[\s]+$', '', title, 0, re.MULTILINE)
    title = re.sub(r'[^A-Za-z0-9А-Яа-я\s_]', '', title)
    title = re.sub(r'[ ]{2,}', ' ', title)  # substitute space sequence with 1
    title = re.split(separator, title)
    _createTable(title, cursor, basename, tablename)

    for data_line in data_list:
        if len(data_line) <= 5:
            continue
        data_line = re.sub(r'^[\s]+', '', data_line)
        data_line = re.sub(r'[\s]*$', '', data_line)
        if separator != ",":
            data_line = re.sub(r'[,]', '.', data_line)
        data_line = re.sub(r'(--)', 'NULL', data_line)
        data_line = re.sub(r'-[9]{4,}\.[09]+', 'NULL', data_line)  # 9999.00 re
        data_line = re.split(separator, data_line)
        data_dict = dict(zip(title, data_line))
        _insertDictToDB(data_dict, cursor, basename, tablename)
