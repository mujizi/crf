# -*- coding: UTF-8 -*-

from .brat2json import *


def token_json2label(paragraph_list, dest_filename, conll_delimiter=' '):
    paragraph_list = [p for p in paragraph_list if p]
    if not paragraph_list:
        return None
    for key in {'tokens', 'labels'}:
        if key not in paragraph_list[0]:
            raise KeyError('key {0} must be in paragraph dict'.format(key))

    if not isinstance(paragraph_list[0]['tokens'][0], dict):
        raise TypeError('token must be in dict')

    token_keys = set(paragraph_list[0]['tokens'][0])
    extra_keys = set(token_keys).difference({'text', 'start', 'end', 'pos_tag'})
    conll_segments = []
    for paragraph in paragraph_list:
        conll_segment_lines = []
        for token, label in zip(paragraph['tokens'], paragraph['labels']):
            base_items = [token['text']]
            if 'pos_tag' in token:
                base_items.append(token['pos_tag'])
            if extra_keys:
                base_items.append([token[key] for key in extra_keys])
            base_items.append(label)
            conll_segment_lines.append(conll_delimiter.join(base_items))
        conll_segments.append('\n'.join(conll_segment_lines))
    write_file(dest_filename, '\n\n'.join(conll_segments))


def output_conll(paragraph_list, dest_filename, delimiter=' '):
    """
    output paragraph list with labels into CoNLL file format.
    :param paragraph_list: source paragraph list with text, entities and labels
    :param dest_filename: destination CoNLL file path
    :param delimiter: delimiter of column in CoNLL file
    :param pos_key: pos tag key in paragraph list
    :return: None
    """
    conll_data = []
    for item in paragraph_list:
        lines = [delimiter.join((t, p, l)) for t, p, l in zip(item['tokens'], item['pos_tags'], item['labels'])]
        conll_data.append('\n'.join(lines))
    write_file(dest_filename, '\n\n'.join(conll_data))


