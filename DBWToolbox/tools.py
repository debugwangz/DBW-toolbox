import os
import numpy as np
from PIL import Image
import pydicom


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


def tif2np(fdir, fname):
    if not fname.endswith('.tif'):
        print('File is not tif!')
        return None
    array = np.array(Image.open(ospj(fdir, fname)))
    return array
