
import math
import codecs


def readfile(file, encoding='utf8'):
    """
    读取文本文件, 返回文本文件内容
    :param file: 要读取的文件名
    :param encoding: 文件编码, 默认为utf8
    :return: 返回文件内容
    """
    with codecs.open(file, mode='r', encoding=encoding) as f:
        return f.read()


def writefile(file, content, mode='w', encoding='utf8'):
    """
    将文本内容写入文件
    :param file: 要写入的文件名
    :param content: 要写入的内容
    :param mode: 写入模式, 默认为w覆盖
    :param encoding: 写入编码, 默认为utf8
    :return:
    """
    with codecs.open(file, mode=mode, encoding=encoding) as f:
        f.write(content)


def transcode(from_file, to_file, from_code='utf8', to_code='GBK'):
    """
    转换文本文件格式
    :param from_file: 待转换的文件名
    :param to_file: 转换后的文件名
    :param from_code: 转换前的文件编码
    :param to_code: 转换后的文件编码
    :return:
    """
    content = readfile(from_file, encoding=from_code)
    writefile(to_file, content, encoding=to_code)
    return '{} ====> {}'.format(from_file, to_file)


def split_list(li, num=8):
    """
    分割列表
    :param li: 要分割的列表
    :param num: 要分割的份数
    :return: 返回分割结果
    """
    return split_list_by_len(li, math.ceil(len(li) / num))


def split_list_by_len(li, n):
    return [li[i: i + n] for i in range(0, len(li), n)]
