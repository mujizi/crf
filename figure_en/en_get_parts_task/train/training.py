from figure_en.experiment import *

SEQ_BILOU = 'BILOU'

MODEL_DIR  = '/home/patsnap/PycharmProjects/crf/figure_en/data/ner_figure_part/get_part_data/train/crf.json'
training_data = '/home/patsnap/PycharmProjects/crf/ner_figure_part/data/training.json'
config = {'model_name': 'merge_data_v2'}


l = ['word.exist_digit()',
     'word[-3:]',
     'word[-2:]',
     'postag',
     'spe_symbol',
     'conjunction',
     # part_name
     'word',
     'word.lower()',
     'word.isupper()',
     'exdigit',
     '-1:format_word',
     '-1:format_postag',
     '-1:exdigit',
     '-2:format_exdigit()',
     '-2:exdigit',
     '-2:format_word',
     '-2:format_postag',
     '-2:format_exdigit()',
     '-3:format_word',
     '-3:format_postag',
     '-3:format_exdigit()',
     '-3:exdigit',
     '-4:format_word',
     '-4:format_postag',
     '-4:format_exdigit()',
     '-4:exdigit',
     '-5:format_word',
     '-5:format_postag',
     '-5:format_exdigit()',
     'isdigit',
     '-1:exdigit',
     '-2:exdigit',
     '-3:exdigit',
     '-4:exdigit',
     '-5:exdigit',
     '+1:word.lower()',
     '+1:word.upper()',
     '+1:postag',
     '+1:word.exdigit()',
     '+1:format_exdigit',
     '-1:format_word',
     '-1:format_postag',
     '+2:word.lower()',
     '+2:word.upper()',
     '+2:postag',
     '+2:word.exdigit()',
     '+2:format_word',
     '+2:format_postag',
     '+3:word.lower()',
     '+3:word.upper()',
     '+3:postag',
     '+3:word.isdigit()',
     '+3:format_exdigit',
     '+3:format_word',
     '+3:format_postag',
     '+4:word.lower()',
     '+4:word.upper()',
     '+4:postag',
     '+4:word.exdigit()',
     '+4:format_exdigit',
     '+4:format_word',
     '+4:format_postag',]


entities = CRFExperiment(config['model_name'], l).train(training_data).evaluation()



# CRFExperiment('crf', ['word.isdigit()',
#                       'word[1:-1].isdigit()',
#                       'word[:-1].isdigit()',
#                       'word[1:].isdigit()',
#                       'word[-3:]',
#                       'word[-2:]',
#                       'postag',
#                       'word',
#                       'word.lower()',
#                       'word.isupper()',
#                       '-1:format_word',
#                       '-1:format_postag',
#                       '-1:format_isdigit()',
#                       '-2:format_word',
#                       '-2:format_postag',
#                       '-2:format_isdigit()',
#                       '-3:format_word',
#                       '-3:format_postag',
#                       '-3:format_isdigit()',
#                       '-4:format_word',
#                       '-4:format_postag',
#                       '-4:format_isdigit()',
#                       '-5:format_word',
#                       '-5:format_postag',
#                       '-5:format_isdigit()',
#                       'isdigit',
#                       '-1:isdigit',
#                       '-2:isdigit',
#                       '-3:isdigit',
#                       '-4:isdigit',
#                       '-5:isdigit',
#                       '+1:word.lower()',
#                       '+1:word.upper()',
#                       '+1:postag',
#                       '+1:word.isdigit()',
#                       '+1:format_word',
#                       '+1:format_postag',
#                       '+2:word.lower()',
#                       '+2:word.upper()',
#                       '+2:postag',
#                       '+2:word.isdigit()',
#                       '+2:format_word',
#                       '+2:format_postag',
#                       '+3:word.lower()',
#                       '+3:word.upper()',
#                       '+3:postag',
#                       '+3:word.isdigit()',
#                       '+3:format_word',
#                       '+3:format_postag',
#
#                       '+4:word.lower()',
#                       '+4:word.upper()',
#                       '+4:postag',
#                       '+4:word.isdigit()',
#                       '+4:format_word',
#                       '+4:format_postag',
#                       'spe_symbol',
#                       ]).evaluation()