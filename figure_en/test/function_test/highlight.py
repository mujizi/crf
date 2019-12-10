from figure_en.utils.highlight import *

from figure_en.utils.io import *
import pandas as pd


# s = 'what are you doing?'
#
# o = highlight(s, 'red')
# o1 = highlight_by_spans(s, [(2, 4), (6, 8)])
# print(o1)
# print(o)

f = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/raw/48_label.json')
# for i in f:
#     s = highlight_paragraph(i)
#     print(s)

print(highlight_paragraph(f[0]))

s = 'what are you doing?'

o = highlight(s, 'red')
o1 = highlight_by_spans(s, [(2, 4), (6, 8)])
print(o1)
print(o)
