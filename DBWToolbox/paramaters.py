# from __future__ import print_function, division, absolute_import


class Paramaters:
    def __init__(self):
        self.param = {}
        self.param['vol_geom_size'] = (256, 256)    # CT图像分辨率 X,Y
        self.param['sx'] = 0.05*1200       # CT图像X 方向实际物理尺寸
        self.param['sy'] = 0.05*1200        # CT图像Y 方向实际物理尺寸
        self.param['dect_count'] = 1024    #高分辨率探测器的分辨率
        self.param['dsd'] = 185.0329      #光源到探测器的距离
        self.param['dso'] = 141.5261       #光源到旋转中心的距离
        self.param['startangle'] = 0     #旋转起始角度
        self.param['endangle'] = 360   #旋转终止角度
        self.param['n_proj'] = 360        #投影数
        self.param['detector_width'] = 0.05
        self.param['algorithm'] = 'FBP_CUDA'  # 投影算法
        self.param['interation'] = -1  # 如果是迭代算法，这里写迭代次数
        self.param['short_scan'] = False  # 是否使用short scan