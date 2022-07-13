# import astra
import numpy as np
class Paramaters:
    def __init__(self):
        self.param = {}
        self.param['nx'] = 512
        self.param['ny'] = 512
        self.param['scale'] = 2
        self.param['nu'] = 1024
        self.offset = 90
        self.param['sx'] = 70
        self.param['sy'] = 70
        self.param['su'] = 1024 * 0.139  # 1024 * 0.417
        self.param['dsd'] = 1500
        self.param['dso'] = 1000
        self.param['nProj'] = 720
        self.param['startangle'] = 0
        self.param['endangle'] = 2 * np.pi
        self.param['detector_width'] = 1

        self.reuse = False

#
#
# def get_fan_sino_param(image, param):
#     angles = np.deg2rad(np.linspace(param['startangle'], param['endangle'],
#                                     param['n_proj'], endpoint=False))
#     sino = get_fan_sino(image, source_ori=param['dso'], ori_detector=param['dsd']-param['dso'], dect_w=param['detector_width'],
#                         dect_count=param['dect_count'], vol_geom_size=param['vol_geom_size'], angles=angles,)
#     return sino
#
#
# def recon_fan_param(sino, param):
#     angles = np.deg2rad(np.linspace(param['startangle'], param['endangle'],
#                                     param['n_proj'], endpoint=False))
#     image = recon_fan(alg=param['algorithm'], sino=sino, source_ori=param['dso'], ori_detector=param['dsd']-param['dso'],
#                       dect_w=param['detector_width'], vol_geom_size=param['vol_geom_size'], angles=angles,
#                       interations=param['interation'], short_scan=param['short_scan'])
#     return image
#
#
# def get_fan_sino(image, source_ori, ori_detector, dect_w, dect_count, vol_geom_size, angles, ):
#     # astra.algorithm.clear()
#     vol_geom_fan = astra.create_vol_geom(vol_geom_size)
#     proj_geom_fan = astra.create_proj_geom('fanflat', dect_w, dect_count,
#                                            angles,
#                                            source_ori, ori_detector)
#
#     proj_fan_id = astra.create_projector('cuda', proj_geom_fan, vol_geom_fan)
#     sino_fan_id, sino_gram = astra.create_sino(image, proj_fan_id)
#
#     astra.projector.delete(proj_fan_id)
#     astra.projector.delete(sino_fan_id)
#     # astra.algorithm.clear()
#     astra.clear()
#     return sino_gram
#
#
# def recon_fan(alg, sino, source_ori, ori_detector, dect_w, vol_geom_size,
#               angles, interations=-1, short_scan=False):
#     astra.algorithm.clear()
#     vol_geom_fan = astra.create_vol_geom(vol_geom_size)
#
#     proj_geom_fan = astra.create_proj_geom('fanflat', dect_w, sino.shape[1],
#                                            angles,
#                                            source_ori, ori_detector)
#     proj_fan_id = astra.create_projector('cuda', proj_geom_fan, vol_geom_fan)
#     sinogram_fan_id = astra.data2d.create('-sino', proj_geom_fan, sino)
#     rec_fan_id = astra.data2d.create('-vol', vol_geom_fan)
#     cfg_fan = astra.astra_dict(alg)
#     cfg_fan['ReconstructionDataId'] = rec_fan_id
#     cfg_fan['ProjectionDataId'] = sinogram_fan_id
#     ## cfg_fan['ProjectorId'] = proj_fan_id
#     cfg_fan['option'] = {'ShortScan': short_scan}
#
#     alg_fan_id = astra.algorithm.create(cfg_fan)
#     if interations != -1:
#         astra.algorithm.run(alg_fan_id, interations)
#     else:
#         astra.algorithm.run(alg_fan_id)
#     rec_fan = astra.data2d.get(rec_fan_id)
#     astra.algorithm.delete(alg_fan_id)
#     astra.data2d.delete(rec_fan_id)
#     astra.data2d.delete(sinogram_fan_id)
#     astra.projector.delete(proj_fan_id)
#     rec_fan[rec_fan < 0] = 0
#     astra.algorithm.clear()
#     astra.clear()
#     return rec_fan