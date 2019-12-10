# -*- coding: UTF-8 -*-
from unittest import TestCase
from figure_en.utils.utils import *


class TestUtils(TestCase):
    def test_get_index_char2word(self):
        tokens = [{'text': '我们', 'start': 0, 'end': 2}, {'text': '来自', 'start': 2, 'end': 4},
                  {'text': '智慧芽', 'start': 4, 'end': 7}]
        self.assertEqual(get_index_char2word(tokens, 1), 0)
        self.assertEqual(get_index_char2word(tokens, 2), 1)
        self.assertEqual(get_index_char2word(tokens, 3), 1)
        self.assertEqual(get_index_char2word(tokens, 5), 2)
        self.assertEqual(get_index_char2word(tokens, 6), 2)
        self.assertRaises(IndexError, get_index_char2word, tokens, 7)

    def test_replace_item_in_list(self):
        old_list1 = list(range(10))
        replaced_items1 = [(3, 12)]
        new_list1 = replace_item_in_list(old_list1, replaced_items1)
        true_list1 = old_list1.copy()
        true_list1[3] = 12
        self.assertEqual(true_list1, new_list1)

        replaced_items2 = [(3, [1, 2])]
        new_list2 = replace_item_in_list(old_list1, replaced_items2, extend_list=True)
        true_list2 = old_list1.copy()
        true_list2.pop(3)
        true_list2.insert(3, 1)
        true_list2.insert(4, 2)
        self.assertEqual(true_list2, new_list2)

        new_list3 = replace_item_in_list(old_list1, replaced_items2, extend_list=False)
        true_list3 = old_list1.copy()
        true_list3.pop(3)
        true_list3.insert(3, [1, 2])
        self.assertEqual(true_list3, new_list3)

    def test_replace_extname(self):
        src_name1 = '/mnt/data1/a.json'
        true_name1 = '/mnt/data1/a.conll'
        self.assertEqual(true_name1, replace_extname(src_name1, 'conll'))
        self.assertEqual(true_name1, replace_extname(src_name1, '.conll'))
