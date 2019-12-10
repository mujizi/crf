# -*- coding: UTF-8 -*-
"""
brat => json in sentences
split json
json => conll
"""
import os
import copy
from ..utils.utils import *
from ..utils.constant import DEFAULT_LABELS
from .conll2json import *
from .prepare_annotataion_data import *
from .json2brat import *
from .json2conll import *
from .entity2label import *
from ..tokenizer import Tokenizer


def data_preparation(src_filename, dest_filename):
    tokenizer = Tokenizer()
    data = []
    for paragraph in read_json(src_filename):
        if 'tokens' not in paragraph:
            paragraph['tokens'] = tokenizer.tokenize_sentence(paragraph['text'])
        if 'labels' not in paragraph:
            paragraph = entity2label(paragraph, DEFAULT_LABELS)
        data.append(paragraph)
    write_json(dest_filename, data)


def data_initialization():
    # data pre-check
    experiment_data_checker()
    # only CoNLL
    # only JSON
    # build OOV data
    if not os.path.exists(VALIDATION_OOV_FILE):
        build_oov_data(VALIDATION_FILE, TRAINING_FILE)
    if not os.path.exists(TEST_OOV_FILE):
        build_oov_data(TEST_FILE, TRAINING_FILE)


def experiment_data_checker():
    is_json = False
    is_train_json = os.path.exists(TRAINING_FILE)
    is_validate_json = os.path.exists(VALIDATION_FILE)
    is_test_json = os.path.exists(TEST_FILE)
    if is_train_json and is_validate_json and is_test_json:
        is_json = True

    is_conll = False
    is_train_conll = os.path.exists(TRAINING_CONLL_FILE)
    is_validate_conll = os.path.exists(replace_extname(VALIDATION_FILE, 'conll'))
    is_test_conll = os.path.exists(replace_extname(TEST_FILE, 'conll'))
    if is_train_conll and is_validate_conll and is_test_conll:
        is_conll = True

    if not is_json and not is_conll:
        raise Exception('training preparation is not pasre')


def prepare_brat_data_by_patents(brat_dest_dirname,
                                 jsonl_dest_filename,
                                 dirname=None,
                                 filenames=None,
                                 is_preprocess=False,
                                 txt_size_threshold=50):
    """
    prepare brat data from patent data files
    :param brat_dest_dirname: brat destination folder path
    :param jsonl_dest_filename: json line destination file path of
    :param dirname: dirname of patent json file
    :param filenames: patent json file paths
    :param is_preprocess: whether preprocess text in patent
    :param txt_size_threshold: text threshold of brat text file
    :return:
    """
    if not dirname and not filenames:
        raise Exception('no files are assigned')
    if dirname and filenames:
        raise Exception('two parameters assign at same time')
    if dirname:
        filenames = get_filenames_in_folder(dirname)

    transform_into_paragraphs_from_files(filenames, jsonl_dest_filename, is_preprocess)
    prepare_brat_data(jsonl_dest_filename, brat_dest_dirname, txt_size_threshold)


def prepare_conll_data(brat_dirname,
                       json_filename,
                       dest_dirname):
    """
    transform CoNLL data from brat files
    :param brat_dirname: brat folder path
    :param json_filename: json destination file of parsed brat file
    :param dest_dirname: destination of final CoNLL file
    :return:
    """
    brat2json_dir(brat_dirname, json_filename)
    data = read_json(json_filename)
    # split data into training, validation and test
    training_data, validation_data, test_data = split_data(data)
    # output training data into CoNLL format
    output_conll(entity2label_batch(training_data), dest_dirname + 'training.conll')
    # output all data into json file
    write_json(dest_dirname + 'training.json', training_data)
    write_json(dest_dirname + 'validation.json', validation_data)
    write_json(dest_dirname + 'test.json', test_data)


def split_data(paragraphs):
    """
    split experiment data into training, validation and test data
    :param paragraphs: paragraph list
    :return: split training, validation and test data
    """
    para_count = len(paragraphs)
    training_index = int(para_count * 0.7)
    validation_index = int(para_count * 0.9)
    training_data = paragraphs[:training_index]
    validation_data = paragraphs[training_index:validation_index]
    test_data = paragraphs[validation_index:]
    return training_data, validation_data, test_data


def oov_rate(compared_sents, base_sents):
    compared_entities = [e['entity'] for sent in compared_sents if 'entities' in sent for e in sent['entities']]
    base_entities = [e['entity'] for sent in base_sents if 'entities' in sent for e in sent['entities']]
    oov_count = 0

    for e in compared_entities:
        if e not in base_entities:
            oov_count += 1

    return oov_count / len(compared_entities)


def build_oov_data(target_filename, base_filename, print_oov_rate=True):
    folder, filename = os.path.split(target_filename)
    basename, extname = os.path.splitext(filename)
    dest_filename = os.path.join(folder, basename + '_oov' + extname)

    base_data = read_json(base_filename)
    base_entities = {e['entity'] for sent in base_data if 'entities' in sent for e in sent['entities']}

    target_data = read_json(target_filename)
    oov_data = []
    for sent in target_data:
        if 'entities' in sent:
            oov_entities = [e for e in sent['entities'] if e['entity'] not in base_entities]
            new_sent = copy.deepcopy(sent)
            new_sent['entities'] = oov_entities
            # if oov_entities:
            oov_data.append(new_sent)
    if print_oov_rate:
        print('OOV rate: {0:.4f}'.format(oov_rate(target_data, base_data)))
    write_json(dest_filename, oov_data)


def label_single2type_from_CoNLL(src_filename, dest_filename):
    sents = read_conll_file(src_filename)
    for sent in sents:
        sent['labels'] = label_single2type(sent['labels'])
    token_json2label(sents, dest_filename)


def label_single2type(labels, label_type=DEFAULT_TYPE):
    for label_idx, label in enumerate(labels):
        labels[label_idx] = label + '-' + label_type
    return labels
