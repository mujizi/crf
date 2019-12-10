# -*- coding: UTF-8 -*-
"""encapsulate CRF features"""
from .utils.constant import *
import re

Dight = re.compile('\d')


class CRFFeature(object):
    feature_sets = []

    def __init__(self, tokens):
        self.tokens = tokens
        self.token_texts = [token['text'] for token in tokens]
        self.length = len(self.tokens)

    def word2feature(self, idx):
        def spe_symbol(text):
            q = ['^', "&", '$', '=']
            for i in q:
                if i in text:
                    tag = True
                    break
                else:
                    tag = False
            return tag

        def exist_dight(text):
            return str(bool(Dight.search(text)))

        def conjunction(text):
            s = ['and', 'or', 'as', ',']
            for i in s:
                if i == text:
                    tag = True
                    break
                else:
                    tag = False
            return tag

        all_features = {
            # id feature
            'word.exist_digit()': exist_dight(self.tokens[idx]['text']),
            'word[-3:]': self.tokens[idx]['text'][-3:],
            'word[-2:]': self.tokens[idx]['text'][-2:],
            'postag': self.tokens[idx]['pos_tag'],
            'spe_symbol': spe_symbol(self.tokens[idx]['text']),
            'conjunction': conjunction(self.tokens[idx]['text']),

            # part_name
            'word': self.tokens[idx]['text'],
            'word.lower()': self.tokens[idx]['text'].islower(),
            'word.isupper()': self.tokens[idx]['text'].isupper(),
        }

        if idx > 0:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            all_features.update({
                '-1:format_word': ' '.join([word_pre_1, word]),
                '-1:format_postag': ' '.join([postag_pre_1, postag]),
                '-2:format_exdigit()': ' '.join([exdigit_pre_1, exdigit]),
                'exdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
            })

        if idx > 1:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            all_features.update({
                '-2:format_word': ' '.join([word_pre_2, word_pre_1, word]),
                '-2:format_postag': ' '.join([postag_pre_2, postag_pre_1, postag]),
                '-2:format_exdigit()': ' '.join([exdigit_pre_2, exdigit_pre_1, exdigit]),
                'isdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
            })

        if idx > 2:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            word_pre_3 = self.tokens[idx - 3]['text']
            postag_pre_3 = self.tokens[idx - 3]['pos_tag']
            exdigit_pre_3 = exist_dight(self.tokens[idx - 3]['text'])
            all_features.update({
                '-3:format_word': ' '.join([word_pre_3, word_pre_2, word_pre_1, word]),
                '-3:format_postag': ' '.join([postag_pre_3, postag_pre_2, postag_pre_1, postag]),
                '-3:format_exdigit()': ' '.join([exdigit_pre_3, exdigit_pre_2, exdigit_pre_1, exdigit]),
                'isdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
                '-3:exdigit': exdigit_pre_3,
            })

        if idx > 3:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            word_pre_3 = self.tokens[idx - 3]['text']
            postag_pre_3 = self.tokens[idx - 3]['pos_tag']
            exdigit_pre_3 = exist_dight(self.tokens[idx - 3]['text'])
            word_pre_4 = self.tokens[idx - 4]['text']
            postag_pre_4 = self.tokens[idx - 4]['pos_tag']
            exdigit_pre_4 = exist_dight(self.tokens[idx - 4]['text'])
            all_features.update({
                '-4:format_word': ' '.join([word_pre_4, word_pre_3, word_pre_2, word_pre_1, word]),
                '-4:format_postag': ' '.join([postag_pre_4, postag_pre_3, postag_pre_2, postag_pre_1, postag]),
                '-4:format_exdigit()': ' '.join([exdigit_pre_4, exdigit_pre_3, exdigit_pre_2, exdigit_pre_1, exdigit]),
                'exdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
                '-3:exdigit': exdigit_pre_3,
                '-4:exdigit': exdigit_pre_4,
            })

        if idx > 4:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            word_pre_3 = self.tokens[idx - 3]['text']
            postag_pre_3 = self.tokens[idx - 3]['pos_tag']
            exdigit_pre_3 = exist_dight(self.tokens[idx - 3]['text'])
            word_pre_4 = self.tokens[idx - 4]['text']
            postag_pre_4 = self.tokens[idx - 4]['pos_tag']
            exdigit_pre_4 = exist_dight(self.tokens[idx - 4]['text'])
            word_pre_5 = self.tokens[idx - 5]['text']
            postag_pre_5 = self.tokens[idx - 5]['pos_tag']
            exdigit_pre_5 = exist_dight(self.tokens[idx - 5]['text'])
            all_features.update({
                '-5:format_word': ' '.join([word_pre_5, word_pre_4, word_pre_3, word_pre_2, word_pre_1, word]),
                '-5:format_postag': ' '.join(
                    [postag_pre_5, postag_pre_4, postag_pre_3, postag_pre_2, postag_pre_1, postag]),
                '-5:format_exdigit()': ' '.join(
                    [exdigit_pre_5, exdigit_pre_4, exdigit_pre_3, exdigit_pre_2, exdigit_pre_1, exdigit]),
                'isdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
                '-3:exdigit': exdigit_pre_3,
                '-4:exdigit': exdigit_pre_4,
                '-5:exdigit': exdigit_pre_5
            })

        if idx < (self.length - 1):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            all_features.update({
                '+1:word.lower()': word_latter_1.islower(),
                '+1:word.upper()': word_latter_1.isupper(),
                '+1:postag': postag_latter_1,
                '+1:word.exdigit()': exdigit_latter_1,
                '+1:format_exdigit': ' '.join([exdigit, exdigit_latter_1]),
                '-1:format_word': ' '.join([word_latter_1, word]),
                '-1:format_postag': ' '.join([postag_latter_1, postag]),
            })

        if idx < (self.length - 2):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            exdigit_latter_2 = exist_dight(self.tokens[idx + 2]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            word_latter_2 = self.tokens[idx + 2]['text']
            postag_latter_2 = self.tokens[idx + 2]['pos_tag']
            all_features.update({
                '+2:word.lower()': word_latter_2.islower(),
                '+2:word.upper()': word_latter_2.isupper(),
                '+2:postag': postag_latter_2,
                '+2:word.exdigit()': exdigit_latter_2,
                '+3:format_exdigit': ' '.join([exdigit, exdigit_latter_1, exdigit_latter_2]),
                '+2:format_word': ' '.join([word, word_latter_1, word_latter_2]),
                '+2:format_postag': ' '.join([postag, postag_latter_1, postag_latter_2]),
            })

        if idx < (self.length - 3):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            word_latter_2 = self.tokens[idx + 2]['text']
            postag_latter_2 = self.tokens[idx + 2]['pos_tag']
            word_latter_3 = self.tokens[idx + 3]['text']
            postag_latter_3 = self.tokens[idx + 3]['pos_tag']
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            exdigit_latter_2 = exist_dight(self.tokens[idx + 2]['text'])
            exdigit_latter_3 = exist_dight(self.tokens[idx + 3]['text'])

            all_features.update({
                '+3:word.lower()': word_latter_3.islower(),
                '+3:word.upper()': word_latter_3.isupper(),
                '+3:postag': postag_latter_3,
                '+3:word.isdigit()': word_latter_3.isdigit(),
                '+3:format_exdigit': ' '.join([exdigit, exdigit_latter_1, exdigit_latter_2, exdigit_latter_3]),
                '+3:format_word': ' '.join([word, word_latter_1, word_latter_2, word_latter_3]),
                '+3:format_postag': ' '.join([postag, postag_latter_1, postag_latter_2, postag_latter_3]),
            })

        if idx < (self.length - 4):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            word_latter_2 = self.tokens[idx + 2]['text']
            postag_latter_2 = self.tokens[idx + 2]['pos_tag']
            word_latter_3 = self.tokens[idx + 3]['text']
            postag_latter_3 = self.tokens[idx + 3]['pos_tag']
            word_latter_4 = self.tokens[idx + 4]['text']
            postag_latter_4 = self.tokens[idx + 4]['pos_tag']
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            exdigit_latter_2 = exist_dight(self.tokens[idx + 2]['text'])
            exdigit_latter_3 = exist_dight(self.tokens[idx + 3]['text'])
            exdigit_latter_4 = exist_dight(self.tokens[idx + 4]['text'])

            all_features.update({
                '+4:word.lower()': word_latter_4.islower(),
                '+4:word.upper()': word_latter_4.isupper(),
                '+4:postag': postag_latter_4,
                '+4:word.exdigit()': exdigit_latter_4,
                '+4:format_exdigit': ' '.join(
                    [exdigit, exdigit_latter_1, exdigit_latter_2, exdigit_latter_3, exdigit_latter_4]),
                '+4:format_word': ' '.join([word, word_latter_1, word_latter_2, word_latter_3, word_latter_4]),
                '+4:format_postag': ' '.join(
                    [postag, postag_latter_1, postag_latter_2, postag_latter_3, postag_latter_4]),
            })

        return all_features

    def word2feature_experiment(self, idx):
        def spe_symbol(text):
            q = ['^', "&", '$', '=']
            for i in q:
                if i in text:
                    tag = True
                    break
                else:
                    tag = False
            return tag

        def exist_dight(text):
            return str(bool(Dight.search(text)))

        def conjunction(text):
            s = ['and', 'or', 'as', ',']
            for i in s:
                if i == text:
                    tag = True
                    break
                else:
                    tag = False
            return tag

        all_features = {
            # id feature
            'word.exist_digit()': exist_dight(self.tokens[idx]['text']),
            'word[-3:]': self.tokens[idx]['text'][-3:],
            'word[-2:]': self.tokens[idx]['text'][-2:],
            'postag': self.tokens[idx]['pos_tag'],
            'spe_symbol': spe_symbol(self.tokens[idx]['text']),
            'conjunction': conjunction(self.tokens[idx]['text']),

            # part_name
            'word': self.tokens[idx]['text'],
            'word.lower()': self.tokens[idx]['text'].islower(),
            'word.isupper()': self.tokens[idx]['text'].isupper(),
        }

        if idx > 0:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            all_features.update({
                '-1:format_word': ' '.join([word_pre_1, word]),
                '-1:format_postag': ' '.join([postag_pre_1, postag]),
                '-2:format_exdigit()': ' '.join([exdigit_pre_1, exdigit]),
                'exdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
            })

        if idx > 1:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            all_features.update({
                '-2:format_word': ' '.join([word_pre_2, word_pre_1, word]),
                '-2:format_postag': ' '.join([postag_pre_2, postag_pre_1, postag]),
                '-2:format_exdigit()': ' '.join([exdigit_pre_2, exdigit_pre_1, exdigit]),
                'isdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
            })

        if idx > 2:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            word_pre_3 = self.tokens[idx - 3]['text']
            postag_pre_3 = self.tokens[idx - 3]['pos_tag']
            exdigit_pre_3 = exist_dight(self.tokens[idx - 3]['text'])
            all_features.update({
                '-3:format_word': ' '.join([word_pre_3, word_pre_2, word_pre_1, word]),
                '-3:format_postag': ' '.join([postag_pre_3, postag_pre_2, postag_pre_1, postag]),
                '-3:format_exdigit()': ' '.join([exdigit_pre_3, exdigit_pre_2, exdigit_pre_1, exdigit]),
                'isdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
                '-3:exdigit': exdigit_pre_3,
            })

        if idx > 3:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            word_pre_3 = self.tokens[idx - 3]['text']
            postag_pre_3 = self.tokens[idx - 3]['pos_tag']
            exdigit_pre_3 = exist_dight(self.tokens[idx - 3]['text'])
            word_pre_4 = self.tokens[idx - 4]['text']
            postag_pre_4 = self.tokens[idx - 4]['pos_tag']
            exdigit_pre_4 = exist_dight(self.tokens[idx - 4]['text'])
            all_features.update({
                '-4:format_word': ' '.join([word_pre_4, word_pre_3, word_pre_2, word_pre_1, word]),
                '-4:format_postag': ' '.join([postag_pre_4, postag_pre_3, postag_pre_2, postag_pre_1, postag]),
                '-4:format_exdigit()': ' '.join([exdigit_pre_4, exdigit_pre_3, exdigit_pre_2, exdigit_pre_1, exdigit]),
                'exdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
                '-3:exdigit': exdigit_pre_3,
                '-4:exdigit': exdigit_pre_4,
            })

        if idx > 4:
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_pre_1 = self.tokens[idx - 1]['text']
            postag_pre_1 = self.tokens[idx - 1]['pos_tag']
            exdigit_pre_1 = exist_dight(self.tokens[idx - 1]['text'])
            word_pre_2 = self.tokens[idx - 2]['text']
            postag_pre_2 = self.tokens[idx - 2]['pos_tag']
            exdigit_pre_2 = exist_dight(self.tokens[idx - 2]['text'])
            word_pre_3 = self.tokens[idx - 3]['text']
            postag_pre_3 = self.tokens[idx - 3]['pos_tag']
            exdigit_pre_3 = exist_dight(self.tokens[idx - 3]['text'])
            word_pre_4 = self.tokens[idx - 4]['text']
            postag_pre_4 = self.tokens[idx - 4]['pos_tag']
            exdigit_pre_4 = exist_dight(self.tokens[idx - 4]['text'])
            word_pre_5 = self.tokens[idx - 5]['text']
            postag_pre_5 = self.tokens[idx - 5]['pos_tag']
            exdigit_pre_5 = exist_dight(self.tokens[idx - 5]['text'])
            all_features.update({
                '-5:format_word': ' '.join([word_pre_5, word_pre_4, word_pre_3, word_pre_2, word_pre_1, word]),
                '-5:format_postag': ' '.join([postag_pre_5, postag_pre_4, postag_pre_3, postag_pre_2, postag_pre_1, postag]),
                '-5:format_exdigit()': ' '.join([exdigit_pre_5, exdigit_pre_4, exdigit_pre_3, exdigit_pre_2, exdigit_pre_1, exdigit]),
                'isdigit': exdigit,
                '-1:exdigit': exdigit_pre_1,
                '-2:exdigit': exdigit_pre_2,
                '-3:exdigit': exdigit_pre_3,
                '-4:exdigit': exdigit_pre_4,
                '-5:exdigit': exdigit_pre_5
            })

        if idx < (self.length - 1):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            all_features.update({
                '+1:word.lower()': word_latter_1.islower(),
                '+1:word.upper()': word_latter_1.isupper(),
                '+1:postag': postag_latter_1,
                '+1:word.exdigit()': exdigit_latter_1,
                '+1:format_exdigit': ' '.join([exdigit, exdigit_latter_1]),
                '-1:format_word': ' '.join([word_latter_1, word]),
                '-1:format_postag': ' '.join([postag_latter_1, postag]),
            })

        if idx < (self.length - 2):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            exdigit_latter_2 = exist_dight(self.tokens[idx + 2]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            word_latter_2 = self.tokens[idx + 2]['text']
            postag_latter_2 = self.tokens[idx + 2]['pos_tag']
            all_features.update({
                '+2:word.lower()': word_latter_2.islower(),
                '+2:word.upper()': word_latter_2.isupper(),
                '+2:postag': postag_latter_2,
                '+2:word.exdigit()': exdigit_latter_2,
                '+3:format_exdigit': ' '.join([exdigit, exdigit_latter_1, exdigit_latter_2]),
                '+2:format_word': ' '.join([word, word_latter_1, word_latter_2]),
                '+2:format_postag': ' '.join([postag, postag_latter_1, postag_latter_2]),
            })

        if idx < (self.length - 3):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            word_latter_2 = self.tokens[idx + 2]['text']
            postag_latter_2 = self.tokens[idx + 2]['pos_tag']
            word_latter_3 = self.tokens[idx + 3]['text']
            postag_latter_3 = self.tokens[idx + 3]['pos_tag']
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            exdigit_latter_2 = exist_dight(self.tokens[idx + 2]['text'])
            exdigit_latter_3 = exist_dight(self.tokens[idx + 3]['text'])

            all_features.update({
                '+3:word.lower()': word_latter_3.islower(),
                '+3:word.upper()': word_latter_3.isupper(),
                '+3:postag': postag_latter_3,
                '+3:word.isdigit()': word_latter_3.isdigit(),
                '+3:format_exdigit': ' '.join([exdigit, exdigit_latter_1, exdigit_latter_2, exdigit_latter_3]),
                '+3:format_word': ' '.join([word, word_latter_1, word_latter_2, word_latter_3]),
                '+3:format_postag': ' '.join([postag, postag_latter_1, postag_latter_2, postag_latter_3]),
            })

        if idx < (self.length - 4):
            word = self.tokens[idx]['text']
            postag = self.tokens[idx]['pos_tag']
            exdigit = exist_dight(self.tokens[idx]['text'])
            word_latter_1 = self.tokens[idx + 1]['text']
            postag_latter_1 = self.tokens[idx + 1]['pos_tag']
            word_latter_2 = self.tokens[idx + 2]['text']
            postag_latter_2 = self.tokens[idx + 2]['pos_tag']
            word_latter_3 = self.tokens[idx + 3]['text']
            postag_latter_3 = self.tokens[idx + 3]['pos_tag']
            word_latter_4 = self.tokens[idx + 4]['text']
            postag_latter_4 = self.tokens[idx + 4]['pos_tag']
            exdigit_latter_1 = exist_dight(self.tokens[idx + 1]['text'])
            exdigit_latter_2 = exist_dight(self.tokens[idx + 2]['text'])
            exdigit_latter_3 = exist_dight(self.tokens[idx + 3]['text'])
            exdigit_latter_4 = exist_dight(self.tokens[idx + 4]['text'])

            all_features.update({
                '+4:word.lower()': word_latter_4.islower(),
                '+4:word.upper()': word_latter_4.isupper(),
                '+4:postag': postag_latter_4,
                '+4:word.exdigit()': exdigit_latter_4,
                '+4:format_exdigit': ' '.join([exdigit, exdigit_latter_1, exdigit_latter_2, exdigit_latter_3, exdigit_latter_4]),
                '+4:format_word': ' '.join([word, word_latter_1, word_latter_2, word_latter_3, word_latter_4]),
                '+4:format_postag': ' '.join([postag, postag_latter_1, postag_latter_2, postag_latter_3, postag_latter_4]),
            })


        features = {feat: feat_val for feat, feat_val in all_features.items() if feat in self.feature_sets}
        print(features)
        return features

    def sent2feature(self):
        if EXP_CONFIG['experiment']:
            return [self.word2feature_experiment(i) for i in range(self.length)]
        else:
            return (self.word2feature(i) for i in range(self.length))


