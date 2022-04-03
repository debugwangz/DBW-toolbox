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
        if columns_width == None:
            sheet.col(i).width = 256 * 17
        else:
            column_width = columns_width[data_list[0].keys()[i]]
            sheet.col(i).width = column_width
    keys = sorted(data_list[0].keys())
    if head_name not in keys:
        raise Exception(print('Missing the head name in excel. Each row and column should have a name！'))
    # head_name 要在第一列
    keys.remove(head_name)
    keys.insert(0, head_name)
    # 填表头
    for i in range(len(keys)):
        sheet.write(0, i, keys[i], style)  # 0行i列

    for row in range(1, len(data_list)+1):
        data = data_list[row-1]
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


def __init_lines_markers(names):
    # List of markers in plt https://matplotlib.org/3.1.0/api/markers_api.html?highlight=marker#module-matplotlib.markers
    lines_marker = {}
    for name in names:
        lines_marker[name] = "None"
    return lines_marker


def __init_hatch(names):
    hatch = {}
    for name in names:
        hatch[name] = ""
    return hatch


def show_LIP(lines: dict, bounds, sub_range, is_show=True, save_path=None, lines_style=None,
             lines_color=None, lines_width=None, lines_marker=None, y_max=-1,
             loc1=2, loc2=4, xlabel='Pixel', ylabel='Intensity', dpi=300,
             legend_loc='upper right', ):
    if lines_style is None:
        lines_style = __init_lines_style(lines.keys())
    if lines_width is None:
        lines_width = __init_lines_width(lines.keys())
    if lines_color is None:
        lines_color = __init_lines_color(lines.keys())
    if lines_marker is None:
        lines_marker = __init_lines_markers(lines.keys())

    # 画主区域
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    for name in lines.keys():
        line = lines[name]
        ax.plot(range(len(line)), line, linewidth=0.8, label=name,
                linestyle=lines_style[name], marker=lines_marker[name],
                color=lines_color[name])
        # ax.legend(loc='upper right', frameon=False, prop={'size': 9})

    if y_max != -1:
        plt.ylim(top=y_max)
    axins = ax.inset_axes(bounds)
    # 画放大区域
    for name in lines.keys():
        axins.plot(sub_range, lines[name][sub_range], linewidth=lines_width[name],
                   linestyle=lines_style[name], color=lines_color[name],
                    marker=lines_marker[name])

    mark_inset(ax, axins, loc1=loc1, loc2=loc2, fc="none", ec='k', lw=1, linestyle=(0, (3, 3)))
    axins.set_xticks([])
    axins.set_yticks([])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc=legend_loc)
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi)
        print('save file in {}'.format(save_path))
    if is_show:
        plt.show(dpi=600)
    plt.close()


# def show_histgram(data_list, hatch=None):
#     # if hatch is None:
#     #     hatch = __init_hatch(data_list)
#     time_cost = {}
#     measures = {}
#     measures['TV']={'Time':1.0,
#                    'MSE': 1.0,
#                    'SSIM':(0.7530 - 0.8078 *0.9)/(0.8078*0.1)
#                    }
#     measures['AGIRT']={'Time':2.7866/46.9946,
#                    'MSE': (0.2375 - 0.3356*0.6)/(0.3356*0.4),
#                    'SSIM':   (0.8045 - 0.8078 *0.9)/(0.8078*0.1)  #0.8002
#                    }
#     measures['Restarted AGIRT']={'Time': 5.0107/46.9946 ,
#                    'MSE': (0.2201 - 0.3356*0.6)/(0.3356*0.4),
#                    'SSIM': 1.0  #0.8066
#                    }
#     measures['FBPConvNet'] = {'Time': 1.57117/46.9946,
#                                  'MSE': (0.2152 - 0.3356*0.6)/(0.3356*0.4),
#                                  'SSIM': (0.7985 - 0.8078 *0.9)/(0.8078*0.1) # 0.8066
#                                  }
#     # measures['FBP'] = {'Time': 1.3165/110.6119,
#     #                              'MSE': 1,
#     #                              'SSIM': 1  # 0.8066
#     #                              }
#     bar_width = 0.2
#     indicators = ['Time', 'MSE', 'SSIM']
#     tick_labels = ['TV', 'FBPConvNet' ,'AGIRT', 'Restarted AGIRT']
#     x = np.arange(3)
#     patterns = ['///','...', '---','\\\\\\','++']
#     for tick_label, i in zip(tick_labels, range(len(tick_labels))):
#         measure = measures[tick_label]
#         y = []
#         for indicator in measure.keys():
#             y.append(measure[indicator])
#         plt.bar(x+i*bar_width,y,bar_width, align='center', label=tick_label,
#                 hatch=patterns[i], color=color_mappings[tick_labels[i]])
#     # plt.ylim(top=1.6)
#
#     plt.ylabel("Performance(Normalized)")
#     plt.xticks(x + 1.5*bar_width , indicators)
#     plt.legend(loc=(0.43, 0.7))
#     # plt.show()
#     plt.savefig(ospj(plot_save_path, 'performance.png'), dpi=300)
#     plt.close()
#

