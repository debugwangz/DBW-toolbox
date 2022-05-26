import os
import numpy as np
from PIL import Image
import pydicom
from matplotlib import pyplot as plt


def save_image2tif(image, filepath, filename, is_rewrite=True):
    if not is_rewrite:
        if os.path.isfile(os.path.join(filepath, filename + '.tif')):
            return
    if not os.path.exists(filepath):
        print('create path {}'.format(filepath))
        os.makedirs(filepath)

    if not type(image) is np.ndarray:
        image = np.array(image)
    Image.fromarray(image).save(os.path.join(filepath, filename + '.tif'))


def read_dicom_mayo(path,):
    s = pydicom.read_file(path)
    image = s.pixel_array
    image = image.astype(np.int16)
    image[image == -2000] = 0
    intercept = s.RescaleIntercept
    slope = s.RescaleSlope
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
    image += np.int16(intercept)
    image = image.astype(np.float64)
    return image


def str_contain(s, sub):
    return not s.find(sub) == -1


def tif2np(fpath):
    if not fpath.endswith('.tif'):
        print('File is not tif!')
        return None
    array = np.array(Image.open(fpath))
    return array


def image_show(image, is_show=True, save_path=None,
               axis_off=True, title=None, dpi=300,
               is_gray=True):
    cmap = None
    if is_gray:
        cmap = plt.get_cmap()
        plt.gray()
    plt.imshow(image)
    if save_path is not None:
        directory, _ = os.path.split(save_path)
        os.makedirs(directory, exist_ok=True)
        plt.savefig(save_path, dpi=dpi)
    if axis_off:
        plt.axis('off')
    if title is not None:
        plt.title(title)
    if is_show:
        plt.show()
    plt.close()
    if is_gray:
        plt.set_cmap(cmap)




def images_show(images, shape, is_show=True, save_path=None,
                axis_off=True, figure_size=(7, 7), dpi=300,
                line_config: dict = None, is_gray=True):
    cmap = None
    if is_gray:
        cmap = plt.get_cmap()
        plt.gray()

    titles = list(images.keys())
    fig, axs = plt.subplots(nrows=shape[0], ncols=shape[1], constrained_layout=False, figsize=figure_size)

    axs = axs.reshape(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i*shape[1] + j >= len(titles):
                axs[i, j].axis('off')
                continue
            title = titles[i*shape[1] + j]
            axs[i, j].set_title(title)
            axs[i, j].imshow(images.get(title))
            if line_config is None:
                continue
            if title in line_config.keys():
                axs[i, j].plot(line_config[title]['x'], line_config[title]['y'],
                               line_config[title]['color'],
                               linewidth=line_config[title]['linewidth'],
                               linestyle=line_config[title]['linestyle'])
            if axis_off:
                axs[i, j].axis('off')
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi)
    if is_show:
        plt.show()
    plt.close()
    if is_gray:
        plt.set_cmap(cmap)

