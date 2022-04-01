import os
import xlwt
from matplotlib import pyplot as plt
from os.path import join as ospj
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


def write_excel(full_name, data_list: list, alignment=None, sheet_name='sheet',
                columns_width:dict =None, head_name='name'):
    if not str.endswith(full_name, '.xls'):
        full_name += '.xls'
    directory, _ = os.path.split(full_name)
    if len(directory) != 0:
        os.makedirs(directory, exist_ok=True)
    work_book = xlwt.Workbook(encoding='utf-8')
    if alignment is None:
        alignment = xlwt.Alignment()
        alignment.wrap = 1
        alignment.horz = 0x02
    style = xlwt.XFStyle()
    style.alignment = alignment
    sheet = work_book.add_sheet(sheet_name)    # 将sheet命名为 sheet_name
    for i in range(len(data_list[0].keys())):
        column_width = columns_width[data_list[0].keys()[i]]
        if column_width == -1 or columns_width == None:
            sheet.col(i).width = 256 * 17
        else:
            sheet.col(i).width = column_width
    keys = sorted(data_list[0].keys())
    # head_name 要在第一列
    keys.remove(head_name)
    keys.insert(0, head_name)
    # 填表头
    for i in range(len(keys)):
        sheet.write(0, i, keys[i], style)  # 0行i列
    if head_name not in keys:
        print('Missing the head_name in excel. Each row and column should have a name！')

    for row in range(1, len(data_list)):
        data = data_list[row]
        for column in range(len(keys)):
            sheet.write(row, column, data[keys[column]], style)  # 从row行第column列开始写，注意第一行是表头，所以row从第二行开始写
    work_book.save(full_name)


def read_excel(full_name, sheet_name='sheet'):
    if not os.path.isfile(full_name):
        raise Exception(full_name+'is not a file !!!')

    df = pd.DataFrame(pd.read_excel(io='measures_75.xls', sheet_name=sheet_name))
    data_all = df.to_dict(orient='index')
    data_list = []
    for i in range(len(data_all.keys())):
        data_list.append(data_all[i])
    return data_list


def __init_lines_style(names):
    lines_style = {}
    for name in names:
        lines_style[name] = 'solid'
    return lines_style


def __init_lines_width(names):
    lines_width = {}
    for name in names:
        lines_width[name] = 1
    return lines_width


def __init_lines_color(names):
    # List of colors in plt https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    lines_color = {}
    colors = ['blue', 'deeppink', 'green', 'black', 'c', 'm', 'y', 'b', 'g', 'r']
    if len(names) > len(colors):
        raise Exception(print('Can not initial line_colors because of too many lines. Please set up lines_color'))
    i = 0
    for name in names:
        lines_color[name] = colors[i]
        i += 1
    return lines_color


def show_line_profile(lines: dict, bounds, sub_range, save_path=None, lines_style=None,
                      lines_color=None, lines_width=None, y_max=-1, loc1=2, loc2=4,
                      xlabel='Pixel', ylabel='Intensity', dpi=300):
    if lines_style is None:
        lines_style = __init_lines_style(lines.keys())
    if lines_width is None:
        lines_width = __init_lines_width(lines.keys())
    if lines_color is None:
        lines_color = __init_lines_color(lines.keys())

    # 画主区域
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    for name in lines.keys():
        line = lines[name]
        ax.plot(range(len(line)), line, linewidth=0.8, label=name, linestyle=lines_style[name],
                color=lines_color[name])
        ax.legend(loc='upper right', frameon=False, prop={'size': 9})

    if y_max != -1:
        plt.ylim(top=y_max)
    axins = ax.inset_axes(bounds)
    # 画放大区域
    for name in lines.keys():
        axins.plot(sub_range, lines[name][sub_range], linewidth=lines_width[name],
                   linestyle=lines_style[name], color=lines_color[name])

    mark_inset(ax, axins, loc1=loc1, loc2=loc2, fc="none", ec='k', lw=1, linestyle=(0, (3, 3)))
    axins.set_xticks([])
    axins.set_yticks([])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi)
        print('save file in {}'.format(save_path))
    plt.show()
    plt.close()




