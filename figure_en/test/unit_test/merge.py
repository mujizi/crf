from figure_en.api_model import Model
from figure_extractor_en.extractor import *
from figure_en.test.test_case.case import case_sentences
from figure_en.utils.highlight import *

load_spacy()
model = Model()


def merge_test(sentence_l):
    if isinstance(sentence_l, list):
        for i in sentence_l:
            r = model.run({'text':i})
            if r == []:
                print('fail: %s' % highlight(i, 'red'), '\n')
            else:
                id_l = []
                name_l = []
                for j in r:
                    id_l.append(j['label_id'])
                    name_l.append(j['representive_label_txt'])
                print('success:', i)
                print('id:', id_l)
                print('name:', name_l, '\n')

    elif isinstance(sentence_l, str):
        r = model.run({'text': sentence_l})
        if r == []:
            print('fail: %s' % highlight(sentence_l, 'red'), '\n')
        else:
            id_l = []
            name_l = []
            for j in r:
                id_l.append(j['label_id'])
                name_l.append(j['representive_label_txt'])
            print('success:', sentence_l)
            print('id:', id_l)
            print('name:', name_l, '\n')


if __name__ == '__main__':
    # merge_test(case_sentences)
    merge_test(' such image attribute change UI 810')
