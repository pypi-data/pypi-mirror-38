import csv
import os
import sqlite3

from .path_tools import create_father_dir


def readcsvgenerator(filename, encoding):
    with open(filename, mode='r', encoding=encoding) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            yield row


def readcsvlist(filename, encoding):
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


def write_csv_rows(filename, rows, quoting=True):
    '''
    :param filename: <str> 要写入的文件名
    :param rows: <list> 要写入的所有行
    :param quoting: <csv.QUOTE_MINIMAL, csv.QUOTE_ALL, csv.QUOTE_NONNUMERIC, csv.QUOTE_NONE>
        csv.QUOTE_MINIMAL 仅当字段中包含分隔符时才用引号括起,
        csv.QUOTE_ALL 任何情况下都将字段用引号括起,
        csv.QUOTE_NONNUMERIC 括起非数字字段, 数字不括起,
        csv.QUOTE_NONE 不括起任何字段
    '''
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


class CsvDB(object):
    def __init__(self, name=None, memory=':memory:'):
        if name:
            self.name = name
        self.db = sqlite3.connect(memory)
        self.table_dict = dict()

    def create_table(self, name, columns):
        """
        根据表名和字段在数据库中创建一个表
        :param name:
        :param columns:
        :return:
        """
        if name not in self.tables:
            sql = 'create table {}({});'.format(name, columns)
            self.db.execute(sql)
            return True
        else:
            return False

    def get_table(self, name=None, filename=None, content=None, fields=None, encoding='utf8'):
        table = Table(db=self, name=name, filename=filename, content=content, fields=fields, encoding=encoding)
        table.create()
        self.table_dict[table.name] = table
        return self

    def table(self, name):
        return self.table_dict[name]

    @property
    def tables(self, printit=False):
        sql = 'SELECT name FROM sqlite_master WHERE type="table" ORDER BY name;'
        tables = self.runsql(sql).fetchall()
        if printit:
            print(tables)
        return tables

    def runsql(self, sql):
        """
        运行SQL语句
        :param sql:
        :return:
        """
        return self.db.execute(sql)

    def run_insert(self, name, content):
        # 进行表插入
        self.db.executemany(
            'INSERT INTO {} VALUES ({})'.format(name, ','.join(['?']*len(content[0]))),
            [tuple(r) for r in content]
        )
        return len(content)


class Table(object):
    def __init__(self, db, name=None, filename=None, content=None, fields=None, encoding='utf8'):
        if (not name and not filename) or (not filename and not content):
            raise ValueError
        self.db = db
        self._name_ = name
        self._filename_ = filename
        self._content_ = content
        self._fields_ = fields
        self.encoding = encoding

    @property
    def name(self):
        if self._name_:
            return self._name_
        else:
            return self._filename_.split(os.sep)[-1].split('.')[0]

    @property
    def fields(self):
        if self._fields_:
            return self._fields_
        else:
            pat = '{}{} varchar(600)'
            row_length = len(self.content[0])
            if row_length == 0:
                raise ValueError
            indexes = list(range(1, row_length + 1))
            fields = ','.join([pat.format('field_', i) for i in indexes])
            return fields

    @property
    def content(self):
        if self._content_:
            return self._content_
        else:
            return readcsv(filename=self._filename_, encoding=self.encoding)

    def _create_(self):
        self.db.create_table(name=self.name, columns=self.fields)

    def _insert_(self):
        self.db.run_insert(name=self.name, content=self.content)

    def create(self):
        self._create_()
        self._insert_()

    def select_all(self):
        sql = 'select * from {};'.format(self.name)
        return self.db.runsql(sql).fetchall()
    