from figure_en.data_process.prepare_experiment_data import *


build_oov_data('/home/patsnap/PycharmProjects/crf/ner_figure_part/data/test.json', '/home/patsnap/PycharmProjects/crf/ner_figure_part/data/training.json')
build_oov_data('/home/patsnap/PycharmProjects/crf/ner_figure_part/data/validation.json', '/home/patsnap/PycharmProjects/crf/ner_figure_part/data/training.json')
