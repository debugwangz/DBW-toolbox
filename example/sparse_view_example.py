from DBWToolbox.reconstruction import get_fan_sino_param, recon_fan_param, Paramaters
from scipy.io import loadmat
from os.path import join as ospj
from DBWToolbox.showresult import write_excel, read_excel_dict, show_LIP, show_histogram
from DBWToolbox.showresult import image_show, images_show
from skimage.metrics import mean_squared_error as mse, structural_similarity as ssim


class SparseViewParamaters(Paramaters):
    def __init__(self, sparse_num):
        super(SparseViewParamaters, self).__init__()
        self.param['n_proj'] = sparse_num        #投影数


def get_sparse_image(full_image, sparse_nums):
    sinos = {}
    images = {}
    for sparse_num in sparse_nums:
        param = SparseViewParamaters(sparse_num).param
        param['nx'] = full_image.shape[0]
        param['ny'] = full_image.shape[1]
        param['dect_count'] = full_image.shape[0] * 2
        sino = get_fan_sino_param(full_image, param)
        sinos[str(sparse_num)] = sino
        rec_image = recon_fan_param(sino, param)
        images[str(sparse_num)] = rec_image
    return sinos, images

def rec_example():
    result_path = ospj('..', 'result')
    phantom = loadmat(ospj('..', 'data', 'phantom.mat'))['phantom256']
    image_show(phantom, save_path=ospj(result_path, 'phantom256.png'))
    sparse_nums = [39, 57, 75, 100]
    sinos, images = get_sparse_image(phantom, sparse_nums)
    images_show(sinos, (2, 2), figure_size=(20, 4), axis_off=False,
                save_path=ospj(result_path, 'sparse-sinograms.png'))
    images_show(images, (2, 2), figure_size=(10, 10), axis_off=True,
                save_path=ospj(result_path, 'sparse-images.png'))
# rec_example()


def write_excel_example():
    sparse_nums = [39, 57, 75, 100]
    result_path = ospj('..', 'result')
    phantom = loadmat(ospj('..', 'data', 'phantom.mat'))['phantom256']
    _, images = get_sparse_image(phantom, sparse_nums)
    data_list = []
    for sparse_num in sparse_nums:
        data = {}
        sparse_image = images[str(sparse_num)]
        data['sparse number'] = str(sparse_num)
        data['mse'] = mse(phantom, sparse_image)
        data['ssim'] = ssim(phantom, sparse_image, data_range=phantom.max()-phantom.min())
        data_list.append(data)
    write_excel(ospj(result_path, 'indicator.xlsx'), data_list=data_list,
                sheet_name='sparse indicator', index='sparse number')
# write_excel_example()


def show_lIP_example():
    sparse_nums = [39, 57, 75, 100]
    result_path = ospj('..', 'result')
    phantom = loadmat(ospj('..', 'data', 'phantom.mat'))['phantom256']
    _, images = get_sparse_image(phantom, sparse_nums)
    lines = {}
    lines['reference'] = phantom[128]
    for sparse_num in sparse_nums:
        lines[str(sparse_num) + ' views'] = images[str(sparse_num)][128]

    show_LIP(lines, bounds=(0.05, 0.45, 0.6, 0.5), sub_range=range(35, 50),
             loc1=3, loc2=4, save_path=ospj(result_path, 'sparse LIP.png'))

show_lIP_example()

def show_hist_example():
    result_path = ospj('..', 'result')
    data = read_excel_dict(ospj(result_path, 'indicator.xlsx'), index='sparse number',
                           sheet_name='sparse indicator')
    show_histogram(data, legend_loc='upper left', save_path=ospj(result_path, 'histgram.png'))
# show_hist_example()