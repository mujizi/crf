# -*- coding: UTF-8 -*-
from unittest import TestCase
from figure_en.data_process.text_preprocess import *


class TestTextPreprocess(TestCase):
    def test_text_preprocess(self):
        raw_text1 = '\nゾレドロン酸\n\nゾレドロン酸'
        lines, mapper = text_preprocess(raw_text1, norm_text=True)
        line_spans = [(l['start'], l['end']) for l in lines]
        line_texts = [l['text'] for l in lines]
        self.assertEqual(['ゾレドロン酸', 'ゾレドロン酸'], line_texts)
        self.assertEqual([(1, 9), (11, 19)], line_spans)
        real_mapper = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7,
                       10: 8, 11: 9, 12: 9, 13: 10,
                       14: 11, 15: 11, 16: 12, 17: 13, 18: 14}
        self.assertEqual(real_mapper, mapper)

        lines, mapper = text_preprocess(raw_text1, norm_text=False, skip_empty=False)
        line_spans = [(l['start'], l['end']) for l in lines]
        line_texts = [l['text'] for l in lines]
        self.assertEqual(['', 'ゾレドロン酸', '', 'ゾレドロン酸'], line_texts)
        print(line_spans)
        self.assertEqual([(0, 0), (1, 7), (8, 8), (9, 15)], line_spans)
        # real_mapper = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8,
        #                11: 9, 12: 9, 13: 10, 14: 11, 15: 11, 16: 12, 17: 13, 18: 14}
        self.assertEqual(mapper, None)

        raw_text2 = 'ゾレドロン酸\n<div class="uspto">This figure </div> is good figure.\n这是\xa0一个化合物.'
        lines, mapper = text_preprocess(raw_text2, norm_text=True, skip_empty=False)
        line_spans = [(l['start'], l['end']) for l in lines]
        line_texts = [l['text'] for l in lines]
        self.assertEqual(['ゾレドロン酸', 'This figureis good figure.', '这是一个化合物.'],
                         line_texts)
        print(line_spans)
        self.assertEqual([(0, 8), (9, 35), (36, 44)], line_spans)
        real_mapper = {0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 26, 10: 27,
                       11: 28, 12: 29, 13: 30, 14: 31, 15: 32, 16: 33, 17: 34, 18: 35,
                       19: 36, 20: 45, 21: 46, 22: 47, 23: 48, 24: 49, 25: 50, 26: 51,
                       27: 52, 28: 53, 29: 54, 30: 55, 31: 56, 32: 57, 33: 58, 34: 59,
                       35: 60, 36: 61, 37: 62, 38: 64, 39: 65, 40: 66, 41: 67, 42: 68, 43: 69}
        self.assertEqual(real_mapper, mapper)

    def test_adjust_entity_offset(self):
        text = ' Hel lo.'
        entity_list = [{'entity': 'Hel lo', 'start': 1, 'end': len(text) - 1, 'type': 'generic'}]
        final_entity_list = [{'entity': 'Hel lo', 'start': 0, 'end': len(text) - 2, 'type': 'generic'}]
        ret_entity_list = adjust_entity_offset(entity_list, 0)
        self.assertEqual(final_entity_list, ret_entity_list)

        text2 = ' Hel lo'
        entity_list2 = [{'entity': 'Hel lo', 'start': 1, 'end': len(text2), 'type': 'generic'}]
        final_entity_list2 = [{'entity': 'Hello', 'start': 1, 'end': len(text2) - 1, 'type': 'generic'}]
        ret_entity_list2 = adjust_entity_offset(entity_list2, 4)
        self.assertEqual(final_entity_list2, ret_entity_list2)

    def test_replace_chars(self):
        text = ' Hel lo.'
        entity_list = [{'entity': 'Hel lo', 'start': 1, 'end': len(text) - 1, 'type': 'generic'}]
        final_entity_list = [{'entity': 'Hel lo', 'start': 0, 'end': len(text) - 2, 'type': 'generic'}]
        ret_entity_list = replace_chars(entity_list, 0, ' ', '', text)
        self.assertEqual(final_entity_list, ret_entity_list)

        text2 = ' Hel lo'
        entity_list2 = [{'entity': 'Hel lo', 'start': 1, 'end': len(text2), 'type': 'generic'}]
        final_entity_list2 = [{'entity': 'Hello', 'start': 1, 'end': len(text2) - 1, 'type': 'generic'}]
        ret_entity_list2 = replace_chars(entity_list2, 4, ' ', '', text2)
        self.assertEqual(final_entity_list2, ret_entity_list2)

        text3 = ' Hel lo'
        entity_list3 = [{'entity': 'Hel lo', 'start': 1, 'end': len(text3), 'type': 'generic'}]
        final_entity_list3 = [{'entity': '我l lo', 'start': 1, 'end': 6, 'type': 'generic'}]
        ret_entity_list3 = replace_chars(entity_list3, 0, ' He', ' 我', text3)
        self.assertEqual(final_entity_list3, ret_entity_list3)

        text4 = ' Hel lo'
        entity_list4 = [{'entity': 'Hel lo', 'start': 1, 'end': len(text4), 'type': 'generic'}]
        final_entity_list4 = [{'entity': 'Hel我们是朋友', 'start': 1, 'end': 9, 'type': 'generic'}]
        ret_entity_list4 = replace_chars(entity_list4, 4, ' lo', '我们是朋友', text4)
        self.assertEqual(final_entity_list4, ret_entity_list4)

        text5 = ' Hel lo'
        entity_list5 = [{'entity': 'Hel lo', 'start': 1, 'end': len(text5), 'type': 'generic'}]
        final_entity_list5 = [{'entity': 'Hel我们是朋友o', 'start': 1, 'end': 10, 'type': 'generic'}]
        ret_entity_list5 = replace_chars(entity_list5, 4, ' l', '我们是朋友', text5)
        self.assertEqual(final_entity_list5, ret_entity_list5)

        text7 = ' Hel lo1'
        entity_list7 = [{'entity': 'Hel lo', 'start': 1, 'end': 7, 'type': 'generic'}]
        final_entity_list7 = [{'entity': 'Hel lo', 'start': 1, 'end': 7, 'type': 'generic'}]
        ret_entity_list7 = replace_chars(entity_list7, 7, '1', '2', text7)
        self.assertEqual(final_entity_list7, ret_entity_list7)

    def test_data_preprocess(self):
        para = {'entities': [{'end': 20, 'type': 'iupac', 'entity': '\xa0\xa0氟吡菌胺', 'start': 14}],
                'patent_id': 'cc879722-3c99-47cd-b95b-7d6c312e1768', 'section': 'description',
                'text': '\xa0\xa0B-51\t\xa0式I化合物\t\xa0\xa0氟吡菌胺(picobenzamid)\n', 'index': 241}

        para = {'section': 'description',
                'text': '作为二磷酸盐，可以例举ォルパドロン酸、阿伦特罗钠水合物、 イバンドロン酸、羟乙二磷酸二钠、ゾレドロン酸、KCO-692(氯甲 双磷酸钠水合物)、インカドロン酸二钠、氨羟二磷酸二钠、YM175、 YM529(ONO-5920)、チルドロン酸二钠(ME3737、SR41319B)、 リセドロン酸钠水合物(NE-58095)等。\n',
                'index': 770, 'entities': [{'end': 27, 'start': 23, 'type': 'iupac', 'entity': '钠水合物'},
                                           {'end': 36, 'start': 29, 'type': 'iupac', 'entity': 'イバンドロン酸'},
                                           {'end': 51, 'start': 45, 'type': 'iupac', 'entity': 'ゾレドロン酸'}],
                'patent_id': '82c3718f-84ac-4a5d-ad60-ddca5dc23ffe'}
        new_para = data_preprocess(para)
        new_text = new_para['text']
        for e in new_para['entities']:
            self.assertEqual(e['entity'], new_text[e['start']:e['end']])
