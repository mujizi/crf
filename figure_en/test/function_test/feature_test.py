from figure_en.crf_feature import *
from figure_en.utils.io import *

# f = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/test.json')
tokens = [{'text': 'FIELD', 'pos_tag': 'NN'}, {'text': 'cat', 'pos_tag': 'NN'}, {'text': '10', 'pos_tag': 'num'}]
# print(f[0]['tokens'])
crf_feature = CRFFeature(tokens)
o = crf_feature.sent2feature()
print(o)
