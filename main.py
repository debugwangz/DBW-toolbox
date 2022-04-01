from DBWToolbox.reconstruction import get_fan_sino_param, recon_fan_param
from scipy.io import loadmat
from os.path import join as ospj
from DBWToolbox.paramaters import Paramaters
from matplotlib import pyplot as plt
from DBWToolbox.showresult import read_excel, show_line_profile
import pandas as pd
# sparse_nums = [39, 57, 75, 100]
#
image = loadmat(ospj('data', 'phantom.mat'))['phantom256']
lines = {}
for i in range(0, 256, 64):
    lines[str(i)] = image[i]
show_line_profile(lines, bounds=(0.05, 0.45, 0.6, 0.5), sub_range=range(64, 128))
#
# param = Paramaters().param
# sino = get_fan_sino_param(image, param)
# plt.imshow(sino, cmap='gray')
# plt.show()
# rec_image = recon_fan_param(sino, param)
# plt.imshow(image, cmap='gray')
# plt.show()

# data = read_excel('measures_75.xls', sheet_name='open3d')
# # df.reset_index(inplace=True)
# for i in range(len(data)):
#     print(data[i])
