import csv
import os
import sqlite3

from zoran_tools.path_tools import create_father_dir


def readcsvgenerator(filename, encoding):
    """
    读取CSV文件为生成器
    """
    with open(filename, mode='r', encoding=encoding) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            yield row


def readcsvlist(filename, encoding):
    """
    读取CSV文件为列表
    """
    with open(filename, mode='r', encoding=encoding) as f:
        f_csv = csv.reader(f)
        content = [row for row in f_csv]
    return content
    

def readcsv(filename, encoding='utf8', li=True):
    '''
    接收一个CSV文件名, 返回其内容, 可能返回<list>也可能返回<generator>
    :param filename: <str> 要读取的CSV路径
    :param encoding:
    :param li: True or False, 指定返回的数据格式, 为True时返回列表, 为False时返回生成器
    :return:
    '''
    if li:
        return readcsvlist(filename, encoding)
    else:
        return readcsvgenerator(filename, encoding)


def write_csv(filename, li, quoting=csv.QUOTE_ALL):
    '''
    接收一个文件名(路径)和一个列表, 将列表写入该文件
    :param filename: <str> 要写入的文件名
    :param li: <list> 要写入的列表
    :param quoting: <csv.QUOTE_MINIMAL, csv.QUOTE_ALL, csv.QUOTE_NONNUMERIC, csv.QUOTE_NONE>
        csv.QUOTE_MINIMAL 仅当字段中包含分隔符时才用引号括起,
        csv.QUOTE_ALL 任何情况下都将字段用引号括起,
        csv.QUOTE_NONNUMERIC 括起非数字字段, 数字不括起,
        csv.QUOTE_NONE 不括起任何字段
    '''
    create_father_dir(filename)
    with open(file=filename, mode='a+', encoding='utf8', newline='') as f:
        sp = csv.writer(f, delimiter=',', quotechar='"', quoting=quoting)
        sp.writerow(li)


write_csv_row = write_csv


def write_csv_rows(filename, rows, quoting=True):
    """
    :param filename: <str> 要写入的文件名
    :param rows: <list> 要写入的所有行
    :param quoting: <csv.QUOTE_MINIMAL, csv.QUOTE_ALL, csv.QUOTE_NONNUMERIC, csv.QUOTE_NONE>
        csv.QUOTE_MINIMAL 仅当字段中包含分隔符时才用引号括起,
        csv.QUOTE_ALL 任何情况下都将字段用引号括起,
        csv.QUOTE_NONNUMERIC 括起非数字字段, 数字不括起,
        csv.QUOTE_NONE 不括起任何字段
    """
    create_father_dir(filename)
    if quoting is None:
        quoting = csv.QUOTE_NONE
    elif quoting == 'minimal':
        quoting = csv.QUOTE_MINIMAL
    elif quoting == 'nonnumeric':
        quoting = csv.QUOTE_NONNUMERIC
    else:
        quoting = csv.QUOTE_ALL

    with open(file=filename, mode='a+', encoding='utf8', newline='') as f:
        sp = csv.writer(f, delimiter=',', quotechar='"', quoting=quoting)
        sp.writerows(rows)


