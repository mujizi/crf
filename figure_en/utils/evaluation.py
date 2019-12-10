# -*- coding: UTF-8 -*-
"""
encapsulate some evaluation related functions
"""
import copy
from .constant import *
from .highlight import *
from .utils import *
from .io import read_json

ENTITY_TYPE_COLOR_MAPPER = get_entity_type_color_mapper()


def evaluate_result_from_file(pred_filename, true_filename, oov_filename=None):
    pred_data = read_json(pred_filename)
    true_data = read_json(true_filename)
    if oov_filename:
        oov_data = read_json(oov_filename)
    else:
        oov_data = None
    evaluate_result(pred_data, true_data, oov_data)


def evaluate_result(pred_data, true_data, oov_data=None):
    """
    evaluate result from data
    :param pred_data: prediction result data
    :param true_data: true result data
    :param oov_data: OOV data
    :return: precision, recall and f1 result
    """

    pred_type_data = split_by_entity_type(pred_data)
    true_type_data = split_by_entity_type(true_data)
    if oov_data:
        true_type_oov_data = split_by_entity_type(oov_data)
    else:
        true_type_oov_data = None

    for entity_type, single_true_data in true_type_data.items():
        print('entity type result: {0}'.format(entity_type))
        print('------------------------')
        if entity_type not in true_type_data:
            print('precision: 0.00')
            print('recall: 0.00')
            print('f1 score: 0.00')
            if oov_data:
                print('OOV recall rate: NaN')
        else:
            if not true_type_oov_data or not true_type_oov_data.get(entity_type):
                evaluate_data(pred_type_data[entity_type], true_type_data[entity_type])
                print('OOV recall rate: NaN')
            else:
                evaluate_data(pred_type_data[entity_type], true_type_data[entity_type])
                _, r, _ = evaluate_data(pred_type_data[entity_type],
                                        true_type_oov_data[entity_type],
                                        False)
                print('OOV recall rate: {0:.4f}'.format(r))


def get_entity_type(true_data):
    types = set(e['type'] for sent in true_data for e in sent['entities'])
    if '' in types:
        raise ValueError('entity type has empty string')
    return types


def split_by_entity_type(data):
    types = get_entity_type(data)
    new_data = {t: [] for t in types}
    if len(types) == 1:
        return {list(types)[0]: data}
    else:
        for sent in data:
            entities = sent['entities']
            for entity_type in types:
                new_sent = copy.deepcopy(sent)
                new_sent['entities'] = [e for e in entities if e['type'] == entity_type]
                new_data[entity_type].append(new_sent)
    return new_data


def evaluate_data(pred_data, true_data, print_result=True, is_rate=True):
    """
    evaluate result from sentence objects (schema refer to CONVENTION.md)
    :param pred_data: prediction sentence objects
    :param true_data: true sentence objects
    :param print_result: whether print precision, recall and f1 score, default is ``True``
    :param is_rate: whether return the precision, recall and f1 score or
                    true positive, predicted count and recall count
    :return:
    """
    pred_count = sum(len(item['entities']) for item in pred_data)
    true_count = sum(len(item['entities']) for item in true_data)
    true_positive_count = 0

    for pred_sent, true_sent in zip(pred_data, true_data):
        true_spans = [(e['start'], e['end']) for e in true_sent['entities']]
        for e in pred_sent['entities']:
            if (e['start'], e['end']) in true_spans:
                true_positive_count += 1

    if pred_count == 0:
        precision = 0.0
    else:
        precision = true_positive_count / pred_count
    recall = true_positive_count / true_count
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    if print_result:
        print('precision: ', true_positive_count, '/', pred_count, '=', '{0:.4f}'.format(precision))
        print('recall: ', true_positive_count, '/', true_count, '=', '{0:.4f}'.format(recall))
        print('f1 score: ', '{0:.4f}'.format(f1))
    if is_rate:
        return precision, recall, f1
    else:
        return true_positive_count, pred_count, true_count


def compare_two_model(compared_model_name, base_model_name, suffix='validation', is_highlight=True):
    """
    get redundant spans of result from compared model
    :param compared_model_name: compared model name of prediction result
    :param base_model_name: baseline model name of prediction result
    :param suffix: model name suffix, use the true data filename mostly, default is ``validation``
    :param is_highlight: whether highlight the result
    :return: redundant result
    """
    tmpl = EVALUATION_DIR + '{0}_' + suffix + '.json'

    compared_file = tmpl.format(compared_model_name)
    base_file = tmpl.format(base_model_name)

    compare_two_files(compared_file, base_file, is_highlight)


def model_result_highlight(model_name, suffix, mode=RESULT_ERROR, skip_empty=True):
    """
    highlight the model prediction result compared with true result
    :param model_name: model name of prediction result
    :param suffix: suffix of model name
    :param mode: highlight mode,
    :param skip_empty: whether skip the empty sentences
    :return: None
    """
    pred_filename = EVALUATION_DIR + model_name + '_' + suffix + '.json'
    true_filename = get_true_filename_by_suffix(suffix)
    compared_data = read_json(pred_filename)
    base_data = read_json(true_filename)
    if mode == RESULT_ERROR:
        compare_two_data(compared_data, base_data, skip_empty)
    elif mode == RESULT_MISSING:
        compare_two_data(base_data, compared_data, skip_empty)
    elif mode == RESULT_DISPLAY:
        for sent in compared_data:
            spans = [(e['start'], e['end']) for e in sent['entities']]
            if not spans and skip_empty:
                continue
            print('===========================')
            print(highlight_by_spans(sent['text'], [(e['start'], e['end']) for e in sent['entities']]))
            # print(highlight_by_spans([(t['start'],t['end']) for t in sent['tokens']]))
            # print(highlight_by_spans_with_tokens(sent['tokens'], spans))
    else:
        raise Exception('comparison mode error')


def compare_two_files(compared_file, base_file, is_highlight=True, skip_empty=True):
    """
    compare two predict file, output the result that compared file more than base file
    :param compared_file: file path of compared prediction result
    :param base_file: file path of baseline result
    :param is_highlight: whether print highlight result
    :param skip_empty: whether skip empty result
    :return: redundant result in compared file
    """
    compared_data = read_json(compared_file)
    base_data = read_json(base_file)

    compare_two_data(compared_data, base_data, is_highlight, skip_empty)


def compare_two_data(compared_data, base_data,
                     is_highlight=True, skip_empty=True, highlight_token=False):
    """
    compared two predict data, output the result that compared file more than base file
    :param compared_data: sentence list of compared prediction result
    :param base_data: file path of baseline result
    :param is_highlight: whether print highlight result
    :param skip_empty: whether skip empty result
    :param highlight_token: whether highlight tokens
    :return: None
    """
    results = []

    for compared_sent, base_sent in zip(compared_data, base_data):
        compared_spans = get_spans_from_entity_list(compared_sent['entities'])
        base_spans = get_spans_from_entity_list(base_sent['entities'])

        diff_spans = compared_spans.difference(base_spans)
        results.append({'text': base_sent['text'], 'tokens': base_sent['tokens'], 'spans': diff_spans})

    if is_highlight:
        for sent in results:
            if skip_empty and not len(sent['spans']):
                continue
            print('===========================')
            if highlight_token:
                print(highlight_by_spans_with_tokens(sent['tokens'], sent['spans']))
            else:
                print(highlight_by_spans(sent['text'], sent['spans']))
    else:
        return results


def compare_two_model_with_true_file(pred_model_name, base_model_name, suffix='validation',
                                     mode=RESULT_MORE, is_highlight=True, highlight_token=False):
    """
    compare prediction result of two model
    :param pred_model_name: model name to be compared
    :param base_model_name: model name to be baseline model
    :param suffix: suffix name of evaluation file
    :param mode: comparision mode, RESULT_MORE: improved recall items, RESULT_ERROR: occurred error items
    :param is_highlight: whether highlight result
    :param highlight_token: whether highlight tokens
    :return:
    """
    true_filename = get_true_filename_by_suffix(suffix)
    tmpl = EVALUATION_DIR + '{0}_' + suffix + '.json'
    pred_filename = tmpl.format(pred_model_name)
    base_filename = tmpl.format(base_model_name)

    compare_two_file_with_true_file(pred_filename, base_filename, true_filename, mode, is_highlight, highlight_token)


def compare_two_file_with_true_file(pred_filename, base_filename, true_filename, mode=RESULT_MORE,
                                    is_highlight=True, highlight_token=False):
    """
    compared prediction result of two files
    :param pred_filename: file path to be compared
    :param base_filename: file path of baseline
    :param true_filename: file path of true file
    :param mode: comparision mode, RESULT_MORE: improved recall items, RESULT_ERROR: occurred error items
    :param is_highlight: whether highlight result
    :param highlight_token: whether highlight tokens
    :return:
    """
    pred_data = read_json(pred_filename)
    base_data = read_json(base_filename)
    true_data = read_json(true_filename)

    compare_two_result_with_true_result(pred_data, base_data, true_data, mode, is_highlight, highlight_token)


def compare_two_result_with_true_result(pred_data, base_data, true_data, mode=RESULT_MORE,
                                        is_highlight=True, highlight_token=False):
    """
    compared prediction result of two sentence list
    :param pred_data: sentence list to be compared
    :param base_data: sentence list of baseline
    :param true_data: sentence list of true result
    :param mode: comparision mode, RESULT_MORE: improved recall items, RESULT_ERROR: occurred error items
    :param is_highlight: whether highlight result
    :param highlight_token: whether highlight tokens
    :return:
    """
    results = []

    for pred_sent, base_sent, true_sent in zip(pred_data, base_data, true_data):
        pred_spans = get_spans_from_entity_list(pred_sent['entities'])
        base_spans = get_spans_from_entity_list(base_sent['entities'])
        true_spans = get_spans_from_entity_list(true_sent['entities'])
        if mode == RESULT_MORE:
            base_true_spans = base_spans.intersection(true_spans)
            pred_true_spans = pred_spans.intersection(true_spans)
            improved_spans = pred_true_spans.difference(base_true_spans)
            results.append({'text': true_sent['text'], 'tokens': pred_sent['tokens'],
                            'spans': improved_spans})
        elif mode == RESULT_ERROR:
            base_error_spans = base_spans.difference(true_spans)
            pred_error_spans = pred_spans.difference(true_spans)
            error_spans = pred_error_spans.difference(base_error_spans)
            results.append({'text': true_sent['text'], 'tokens': pred_sent['tokens'],
                            'spans': error_spans})
        else:
            raise Exception('result display mode error')

    if is_highlight:
        for sent in results:
            if not sent['spans']:
                continue
            if highlight_token:
                no_hl_text = ' '.join(t['text'] for t in sent['tokens'])
                hl_text = highlight_by_spans_with_tokens(sent['tokens'], sent['spans'])
                if no_hl_text != hl_text:
                    print('===========================')
                    print(hl_text)
            else:
                no_hl_text = ''.join(t['text'] for t in sent['tokens'])
                hl_text = highlight_by_spans(sent['text'], sent['spans'])
                if no_hl_text != hl_text:
                    print('===========================')
                    print(hl_text)
    else:
        return results


def get_true_filename_by_suffix(suffix):
    """
    get true file path by its name
    :param suffix:  filename of true file
    :return: total file path
    """
    return DATA_DIR + suffix + '.json'


def get_spans_from_entity_list(entity_list):
    spans = set()
    for entity in entity_list:
        span = (entity['start'], entity['end'], ENTITY_TYPE_COLOR_MAPPER[entity['type']])
        spans.add(span)
    return spans
