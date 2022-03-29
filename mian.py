from DBWToolbox.reconstruction import get_fan_sino_param, recon_fan_param
from scipy.io import loadmat
from os.path import join as ospj
from DBWToolbox.paramaters import Paramaters
from matplotlib import pyplot as plt

sparse_nums = [39,57,75,100]

image = loadmat(ospj('data', 'phantom.mat'))['phantom256']

param = Paramaters().param
sino = get_fan_sino_param(image, param)
plt.imshow(sino, cmap='gray')
plt.show()
rec_image = recon_fan_param(sino, param)
plt.imshow(image, cmap='gray')
plt.show()
