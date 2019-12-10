from figure_en.en_get_parts_task.predict.get_predicted import *
import pandas as pd
from figure_extractor_en.extractor import get_parts

def csv_get_parts(src_file, dest_file):
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


def csv_single_rule(src_file, dest_file):
    with open(dest_file, 'w') as f2:
        f = pd.read_csv(src_file)
        pn_l = f['pn']
        desc_l = f['desc']
        for i in range(0, len(pn_l)):
            get_parts = single_rule(desc_l[i])
            pn = pn_l[i]
            dic = {'pn': pn,
                   'get_parts': get_parts}
            print(dic)
            f2.write(json.dumps(dic) + '\n')


if __name__ == '__main__':
    src_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/html_1.csv'
    dest_file = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/html_1.json'
    csv_get_parts(src_file, dest_file)

    # dest_file = '/home/patsnap/PycharmProjects/crf/figure_en/figure_en/en_get_parts_task/data/pre/59_single.json'
    # csv_single_rule(src_file, dest_file)

    # model = Model()
    # r = model.run_model(i)
    # r = model.postprocess(r, i, i)
    # print(r['result'])