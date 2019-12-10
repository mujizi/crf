from figure_en.api_model import Model
from figure_extractor_en.api_model import Model as Rule_model
from figure_extractor_en.extractor import get_parts
from figure_en.en_get_parts_task.utils.tools import *
from figure_en.en_get_parts_task.predict.relation_pairs import *
from figure_en.utils.io import *
import json
model = Model()
# rule_model = Rule_model()


def merge2model(text):
    # rule_base model
    entities = model.run({'text': text})  # .train(training_data).evaluation()
    print(entities)
    return entities


def csv2get_parts(src_file, dest_file):
    if src_file.endswith('.json'):
        with open(dest_file, 'w') as f2:
            f = read_json(src_file)
            for i in f:
                get_parts = merge2model(i['text'])
                pn = i['pn']
                dic = {'pn': pn,
                       'get_parts': get_parts,
                       'text': i['text']}
                print(dic)
                f2.write(json.dumps(dic) + '\n')

    elif src_file.endswith('.csv'):
        with open(dest_file, 'w') as f2:
            f = pd.read_csv(src_file)
            pn_l = f['pn']
            desc_l = f['desc']
            for i in range(0, len(pn_l)):
                get_parts = merge2model(desc_l[i])
                pn = pn_l[i]
                dic = {'pn': pn,
                       'get_parts': get_parts,
                       'text': desc_l[i]}
                print(dic)
                f2.write(json.dumps(dic) + '\n')


if __name__ == '__main__':
    src_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/63_raw/batch_patent.json'
    dest_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/new_map_result_6_5.jsonl'
    csv2get_parts(src_file, dest_file)

    # src_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/html_1.csv'
    # dest_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/html_1.json'
    # csv2get_parts(src_file, dest_file)

    # src_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/59_raw/59.csv'
    # dest_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/59_raw/bug59.json'
    # csv2get_parts(src_file,dest_file)

    # text = 'In this embodiment system 10.8'
    # r = merge2model(text)
    # print(r)