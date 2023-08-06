from .zoran_tools import regtest
from .db_tools import *
from .path_tools import *



@regtest
def test_read_SQLite_table():
    sqls = ['select * from test limit 1;', None]
    fields = ['*', ['name'], 'name, age']
    for sql in sqls:
        for field in fields:
            print('--------------{}----------{}---------------------------------'.format(field, sql))
            result = read_SQLite_table(db='test.db', table='test', sql=sql, field=field,)
            for r in result:
                print(r)


@regtest
def test_showtables():
    tables = showtables('test.db')
    print(tables)


@regtest
def test_list_files():
    print('list_files输出文件名', list_files())
    print('list_files输出文件路径', list_files(abspath=True))


@regtest
def test_create_father_dir():
    filename = os.path.sep.join([os.getcwd(), 'test_create_dir', 'test.py'])
    fatherpath = os.path.dirname(filename) + os.path.sep 
    path = Path(fatherpath)
    if path.is_dir():
        os.removedirs(fatherpath)
    create_father_dir(filename)
    if path.is_dir():
        print('create_dir 测试成功!')
        os.removedirs(fatherpath)

