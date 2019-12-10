# -*- coding: UTF-8 -*-
import json
from unittest import TestCase
from figure_en.utils.io import *
from tests import TEST_DATA_DIR


class TestIoWrapper(TestCase):

    def test_read_lines_in_file(self):
        filename = TEST_DATA_DIR + 'a.txt'
        lines1 = read_lines(filename)
        self.assertEqual(['first line', 'second line'], lines1)
        lines2 = read_lines(filename, strip=False)
        self.assertEqual(['first line', 'second line', ' '], lines2)
        lines3 = read_lines(filename, filter_empty=False)
        self.assertEqual(['first line', '', 'second line', ''], lines3)
        lines4 = read_lines(filename, strip=False, filter_empty=False)
        self.assertEqual(['first line', '', 'second line', ' '], lines4)

    def test_read_file(self):
        filename = TEST_DATA_DIR+'a.txt'
        text = read_file(filename)
        self.assertEqual('first line\n\nsecond line\n \n', text)

    def test_write_file(self):
        dest_filename = TEST_DATA_DIR+'b.txt'
        text = "a\nb"
        write_file(dest_filename, text)
        dest_text = read_file(dest_filename)
        self.assertEqual(text, dest_text)

    def test_write_lines_to_file(self):
        lines = ['A', ' ', 'b', '']
        dest_filename = TEST_DATA_DIR+'c.txt'

        write_lines(dest_filename, lines, strip=True, filter_empty=True)
        lines1 = read_lines(dest_filename, strip=True, filter_empty=False)
        self.assertEqual(['A', 'b'], lines1)

        write_lines(dest_filename, lines, filter_empty=True)
        lines2 = read_lines(dest_filename, strip=False, filter_empty=False)
        self.assertEqual(['A', ' ', 'b'], lines2)

        write_lines(dest_filename, lines, strip=True)
        lines3 = read_lines(dest_filename, strip=False, filter_empty=False)
        self.assertEqual(['A', '', 'b', ''], lines3)

        write_lines(dest_filename, lines, strip=False, filter_empty=False)
        lines4 = read_lines(dest_filename, strip=False, filter_empty=False)
        self.assertEqual(['A', ' ', 'b', ''], lines4)

    def test_read_json_file(self):
        filename = TEST_DATA_DIR+'a.json'
        data = read_json(filename)
        true_data = {"a": 1, "b": "2", "c": [1, 2, 3]}
        self.assertEqual(true_data, data)

    def test_write_json_to_file(self):
        filename = TEST_DATA_DIR+'b.json'
        true_data = {"a": 1, "b": "2", "c": [1, 2, 3]}
        write_json(filename, true_data)
        data = read_json(filename)
        self.assertEqual(true_data, data)

    def test_read_jsonl(self):
        filename = TEST_DATA_DIR+'a.jsonl'
        item_list = read_jsonline(filename)
        true_list = [{'a': 1}, {'b': [1, 2, 3], 'a': 2}]
        self.assertEqual(true_list, item_list)

    def test_read_jsonline_lazy(self):
        filename = TEST_DATA_DIR + 'a.jsonl'
        for line in read_jsonline_lazy(filename):
            print(line)
