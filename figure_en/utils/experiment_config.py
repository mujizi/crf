# -*- coding: UTF-8 -*-
import os
import yaml
from .exception import ParameterError
from .singleton import SingletonType


class ExperimentConfig(metaclass=SingletonType):
    default_config_path = os.path.join(os.path.dirname(__file__), '../../config/experiment/config.yml')

    def __init__(self, experiment_config=None):
        if experiment_config:
            if isinstance(experiment_config, str):
                if not os.path.exists(experiment_config):
                    experiment_config = {}
                    # raise FileNotFoundError('config file {0} is not existed'.format(experiment_config))
                else:
                    experiment_config = yaml.load(open(self.default_config_path).read())
            elif not isinstance(experiment_config, dict):
                raise ParameterError('experiment config is not dict')
        else:
            if not os.path.exists(self.default_config_path):
                experiment_config = {}
            else:
                experiment_config = yaml.load(open(self.default_config_path).read())

        self.experiment_config = experiment_config

    def __getitem__(self, item):
        return self.experiment_config[item]

    def __setitem__(self, key, value):
        self.experiment_config[key] = value

    def dump_to_file(self, dest_filename):
        pass
