import copy
import torch
import os
import abc

from DBWToolbox.tools import save_image2tif
from DBWToolbox.showresult import write_excel
import numpy as np
from os.path import join as ospj
import time
import statistics as sta
from DBWToolbox.tools import seconds2time


class SolverBase(metaclass=abc.ABCMeta):
    def __init__(self, root_save_dir='', **kwargs):
        self.arge = kwargs
        self.init_attr(root_save_dir, **kwargs)
        self.init_slover(**kwargs)
        self.init_dir()
        self.__init_resume(**kwargs)

    @abc.abstractmethod
    def init_slover(self, **kwargs):
        pass

    def __init_resume(self, **kwargs):
        if 'resume_epoch' not in kwargs.keys() or kwargs['resume_epoch'] == -1:
            self.resume_epoch = -1
            self.start_epoch = 0
        else:
            self.resume_epoch = kwargs['resume_epoch']
            self.resume(epoch=self.resume_epoch)
            self.start_epoch = self.resume_epoch

    def init_attr(self, default_save_dir, **kwargs):
        self.current_epoch = 0
        self.default_save_dir = default_save_dir
        self.num_epochs = kwargs['num_epochs']
        self.batch_size = kwargs['batch_size']
        self.checkpoint_pool = {}
        self.metrics_pool = {}
        self.test_epoch = kwargs['test_epoch']
        if 'print_n_epoch' in kwargs.keys() and kwargs['print_n_epoch'] != -1:
            self.print_n_epoch = kwargs['print_n_epoch']
        else:
            self.print_n_epoch = -1

        if 'is_save' in kwargs.keys():
            self.is_save = kwargs['is_save']
        else:
            self.is_save = True

        self.init_metrics()
        if 'device' in kwargs.keys():
            self.device = torch.device(kwargs['device'])
        else:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    def register_save_checkpoint(self, key, value):
        if key in self.checkpoint_pool.keys():
            print('{} already exist in checkpoint pool. Old one will be replaced by new one'.format(key),)
        self.checkpoint_pool.update({key: value})

    def register_save_metrics(self, key, value):
        if key in self.metrics_pool.keys():
            # self.metrics_pool[key] = self.combine_dict([self.metrics_pool, {key: value}])
            print('{} already exist in metrics pool. Old one will be replaced by new one!'.format(key))
        self.metrics_pool.update({key: value})

    def init_metrics(self):
        self.lrs = []
        self.register_save_metrics('lrs', self.lrs)

        self.train_ssim = []
        self.register_save_metrics('train_ssim', self.train_ssim)
        self.train_mse = []
        self.register_save_metrics('train_mse', self.train_mse)

        self.validation_loss = []
        self.register_save_metrics('validation_loss', self.validation_loss)
        self.validation_ssim = []
        self.register_save_metrics('validation_ssim', self.validation_ssim)
        self.validation_mse = []
        self.register_save_metrics('validation_mse', self.validation_mse)

        self.test_ssim = []
        self.register_save_metrics('test_ssim', self.test_ssim)
        self.test_mse = []
        self.register_save_metrics('test_mse', self.test_mse)

    def init_dir(self, hyperparam_path=''):
        if self.is_save == False:
            return
        self.checkpoint_path = ospj(self.default_save_dir, hyperparam_path, 'check_point')
        self.metrics_path = ospj(self.default_save_dir, hyperparam_path, 'metrics')
        self.result_path = ospj(self.default_save_dir, hyperparam_path, 'result_path')

        os.makedirs(self.checkpoint_path, exist_ok=True)
        os.makedirs(self.metrics_path, exist_ok=True)
        os.makedirs(self.result_path, exist_ok=True)

        # self.fig_path = os.path.join(self.default_save_dir, hyperparam_path, 'fig')
        # os.makedirs(self.fig_path, exist_ok=True)

    def get_checkpoint_name(self, **kwargs):
        return 'Model_epoch{}.ckpt'.format(kwargs['epoch'])

    def get_metrics_name(self, **kwargs):
        return 'Metrics_epoch{}'.format(kwargs['epoch'])

    def resume(self, **kwargs):
        metrics = self.load_metrics(**kwargs)
        self.load_metrics_attr(metrics)
        # self.init_metrics()
        self.load_checkpoint(**kwargs)

    def save_checkpoint(self, **kwargs):
        if self.is_save == False:
            return
        checkpoint_name = self.get_checkpoint_name(**kwargs)
        print('save model in {}'.format(os.path.join(self.checkpoint_path, checkpoint_name)))
        f = os.path.join(self.checkpoint_path, checkpoint_name)
        checkpoints = {}
        for key in self.checkpoint_pool.keys():
            checkpoints[key] = self.checkpoint_pool[key].state_dict()
        torch.save(checkpoints, f)

    def load_checkpoint(self, **kwargs):
        checkpoint_name = self.get_checkpoint_name(**kwargs)
        f = os.path.join(self.checkpoint_path, checkpoint_name)
        checkpoint = torch.load(f)
        return checkpoint

    def save_metrics(self, **kwargs):
        if self.is_save == False:
            return
        metrics_name = self.get_metrics_name(**kwargs)
        print('save metrics in {}'.format(os.path.join(self.checkpoint_path, metrics_name)))
        metrics = {}
        for key in self.metrics_pool.keys():
            if isinstance(self.metrics_pool[key], list):
                metrics[key] = np.array(self.metrics_pool[key])
        f = os.path.join(self.metrics_path, metrics_name)
        np.save(f, metrics)

    def load_metrics(self, **kwargs):
        metrics_name = self.get_metrics_name(**kwargs)
        if not metrics_name.endswith('.npy'):
            metrics_name += '.npy'
        f = os.path.join(self.metrics_path, metrics_name)
        metrics = np.load(f, allow_pickle=True).item()
        for key in metrics.keys():
            if type(metrics[key]) is np.ndarray:
                metrics[key] = metrics[key].tolist()
        return metrics

    def load_metrics_attr(self, metrics):
        self.lrs.extend(metrics['lrs'])

        self.train_ssim.extend(metrics['train_ssim'])
        self.train_mse.extend(metrics['train_mse'])

        self.validation_loss.extend(metrics['validation_loss'])
        self.validation_ssim.extend(metrics['validation_ssim'])
        self.validation_mse.extend(metrics['validation_mse'])

        self.test_ssim.extend(metrics['test_ssim'])
        self.test_mse.extend(metrics['test_mse'])
        return metrics


    def training_begin(self):
        return None

    def training_epoch_begin(self):
        return None

    def training_step(self, batch, batch_idx):
        return None

    def training_epoch_end(self, outputs):
        return None

    def training_end(self):
        return None


    def validation_begin(self):
        return None

    def validation_epoch_begin(self):
        return None

    def validation_step(self, batch, batch_idx):
        return None

    def validation_epoch_end(self, outputs):
        return None

    def validation_end(self):
        return None

    def test_step(self, batch, batch_idx):
        return None

    def test_begin(self):
        return None

    def test_end(self, outputs):
        return None

    def print_every_n_epoch(self, train_outputs=None, validation_outputs=None, time_cost=0.0):
        return None

    def save_model(self, train_outputs=None, validation_outputs=None,):
        pass

    """Combine dicts, combine values with same key to a list instead of overwirting the value"""
    def combine_dict(self, dicts: list):
        result_dict = {}
        for d in dicts:
            for k, v in d.items():
                try:
                    result_dict.setdefault(k, []).extend(v)
                except TypeError:
                    result_dict[k].append(v)
        return result_dict

    def train(self, train_loader, validation_loader=None):
        start = time.time()
        start_epoch = 1
        if validation_loader is None:
            print('Validation loader is None, validation step will not be executed')
        self.training_begin()
        if self.resume_epoch != -1:
            start_epoch = self.resume_epoch+1
        epoch_start = time.time()
        # ---------------------- train one epoch --------------------------------------
        for epoch in range(start_epoch, self.num_epochs+1):
            self.current_epoch = epoch
            train_epoch_metrics = {}
            self.training_epoch_begin()
            for batch_idx, batch in enumerate(train_loader):
                for i in range(len(batch)):
                    item = batch[i]
                    if isinstance(item, torch.Tensor):
                        batch[i] = batch[i].to(self.device)
                step_metrics = self.training_step(batch, batch_idx)
                assert isinstance(step_metrics, dict), "training_step should return dict"
                train_epoch_metrics = self.combine_dict([step_metrics, train_epoch_metrics])
            self.training_epoch_end(train_epoch_metrics)
            # ---------------------- validate one epoch --------------------------------------
            with torch.no_grad():
                validation_epoch_metrics = None
                if validation_loader is not None:
                    validation_epoch_metrics = {}
                    self.validation_epoch_begin()
                    for batch_idx, batch in enumerate(validation_loader):
                        for i in range(len(batch)):
                            item = batch[i]
                            if isinstance(item, torch.Tensor):
                                batch[i] = batch[i].to(self.device)
                        step_metrics = self.validation_step(batch, batch_idx)
                        assert isinstance(step_metrics, dict), "validation_step should return dict"
                        validation_epoch_metrics = self.combine_dict([step_metrics, validation_epoch_metrics])
                    self.validation_epoch_end(validation_epoch_metrics)
            # print something in every n epoch(s) if needed
            if self.print_n_epoch != -1 and epoch % self.print_n_epoch == 0:
                epoch_end = time.time()
                self.print_every_n_epoch(train_outputs=train_epoch_metrics, validation_outputs=validation_epoch_metrics,
                                         time_cost=epoch_end-epoch_start)
                epoch_start = time.time()
            self.save_model(train_outputs=train_epoch_metrics, validation_outputs=validation_epoch_metrics)

        end = time.time()
        print('Training totally cost {}'.format(seconds2time(end-start)))
        self.training_end()

    def _test_step(self, batch, batch_idx):
        for i in range(len(batch)):
            item = batch[i]
            if isinstance(item, torch.Tensor):
                batch[i] = batch[i].to(self.device)
        test_result = self.test_step(batch, batch_idx)
        step_test_metrics = None
        if 'metric_kwargs' in test_result.keys():
            step_test_metrics = test_result['metric_kwargs']
        if 'save_result' in test_result.keys():
            assert self.batch_size == 1, 'batch size should be 1 if you want to save image'
            self.save_result(**test_result['save_result'])
        return step_test_metrics

    def save_result(self, filename, image):
        if self.is_save == False:
            return
        save_image2tif(image, filepath=self.result_path, filename=filename)

    def combine_test_metrics(self, step_test_metrics, test_metrics):
        for method_name in step_test_metrics.keys():
            test_method = test_metrics.setdefault(method_name, {})
            for metrics_name in step_test_metrics[method_name].keys():
                test_metrics_list = test_method.setdefault(metrics_name, [])
                test_metrics_list.append(step_test_metrics[method_name][metrics_name])
        return test_metrics

    def test(self, test_loader, **kwargs):
        with torch.no_grad():
            self.test_begin()
            start = time.time()
            assert self.test_epoch > 0, "Test epoch should bigger than zero"
            self.load_checkpoint(epoch=kwargs['test_epoch'], **kwargs)
            test_metrics = {}
            for batch_idx, batch in enumerate(test_loader):
                step_test_metrics = self._test_step(batch, batch_idx)
                if step_test_metrics is not None:
                    test_metrics = self.combine_test_metrics(step_test_metrics, test_metrics)
            test_metrics = self.compute_test_metrics(test_metrics)
            self.save_test_metrics(test_metrics)
            self.test_end(test_metrics)
            end = time.time()
            print('test cost {} s'.format(end-start))


    def save_test_metrics(self, test_metrics, **kwargs):
        if self.is_save == False:
            return
        write_excel(ospj(self.metrics_path, 'test_metrics.xlsx'), data_list=test_metrics, index='method')

    def compute_test_metrics(self, test_metrics, is_print=False):
        methods = list(test_metrics.keys())
        metrics = list(test_metrics[methods[0]].keys())
        data_list = []
        for method in methods:
            data = {}
            for metric in metrics:
                mean = sta.mean(test_metrics[method][metric])
                if len(test_metrics[method][metric]) == 1:
                    std = 0
                else:
                    std = sta.stdev(test_metrics[method][metric])
                data['method'] = method
                data[metric] = '{} ± {}'.format(mean, std)
                if is_print:
                    print('{} {} is {} ± {}'.format(method, metric, mean, std))
            data_list.append(data)
        return data_list



