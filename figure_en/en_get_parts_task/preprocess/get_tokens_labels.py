from figure_en.utils import io
from figure_en.tokenizer import EnglishTokenizer
from figure_en.data_process.entity2label import *
from figure_en.utils.constant import *
from figure_en.utils.io import *
import json


def get_tokens_labels(src_file_path, dest_file_path):
    tokenizer = EnglishTokenizer()
    new_list = []
    if src_file_path.endswith('json'):
        src_file = read_json(src_file_path)
        for i in src_file:
            tokens = tokenizer.tokenize_sentence(i['text'])
            print(i['text'])
            dic = {'tokens': tokens,
                   'text': i['text'],
                   'pn': i['pn'],
                   'entities': i['entities']}
            dic2 = entity2label(dic, label_schema='BILOU', resolve_conflict=True)
            new_list.append(dic2)
        write_json(dest_file_path, new_list)

    elif src_file_path.endswith('jsonl'):
        with open(dest_file_path, 'w') as df:
            with open(src_file_path, 'r') as f:
                l = []
                for i in f:
                    l.append(json.loads(i))
                for i in l:
                    tokens = tokenizer.tokenize_sentence(i['text'])
                    dic = {'tokens': tokens,
                           'text': i['text'],
                           'pn': i['pn'],
                           'entities': i['entities']}
                    print(dic['entities'])
                    print(dic['tokens'])
                    print(dic['text'])
                    print(dic['pn'])
                    dic2 = entity2label(dic, label_schema='BILOU', resolve_conflict=True)
                    df.write(json.dumps(dic2) + '\n')


if __name__ == '__main__':
    sf = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/63_raw/merge_63.json'
    df = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/63_raw/merge_63_5_29.json'
    # s = 'The external distraction apparatus <b>1</b> includes a stationary member or portion <b>2</b>. The stationary member <b>2</b> may be fixed to the head of a patient <b>12</b>. This may be accomplished through the use of standard fixation hardware such as fixation pins <b>20</b> (see, for example, FIG. 2). The stationary member <b>2</b> may serve to affix the external distraction apparatus <b>1</b> to the patient. The stationary member <b>2</b> may also serve as the frame of reference for all distraction movements performed by the apparatus <b>1</b>. The stationary member <b>2</b> may be halo or horseshoe like in shape. A portion of the stationary member <b>2</b> may be anterior to the head of the patient <b>12</b> when the apparatus <b>1</b> is in place on the patient <b>12</b>'
    get_tokens_labels(sf, df)