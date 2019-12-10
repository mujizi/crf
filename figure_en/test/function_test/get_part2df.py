import pandas as pd
from figure_en.utils.io import *


def get_get2df(src, dest):
    f = read_jsonline(src)
    pn_l = []
    id_l = []
    name_l = []
    for i in f:
        get_parts = i['get_parts']
        for j in get_parts:
            id_l.append(j['id'])
            name_l.append(j['part_name'])
            pn_l.append(i['pn'])

    data = {'pn': pn_l,
            'name': name_l,
            'id': id_l}
    df = pd.DataFrame(data=data)
    df.to_csv(dest)


if __name__ == '__main__':
    src = '/home/patsnap/PycharmProjects/crf/figure_en/figure_en/en_get_parts_task/data/pre/59_get_parts.json'
    dest = '/home/patsnap/PycharmProjects/crf/figure_en/figure_en/en_get_parts_task/data/pre/59_csv2df.csv'
    get_get2df(src,dest)