# -*- coding: UTF-8 -*-
"""data process script includes some data process logic"""
from figure_en.api_model import Model
from figure_en.utils.constant import *
from figure_en.data_process.prepare_experiment_data import *


def run_batch():
    model = Model()
    model.run({'text': 'Your Content'})


if __name__ == '__main__':
    data_preparation(DATA_DIR + 'training_ori.json', TRAINING_FILE)
