# -*- coding: UTF-8 -*-
from unittest import TestCase
from figure_en.data_process.conll2json import *
from tests import TEST_DATA_DIR


class TestCoNLL2Json(TestCase):
    def test_conll2json(self):
        conll_filename = TEST_DATA_DIR + 'b.conll'
        json_filename = TEST_DATA_DIR + 'b.json'
        conll2json(conll_filename, json_filename)
