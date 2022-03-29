from __future__ import print_function, division, absolute_import
import numpy as np
import json
config_path = 'config/'
class Paramaters:
    def __init__(self):
        self.param = {}
        self.param['vol_geom_size'] = (256, 256)    # CT图像X方向分辨率
        self.param['ny_h'] = 512    # CT图像Y方向分辨率

        self.param['nx_l'] = 1200     # CT图像X方向分辨率
        self.param['ny_l'] = 1200    # CT图像Y方向分辨率

        self.param['sx'] = 0.05*1200       # CT图像X 方向实际物理尺寸
        self.param['sy'] = 0.05*1200        # CT图像Y 方向实际物理尺寸

        self.param['nu'] = 1200       #低分辨率探测器的分辨率
        self.param['dect_count'] = 1024    #高分辨率探测器的分辨率
        # self.param['nu_h'] = 512
        self.param['su'] = 1200*0.05   #探测器的实际物理尺寸
        self.param['dsd'] = 185.0329      #光源到探测器的距离
        self.param['dso'] = 141.5261       #光源到旋转中心的距离
        self.param['startangle'] = 0     #旋转起始角度
        self.param['endangle'] = 360   #旋转终止角度
        self.param['nProj'] = 360        #投影数
        self.param['detector_width'] = 0.05
        self.param['u_water'] = 0.0205
        self.param['algorithm'] = 'FBP_CUDA'
        self.param['short_scan'] = False
        # with open(config_path+'init_config.json', 'w') as f:
        #     json.dump(self.param, f)

