from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import numpy as np
import pandas as pd
import os
from styleframe import StyleFrame
from DBWToolbox.tools import remove_empty

def write_excel(full_name, data_list: list,
                sort_by=None, sort_axis=0, ascending=True,
                alignment=None, sheet_name='sheet',
                columns_width: dict =None, index='name'):

    table_head = list(data_list[0].keys())
    if index not in table_head:
        raise Exception(print('Missing the index column in excel. Each row and column should have a name！'))

    if table_head[0] != index:     # index 要在第一列
        table_head.remove(index)
        table_head.insert(0, index)
    table_content = {}
    #构建表内容
    for i in range(len(data_list)):
        for index in table_head:
            if index not in table_content.keys():
                table_content[index] = []
            table_content[index].append(data_list[i][index])
    frame = pd.DataFrame.from_dict(table_content)
    if sort_by is not None:
        frame.sort_values(by=sort_by, axis=sort_axis, ascending=ascending, inplace=True)
    with StyleFrame.ExcelWriter(full_name) as writer:# 注意style只接受openpyxl作为engine
        sf = StyleFrame(frame)
        sf.to_excel(writer, sheet_name=sheet_name, index=False, best_fit=table_head)

    return


def read_excel_dict(full_name, index, sheet_name='sheet'):
    data_list = read_excel_list(full_name, sheet_name)
    data = {}
    for i in range(len(data_list)):
        row_name = str(data_list[i][index])
        column_values = {}
        for column_name in data_list[i].keys():
            if column_name == index:
                continue
            column_values[column_name] = data_list[i][column_name]
        data[row_name] = column_values
    return data


def read_excel_list(full_name, sheet_name='sheet'):
    if not os.path.isfile(full_name):
        raise Exception(full_name+'is not a file !!!')

    df = pd.DataFrame(pd.read_excel(io=full_name, sheet_name=sheet_name))
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


def __init_colors(names):
    # List of colors in plt https://matplotlib.org/3.1.0/gallery/color/named_colors.html
    colors = {}
    default_colors = ['#845ec2', '#d65db1', '#ff6f91', '#ffc75f',
                      '#008e9b', '#008f7a',
                      'c', 'm', 'y', 'b', 'g', 'r']

    # default_colors = ['blue', 'deeppink', 'green', 'black', 'c', 'm', 'y', 'b', 'g', 'r']
    if len(names) > len(default_colors):
        raise Exception(print('Can not initial line_colors because of too many lines. Please set up lines_color'))
    for name, i in zip(names, range(len(names))):
        colors[name] = default_colors[i]
    return colors


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


def __default_hatch(names):
    hatch = {}
    patterns = ['///', '...', '---', '\\\\\\', '++']
    if len(names) > len(patterns):
        raise Exception(print('Can not get default patterns because of too many names. Please set up patterns'))
    for name, i in zip(names, range(len(names))):
        hatch[name] = patterns[i]
    return hatch


def show_LIP(lines: dict, bounds, sub_range, is_show=True, save_path=None, lines_style=None,
             lines_color=None, lines_width=None, lines_marker=None, ylim=None,
             loc1=2, loc2=4, xlabel='Pixel', ylabel='Intensity', dpi=300,
             legend_loc='upper right', ):
    if lines_style is None:
        lines_style = __init_lines_style(lines.keys())
    if lines_width is None:
        lines_width = __init_lines_width(lines.keys())
    if lines_color is None:
        lines_color = __init_colors(lines.keys())
    if lines_marker is None:
        lines_marker = __init_lines_markers(lines.keys())

    # 画主区域
    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    for name in lines.keys():
        line = lines[name]
        ax.plot(range(len(line)), line, linewidth=0.5, label=name,
                linestyle=lines_style[name], marker=lines_marker[name],
                color=lines_color[name])
        # ax.legend(loc='upper right', frameon=False, prop={'size': 9})
    if ylim is not None:
        plt.ylim(ylim)
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
    if is_show:
        plt.show()
    plt.close()


def show_histogram(data, hatch=None, bar_width=-1, colors=None, x_label='', y_label='',
                   save_path=None, is_show=True, legend_loc='upper right', dpi=300, default_hatch=False):
    tick_labels = list(data.keys())
    indicators = list(data[tick_labels[0]].keys())
    x = np.arange(len(indicators))
    fig, ax = plt.subplots()
    if bar_width == -1:
        bar_width = 1/(len(tick_labels)+1)
    if hatch is None:
        if default_hatch:
            hatch = __default_hatch(tick_labels)
        else:
            hatch = __init_hatch(tick_labels)

    if colors is None:
        colors = __init_colors(tick_labels)
    for tick_label, i in zip(tick_labels, range(len(tick_labels))):
        measure = data[tick_label]
        y = []
        for indicator in indicators:
            y.append(measure[indicator])
        ax.bar(x + (i-(len(tick_labels)-1)/2) * bar_width, y, bar_width, label=tick_label,
               hatch=hatch[tick_label], color=colors[tick_label], )

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xticks(x, indicators)
    ax.legend(loc=legend_loc)
    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi)
    if is_show:
        plt.show()

    plt.close()

def image_show(image, is_show=True, save_path=None,
               axis_off=True, title=None, dpi=300,
               is_gray=True, fontsize=16):
    cmap = None
    if is_gray:
        cmap = plt.get_cmap()
        plt.gray()
    plt.imshow(image)
    if save_path is not None:
        directory, _ = os.path.split(save_path)
        os.makedirs(directory, exist_ok=True)
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    if axis_off:
        plt.axis('off')
    if title is not None:
        plt.title(title, fontsize=fontsize)
    if is_show:
        plt.show()
    plt.close()
    if is_gray:
        plt.set_cmap(cmap)


def images_show(images: dict, shape=-1, is_show=True, save_path=None,
                axis_off=True, figure_size=(7, 7), dpi=300, title=None,
                line_config: dict = None, is_gray=True, fontsize=16):

    if len(images.keys()) == 1:
        image_title = list(images.keys())[0]
        image = images[image_title]
        image_show(image, is_show, save_path, axis_off,
                   image_title, dpi, is_gray, fontsize)
        return
    if shape == -1:
        shape = (1, len(images.keys()))
    cmap = None
    if is_gray:
        cmap = plt.get_cmap()
        plt.gray()
    images_titles = list(images.keys())
    fig, axs = plt.subplots(nrows=shape[0], ncols=shape[1], constrained_layout=False, figsize=figure_size)
    axs = axs.reshape(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i*shape[1] + j >= len(images_titles):
                axs[i, j].axis('off')
                continue
            image_title = images_titles[i * shape[1] + j]
            axs[i, j].set_title(image_title, fontsize=fontsize)
            axs[i, j].imshow(images.get(image_title))
            if line_config is None:
                continue
            if image_title in line_config.keys():
                axs[i, j].plot(line_config[image_title]['x'], line_config[image_title]['y'],
                               line_config[image_title]['color'],
                               linewidth=line_config[image_title]['linewidth'],
                               linestyle=line_config[image_title]['linestyle'])
            if axis_off:
                axs[i, j].axis('off')
    plt.tight_layout()
    if title is not None:
        plt.suptitle(title, fontsize=fontsize)
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    if is_show:
        plt.show()
    plt.close()
    if is_gray:
        plt.set_cmap(cmap)


def plot_metrics(metrics, is_remove_empty=True, metrics_name=None, range_begin=0, title=None,
                 xlabel=None, ylabel=None, save_path=None, dpi=300):
    if isinstance(metrics, np.ndarray):
        metrics = metrics.item()
    assert isinstance(metrics, dict), "Metrics should be dict"
    if is_remove_empty:
        metrics = remove_empty(metrics)
    if metrics_name == None:
        metrics_name = metrics.keys()
    for metric_name in metrics_name:
        metric = metrics[metric_name]
        plt.plot(range(range_begin, len(metric)), metric[range_begin:], label=metric_name)
    plt.legend()

    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    plt.show()