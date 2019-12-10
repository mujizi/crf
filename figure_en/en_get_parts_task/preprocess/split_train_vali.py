from figure_en.utils.io import *


def split_dataset(file):
    textline_file = read_json(file)
    pn_list = []
    for line in textline_file:
        pn_list.append(line['pn'])
    pn_list = list(set(pn_list))

    train_pn_list = pn_list
    validation_pn_list = pn_list[50:63]
    test_pn_list = pn_list[50:63]

    training_data = []
    for pn in train_pn_list:
        for line in textline_file:
            if line['pn'] == pn:
                training_data.append(line)

    validation_data =[]
    for pn in validation_pn_list:
        for line in textline_file:
            if line['pn'] == pn:
                validation_data.append(line)

    test_data = []
    for pn in test_pn_list:
        for line in textline_file:
            if line['pn'] == pn:
                test_data.append(line)

    write_json('/home/patsnap/PycharmProjects/crf/ner_figure_part/data/training.json', training_data)
    write_json('/home/patsnap/PycharmProjects/crf/ner_figure_part/data/validation.json', validation_data)
    write_json('/home/patsnap/PycharmProjects/crf/ner_figure_part/data/test.json', test_data)
    print(len(training_data))
    print(len(validation_data))
    print(len(test_data))
    return pn_list


if __name__ == '__main__':
    f_p = ('/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/63_raw/merge_63.json')
    pn = split_dataset(f_p)
    # print(pn)
    # print(len(pn))


