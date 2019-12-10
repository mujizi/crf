from figure_en.utils.io import *
import pandas as pd
from figure_en.en_get_parts_task.utils.tools import *


def get_dataframe(src_file_name, dest_file_name):
    f = read_jsonline(src_file_name)
    print(f)
    name_l = []
    id_l = []
    pn_l = []
    for i in f:
        parts = i['get_parts']
        for j in parts:
            name_l.append(j['representive_label_txt'])
            re_id = replace_html_tag(j['label_id'])
            id_l.append(re_id)
            pn_l.append(i['pn'])

    data = {'name': name_l,
            'id': id_l,
            'pn': pn_l}
    df = pd.DataFrame(data=data)
    df.to_csv(dest_file_name)


def role_crf_cover(role_file, crf_file):
    crf = pd.read_csv(crf_file)
    role = pd.read_csv(role_file)
    pn_l = set(crf['pn'])
    c_id_l = list(crf['id'])
    r_id_l = list(role['id'])
    new_role_l = []
    for pn in pn_l:
        dic = {}
        part_id_l = []
        for i in range(0, role.shape[0]):
            if pn == role.loc[i]['pn']:
                part_id_l.append(role.loc[i]['id'])
        dic['id'] = set(part_id_l)
        dic['pn'] = pn
        new_role_l.append(dic)

    new_crf_l = []
    for pn in pn_l:
        dic = {}
        part_id_l = []
        for i in range(0, crf.shape[0]):
            if pn == crf.loc[i]['pn']:
                part_id_l.append(crf.loc[i]['id'])
        dic['id'] = set(part_id_l)
        dic['pn'] = pn
        new_crf_l.append(dic)

    for i in range(0, len(new_crf_l)):
        r = list(new_crf_l[i]['id'] - new_role_l[i]['id'])
        print(r)
        print(new_crf_l[i]['pn'])


if __name__ == '__main__':
    get_dataframe('/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/new_map_result.json',
                  '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/new_map_result.csv')

    # get_dataframe('/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/html_1.json',
    #               '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/html_1_id_name.csv')

    # role_crf_cover('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/pre/role_65.csv',
    #                '/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/pre/crf_65.csv')