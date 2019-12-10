# -*- coding: UTF-8 -*-
import os
import json
from .exception import ParameterError


def set_env(*args, **kwargs):
    """
    set environment variables, can be set in non-keyword parameter or keyword parameter
    (if non-keyword and keyword parameters are set in same time, set the variables in turn.)

    :param args: environment variables dict
    :param kwargs: keyword parameter, must have name and val key, other parameter will be ignored
    :return: None
    """
    if len(args) == 0 and len(kwargs) == 0:
        raise ParameterError('parameter is empty')
    if len(args) > 1:
        raise ParameterError('parameter count just allow 1')

    if not isinstance(args[0], dict):
        raise ParameterError('env parameters are not dict.')

    env_dict = args[0]

    for env_name, env_val in env_dict.items():
        os.environ[env_name] = json.dumps(env_val, ensure_ascii=False)

    if len(kwargs):
        if 'name' not in kwargs or 'val' not in kwargs:
            raise Exception('key parameters must be in name and val.')

        os.environ[kwargs['name']] = kwargs['val']


__EXPERIMENT_CONFIG_VARIABLE_NAME = 'experiment'


def set_experiment_envs(*, config=None, name=None, val=None):
    if not config and not name and not val:
        set_env({__EXPERIMENT_CONFIG_VARIABLE_NAME: {}})
    else:
        env_str = os.environ.get(__EXPERIMENT_CONFIG_VARIABLE_NAME)
        if not env_str:
            env_dict = {}
        else:
            env_dict = json.loads(env_str)
        if config:
            for config_name in config:
                if not isinstance(config_name, str):
                    raise Exception('experiment parameter name must be string')
            env_dict.update(config)
        if name is not None and val is not None:
            if not isinstance(name, str):
                raise Exception('experiment parameter name must be string')
            env_dict[name] = val
        set_env({__EXPERIMENT_CONFIG_VARIABLE_NAME: env_dict})


def get_experiment_env(name):
    if not isinstance(name, str):
        raise ParameterError('name is not string')
    if not os.environ.get(__EXPERIMENT_CONFIG_VARIABLE_NAME):
        set_experiment_envs()
    return json.loads(os.environ[__EXPERIMENT_CONFIG_VARIABLE_NAME]).get(name)
