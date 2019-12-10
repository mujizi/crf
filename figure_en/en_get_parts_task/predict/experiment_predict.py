from figure_en.experiment import *
from figure_en.en_get_parts_task.predict.relation_pairs import *
from figure_en.en_get_parts_task.predict.remove_repeat import *
from figure_en.en_get_parts_task.utils.tools import *
from figure_extractor_en.extractor import get_parts
from figure_extractor_en.api_model import Model

SEQ_BILOU = 'BILOU'
CUT_TOKEN_PATTERN = re.compile(r"(\s|,|\(|\)|\.)")
training_data = '/home/patsnap/PycharmProjects/crf/figure_en/data/training.json'
config = {
     'model_name': 'merge_data_v2',

}
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
     '+4:format_postag']


def merge_model(text):
     # rule_base model
     rule_entities = get_parts(text)
     rule_entities = rule_voting(rule_entities)
     # crf_model
     entities = CRFExperiment(config['model_name'], l).inference(text)   # .train(training_data).evaluation()
     entities = replace_html_part_id(entities)
     # relation pair between part_name and part_id
     pair_dic = relation_pair(entities)
     crf_entities = voting(pair_dic)
     merge_entities = merge_rule_crf(rule_entities, crf_entities)
     # print(rule_entities)
     return merge_entities


def single_rule(text):
     # rule_entities = get_parts(text)
     rule_model = Model()
     rule_entities = rule_model.run_model(text)
     return rule_entities


def singe_crf(text):
     # crf_model
     entities = CRFExperiment(config['model_name'], l).inference(text)  # .train(training_data).evaluation()
     entities = replace_html_part_id(entities)
     # relation pair between part_name and part_id
     pair_dic = relation_pair(entities)
     crf_entities = voting(pair_dic)
     return crf_entities


def csv2get_parts(src_file, dest_file):
    with open(dest_file, 'w') as f2:
        f = pd.read_csv(src_file)
        pn_l = f['pn']
        desc_l = f['desc']
        for i in range(0, len(pn_l)):
            get_parts = merge_model(desc_l[i])
            pn = pn_l[i]
            dic = {'pn': pn,
                   'get_parts': get_parts}
            print(dic)
            f2.write(json.dumps(dic) + '\n')


if __name__ == '__main__':
     # text = 'flow channels <b>5U, 6SN, 1DD and AV'
     # text = 'accompanied with guide rails <b>56</b>, <b>57</b> and <b>666</b>. recording unit <b>24</b>,'
     # r = merge_model(text)
     # print(len(r))
     # print(r)
     src_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/59_raw/59.csv'
     dest_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/model_v2_5_59.json'
     csv2get_parts(src_file, dest_file)


     # f = pd.read_csv('/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/html_1.csv')
     # text = f['text']
     # desc = text[0]
     # r = singe_crf(desc)
     # print(len(r))
     # r = task_inference(desc)
     # print(r)
     # new = merge_model(text)
     # # print(len(r))
     # # print('role:%s' % r)
     # print(len(new))
     # print('crf:%s' % new)
     # us_f = '/home/patsnap/PycharmProjects/en_extract_pre/data/raw/us_desc.csv'
     # dest = '/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/pre/html_60.json'
     # text = extract_single_patent('US9580265', us_f)
     # print(text)
     # r = singe_crf(text)
     # print(len(r))
     # print(r)
     # id_l = [i['id'] for i in r]
     # name_l = [i['part_name'] for i in r]
     # print(id_l)
     # print(name_l)
     # write_json(dest, r)


