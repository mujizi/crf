# -*- coding: UTF-8 -*-
from unittest import TestCase
from figure_en.data_process.json2conll import *
from figure_en.data_process.conll2json import *
from tests import *


class TestJson2Conll(TestCase):

    def test_token_json2label(self):
        src_filename = TEST_DATA_DIR + 'a.conll'
        dest_filename = TEST_DATA_DIR + 'b.conll'
        sents = read_conll_file(src_filename)
        token_json2label(sents, dest_filename)
        self.assertEqual(read_file(dest_filename), read_file(src_filename))
