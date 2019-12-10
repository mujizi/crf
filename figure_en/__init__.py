# -*- coding: utf-8 -*-
import pkg_resources
from figure_en.api_model import Model

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'