from figure_en.api_model import Model
from figure_en.api_model import Model
from figure_extractor_en.extractor import *
from figure_en.test.test_case.case import case_sentences
from figure_en.utils.highlight import *
import os
from modelhub.framework import ApiModel
from figure_en.utils.constant import EXP_CONFIG
from figure_en.crf_tagger import CRFTagger
from figure_en.post_process import post_process
from figure_en.en_get_parts_task.utils.tools import *
from figure_en.en_get_parts_task.utils.log import *
model = Model()


def single_crf_rule_test(sentence_l):
    if isinstance(sentence_l, list):
        for i in sentence_l:
            c, r = model.run_model(i)
            c = post_process(c)
            r = voting(r)
            logging.info('Rule:')
            if r == []:
                print('rule fail: %s' % highlight(i, 'red'))
            else:
                id_l = []
                name_l = []
                for j in r:
                    id_l.append(j['label_id'])
                    name_l.append(j['representive_label_txt'])
                logging.info('success:%s' % sentence_l)
                logging.info('id:%s' % id_l)
                logging.info('name:%s' % name_l)

            logging.info('Crf:')
            if c == []:
                print('crf fail: %s' % highlight(i, 'red'))
            else:
                id_l = []
                name_l = []
                for j in c:
                    id_l.append(j['label_id'])
                    name_l.append(j['representive_label_txt'])
                logging.info('success:%s' % sentence_l)
                logging.info('id:%s' % id_l)
                logging.info('name:%s' % name_l)

    elif isinstance(sentence_l, str):
        c, r = model.run_model(sentence_l)
        c = post_process(c)
        r = voting(r)
        logging.info('Rule:')
        if r == []:
            print('rule fail: %s' % highlight(sentence_l, 'red'))
        else:
            id_l = []
            name_l = []
            for j in r:
                id_l.append(j['label_id'])
                name_l.append(j['representive_label_txt'])
            logging.info('success:%s' % sentence_l)
            logging.info('id:%s' % id_l)
            logging.info('name:%s' % name_l)

        logging.info('Crf:')
        if c == []:
            print('crf fail: %s' % highlight(sentence_l, 'red'))
        else:
            id_l = []
            name_l = []
            for j in c:
                id_l.append(j['label_id'])
                name_l.append(j['representive_label_txt'])
            logging.info('success:%s' % sentence_l)
            logging.info('id:%s' % id_l)
            logging.info('name:%s' % name_l)


if __name__ == '__main__':
    log = Log('/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/test/log/1.log')
    # single_crf_rule_test(case_sentences)
    # case = 'associated VOQ-module 100. Each VOQ-module 100 consists of a flow-controller 102, a flow-demultiplexer 104, a set of flow-VOQs 106, a flow-server 108, and an optional controller 105, which may '
    # case = 'includes a differently configured first side piece 341 and second side piece 342'
    # case = 'the cleaning liquid supply unit 26(26a, 26b) supplies a'
    # case = 'The power strip of this embodiment includes an AD converter (Analog-to-Digital converter) 50, a control part 60, and a communication part 70.'
    # case = 'in a case that the water-soluble resin (thermoplastic resin) 12 in a solid state'
    # case = 'this transmitted rotation speed is received by the communication I/F 36 of the left wheel controller 30L'
    # case = 'in some embodiments, may produce light in the UV-A band (320-400 nm) and'
    # case = 'An ‘X’ character could be coated onto the cover film <b>320</b>.'
    # case = 'which filters signal 1348 based on the secondary path dynamics model.'
    case = 'the area S1 of the opening 523'
    single_crf_rule_test(case)
