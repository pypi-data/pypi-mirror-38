import sqlite3
import csv
import os


def readcsvlist(filename, encoding):
    with open(filename, mode='r', encoding=encoding) as f:
        f_csv = csv.reader(f)
        content = [row for row in f_csv]
    return content


class CsvDB(object):
    def __init__(self):
        self.db = sqlite3.connect(':memory:')
        self.tables = []

    def addtable(self, csvfile, encoding='utf8'):
        content = readcsvlist(csvfile, encoding=encoding)
        tablename = ''.join(csvfile.split(os.path.sep)[-1].split('.')[:-1])
        row_length = len(content[0])
        fields = ['field_{} varchar(600)']*row_length
        indexes = list(range(1, row_length+1))
        fields = ','.join([f.format(i) for f, i in zip(fields, indexes)])
        sql = 'create table {}({});'.format(tablename, fields)
        self.db.execute(sql)

        self.db.executemany(
            'INSERT INTO {} VALUES ({})'.format(tablename, ','.join(['?']*row_length)),
            [tuple(r) for r in content]
        )

    def showtables(self):
        cur = self.db.cursor()
        cur.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name;')
        self.tables = [r for r in cur.fetchall()]
        return self.tables
