# -*- coding: UTF-8 -*-
from unittest import TestCase
from figure_en.utils.experiment_config import *


class TestExperimentConfig(TestCase):
    def test_experiment_config(self):
        config = ExperimentConfig()
        print(config)
