def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton

@singleton
class TuneHYParameter(object):
    def __init__(self, hy_parameters_range: dict):
        super(TuneHYParameter, self).__init__()
        self.hy_parameters_range = hy_parameters_range


