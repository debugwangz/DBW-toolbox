import os
import numpy as np
# from PIL import Image
import pydicom
# from matplotlib import pyplot as plt
from math import ceil
import json
from skimage.external import tifffile as tif


def HU_to_attuation(image, water):
    image = image.astype(np.float32)
    image /= 1000
    image *= water
    image += water
    return image


def Attuation_to_HU(image, water):
    image -= water
    image /= water
    image *= 1000
    image = image.astype(np.int16)
    return image


def save_image2tif(image, filepath, filename, is_rewrite=True):
    if not is_rewrite:
        if os.path.isfile(os.path.join(filepath, filename + '.tif')):
            return
    if not os.path.exists(filepath):
        print('create path {}'.format(filepath))
        os.makedirs(filepath)

    if not type(image) is np.ndarray:
        image = np.array(image)
    tif.imsave(os.path.join(filepath, filename + '.tif'), image)
    # Image.fromarray(image).save(os.path.join(filepath, filename + '.tif'))


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
    array = np.array(tif.imread(fpath))
    return array


def remove_empty(d:dict):
    d_tmp = {}
    for key in d.keys():
        value = d[key]
        if len(value) != 0:
            d_tmp[key] = value
    return d_tmp


def seconds2time(seconds:float):
    seconds = ceil(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return "%dh : %02dm : %02ds" % (h, m, s)
    if m > 0:
        return "%02dm : %02ds" % (m, s)
    return "%02ds" % s


def save_dict2_josn(filepath, d: dict, mode='w'):
    json_str = json.dumps(d, ensure_ascii=False)

    with open(filepath, mode) as json_file:
        json_file.write(json_str)