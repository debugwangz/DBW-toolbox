import matplotlib.pyplot as plt
import pandas as pd
import os
from os.path import join as ospj
from tools import str_contain
from tools import tif2np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import numpy as np
from PIL import Image
from skimage.draw import line
import xlwt


def write_excel(file_path, data_list: list):
    if not str.endswith(file_path, '.xls'):
        file_path += '.xls'

    work_book = xlwt.Workbook(encoding='utf-8')
    alignment = xlwt.Alignment()
    alignment.wrap = 1
    alignment.horz = 0x02
    style = xlwt.XFStyle()
    style.alignment = alignment
    sheet = work_book.add_sheet('open3d')    # 将sheet命名为open3d
    for i in range(len(data_list[0].keys())):
        sheet.col(i).width = 256 * 17
    keys = sorted(data_list[0].keys())
    # 填表头
    for i in range(len(keys)):
        sheet.write(0, i, keys[i], style)  # 0行i列
    if 'name' not in keys:
        print('Rows dont have their name. Each row should have a name！')
        return
    # name 要在第一列
    keys.remove('name')
    keys.insert(0, 'name')
    for row in range(1, len(data_list)):
        data = data_list[row]
        for column in range(len(keys)):
            sheet.write(row, column, data[keys[column]], style)  # 从row行第column列开始写，注意第一行是表头，所以row从第二行开始写
    work_book.save(file_path)

