# -*- coding: UTF-8 -*-
from unittest import TestCase
from figure_en.utils.highlight import *


class TestHighlight(TestCase):
    def test_highlight_by_spans(self):
        text = 'This is an good example.'
        spans = [(0, 4), (5, 7), (8, 10, 'blue'), (11, 15, 'green'), (16, 23)]
        hl_text = highlight_by_spans(text, spans)
        true_text = '[0;30;43mThis[0m [0;30;43mis[0m [0;30;44man[0m [0;37;42mgood[0m [0;30;43mexample[0m.'
        self.assertEqual(hl_text, true_text)
        print(hl_text)

    def test_highlight_by_spans_with_tokens(self):
        tokens = [{'text': '我们', 'start': 0, 'end': 2}, {'text': '来自', 'start': 2, 'end': 4},
                  {'text': '智慧芽', 'start': 4, 'end': 7}]
        spans = [(0, 2), (2, 4), (4, 7)]
        hl_text = highlight_by_spans_with_tokens(tokens, spans, is_merge_spans=True)
        print(hl_text)
        self.assertEqual(hl_text, ' [0;30;43m我们 来自 智慧芽[0m')

        tokens = [{'text': '我们', 'start': 0, 'end': 2}, {'text': '来自', 'start': 2, 'end': 4},
                  {'text': '智慧芽', 'start': 4, 'end': 7}]
        spans = [(0, 2, 'red'), (2, 4, 'blue'), (4, 7, 'green')]
        hl_text = highlight_by_spans_with_tokens(tokens, spans)
        print(hl_text)
        self.assertEqual(hl_text, ' [1;31;40m我们[0m  [0;30;44m来自[0m  [0;37;42m智慧芽[0m')

    def test_merge_spans(self):
        spans1 = [(1, 10), (2, 5)]
        self.assertEqual(merge_spans(spans1), [(1, 10)])
        spans2 = [(1, 10, 'yellow'), (2, 11, 'blue'), (20, 100, 'blue'), (200, 300)]
        self.assertEqual(merge_spans(spans2), [(1, 11, 'blue'), (20, 100, 'blue'), (200, 300)])
