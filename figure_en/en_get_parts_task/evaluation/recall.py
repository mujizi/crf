import pandas as pd
import re
N = re.compile(r'\d{0,3}')


def recall(crf, label):
    crf_f = pd.read_csv(crf)
    label_f = pd.read_csv(label)
    c_pn = crf_f['pn']
    label_pn = list(label_f['pn'])
    c_id = crf_f['id']
    label_id = list(label_f['id'])
    # c_name = crf_f['name']
    # label_name = label_f['part_name']

    n = 0
    new_id = []
    new_pn = []
    for i, i2 in zip(label_pn, label_id):
        for j, j2 in zip(c_pn, c_id):
            if i == j and i2 == j2:
                n += 1
                print(n)
                continue
    print('recall: %s' % (n/580))


def make_pn_dic(pn_l, id_l):
    set_pn = set(pn_l)
    new = []
    for pn in set_pn:
        new_id = []
        for pn2, id in zip(pn_l, id_l):
            if pn2 == pn:
                new_id.append(id)
        dic = {
            'pn': pn,
            'id': new_id
        }
        new.append(dic)
    return new


def fail_analysis(get_parts_file, label_file, fail_file):
    parts_f = pd.read_csv(get_parts_file)
    label_f = pd.read_csv(label_file)
    parts_pn_l = parts_f['pn']
    label_pn_l = list(label_f['pn'])
    parts_id_l = parts_f['id']
    label_id_l = list(label_f['id'])
    new_parts_l = make_pn_dic(parts_pn_l, parts_id_l)
    new_label_l = make_pn_dic(label_pn_l, label_id_l)
    print(new_parts_l)
    print(new_label_l)
    miss_pn = []
    miss_id = []
    for i in new_parts_l:
        for j in new_label_l:
            if i['pn'] == j['pn']:
                for z in j['id']:
                    if z not in i['id']:
                        miss_pn.append(i['pn'])
                        miss_id.append(z)
                        print(z)
                        print(i['pn'])
    dic  = {'pn': miss_pn,
            'id': miss_id}

    df = pd.DataFrame(data=dic)
    df.to_csv(fail_file)


def precision(src):
    f = pd.read_csv(src)
    label = f['label']
    n = 0
    for i in label:
        # print(i)
        if pd.isnull(i):
            n += 1
    print(n)
    print(len(label))
    print(n / len(label))



if __name__ == '__main__':
    crf = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/59_raw/bug59.csv'
    label = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/59_raw/59_id.csv'
    recall(crf, label)
    # src = '/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/pre/crf_999.csv'
    # precision(src)