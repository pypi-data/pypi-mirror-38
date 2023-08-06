"""
模块的主要功能是进行路径操作
"""

import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def list_files(directory=None, fm=None, isabspath=False):
    '''
    返回文件夹下的所有文件<list>
    :param directory: <str> 文件夹路径
        如果给出文件夹路径, 则返回该文件夹下的文件;
        如果没有给出文件夹路径, 则返回控制台所在文件夹下的文件
    :param fm: <str, list> 指定文件格式
        如果给出了文件格式, 则返回指定格式的文件;
        如果没有给出文件格式, 则返回所有文件
    :param isabspath: <bool> 为真时返回绝对路径文件名, 为假时返回相对路径文件名
    '''
    if not directory:
        directory = os.getcwd()
    files = os.listdir(directory)
    
    if isinstance(fm, str):
        fm = [fm]
        files = [file for file in files if file.split('.')[-1] in fm]

    if not isabspath:
        return files
    else:
        files = [os.path.join(directory, file) for file in files]
        return files


def create_father_dir(filename):
    '''
    接收一个文件名, 判断其父路径是否存在, 如果不存在, 则创建
    :param filename: <str>接收的文件路径, 为相对路径
    '''
    absfiledir = os.path.abspath(os.path.dirname(filename) + os.path.sep + '.')  # 获取父文件夹的绝对路径
    # 如果父文件夹不存在则创建
    path = Path(absfiledir)
    if path.is_dir():
        pass
    else:
        os.makedirs(absfiledir)


def create_dir_by_filename(filename, tail=None):
    '''
    创建文件同名文件夹
    :param filename: <str>接收的文件路径, 为相对路径或绝对路径
    :param tail: <str>有时候生成的文件夹后要加个尾缀
    '''
    fatherpath = os.path.abspath(os.path.dirname(filename))
    dirname = ''.join(filename.split(os.path.sep)[-1].split('.')[:-1])
    absdir = os.path.join(fatherpath, dirname)
    if tail:
        absdir += tail
    path = Path(absdir)
    if not path.is_dir():
        os.makedirs(absdir)
    return absdir


# tkinter.filedialog.asksaveasfile():选择以什么文件保存，创建文件并返回文件流对象
# tkinter.filedialog.askopenfile():选择打开什么文件，返回IO流对象
# tkinter.filedialog.askopenfiles():选择打开多个文件，以列表形式返回多个IO流对象
def get_goal_by_dialog_box(goal='file', filetype=None):
    """
    启用对话框, 以根据goal参数的不同选择文件或文件夹
    :param goal:
    :param filetype:
    :return: 返回文件名或文件夹名
    """
    root = tk.Tk()
    root.withdraw()

    if goal == 'file':
        if isinstance(filetype, tuple):
            goal_name = filedialog.askopenfilename(filetype=filetype)
        else:
            goal_name = filedialog.askopenfilename()  # 选择文件, 返回文件名
    elif goal == 'files':
        if isinstance(filetype, tuple):
            goal_name = filedialog.askopenfilenames(filetype=filetype)
        else:
            goal_name = filedialog.askopenfilenames()  # 选择多个文件, 返回文件名列表
    elif goal == 'directory':
        goal_name = filedialog.askdirectory()  # 选择目录，返回目录名
    else:
        goal_name = os.getcwd()

    root.destroy()
    return goal_name


def get_file_by_dialog_box():
    """
    打开一个对话框, 以选择文件, 返回文件路径.
    利用了tkinter框架
    :return: 返回文件绝对路径名
    """
    return get_goal_by_dialog_box(goal='file')


def get_files_by_dialog_box():
    """
    打开一个对话框, 以选择多个文件, 返回文件名列表
    :return:
    """
    return get_goal_by_dialog_box(goal='files')


def get_directory_by_dialog_box():
    """
    打开一个对话框, 以选择文件夹, 返回文件夹名
    :return:
    """
    return get_goal_by_dialog_box(goal='directory')


def ask_file(filetype=None):
    return get_goal_by_dialog_box(goal='file', filetype=filetype)


def ask_files(filetype=None):
    return get_goal_by_dialog_box(goal='files', filetype=filetype)


def ask_dir():
    return get_goal_by_dialog_box(goal='directory')


def ask_directory(fi):
    return ask_dir()


def chdir():
    """
    切换控制台路径
    :return:
    """
    return os.chdir(ask_dir())




