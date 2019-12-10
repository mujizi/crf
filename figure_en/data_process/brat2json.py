# -*- coding: UTF-8 -*-
import os
import json
import itertools
from ..utils.io import *
from ..utils.utils import *


def brat2json_dir(dirname, dest_filename=None):
    """
    transform brat directory into paragraph list
    :param dirname: brat directory path
    :param dest_filename: destination filename, if None, no output
    :return: parsed paragraph list
    """
    paragraphs = []
    for filename in get_brat_filename(dirname):
        paragraphs.extend(brat2json_file(filename))
    if dest_filename:
        write_json(dest_filename, paragraphs)
    return paragraphs


def brat2json_file(src_filename, dest_filename=None):
    """
    transform brat file into paragraph list
    :param src_filename: brat filename, without suffix
    :param dest_filename: destination filename, if None, no ouput.
    :return: parsed paragraph list
    """
    paragraphs = []
    entities = parse_ann_file(src_filename + '.ann')
    text = read_file(src_filename + '.txt')
    meta_info = None
    tokens = None
    if os.path.exists(src_filename + '.meta'):
        meta_info = read_meta_info(src_filename)
    if os.path.exists(src_filename + '.tok'):
        tokens = parse_tok_file(src_filename)
    for line_index, (line, (start, end)) in enumerate(zip(*split_into_lines(text))):
        line_entities = select_entity_by_offset(entities, start, end)
        line_entities = adjust_entities_offsets(line_entities, -start)
        check_entities(line_entities, line)
        dirname = os.path.dirname(src_filename)
        basename = os.path.basename(src_filename)
        paragraph = {'text': line, 'entities': line_entities, 'dir': dirname, 'file': basename}
        if meta_info:
            paragraph.update(meta_info[line_index])
        if tokens:
            paragraph['tokens'] = tokens['tokens'][line_index]
            if 'pos_tags' in tokens:
                paragraph['pos_tags'] = tokens['pos_tags'][line_index]
        paragraphs.append(paragraph)
    if dest_filename:
        write_json(dest_filename, paragraphs)
    return paragraphs


def brat2jsonl(filenames, dest_filename):
    """
    transform brat files into paragraph list and dump into json line file
    :param filenames: brat filenames, without suffix
    :param dest_filename: destination json line file
    :return: parsed paragraphs
    """
    metadata = read_meta_infos(filenames)
    paragraphs = []
    for filename in filenames:
        entities = parse_ann_file(filename + '.ann')
        text = read_file(filename + '.txt')
        for line_index, (line, (start, end)) in enumerate(zip(*split_into_lines(text))):
            line_entities = select_entity_by_offset(entities, start, end)
            line_entities = adjust_entities_offsets(line_entities, -start)
            paragraph = metadata[filename][line_index]
            paragraph['text'] = line
            paragraph['entities'] = line_entities
            paragraphs.append(paragraph)
    write_file(dest_filename, '\n'.join(json.dumps(para) for para in paragraphs))
    return paragraphs


def parse_ann_file(filename):
    entities = []
    for line in read_lines(filename):
        index, metainfo, text = line.split('\t')
        if index.startswith('T'):
            entity_type, start, end = metainfo.split(' ')
            start = int(start)
            end = int(end)
            entity = {'entity': text, 'start': start, 'end': end, 'type': entity_type, 'id': index}
            entities.append(entity)
    return entities


def parse_tok_file(filename):
    """
    parse tokenized file
    :param filename: tokenized filename, without suffix
    :return: parsed tokens and pos tags
    """
    tok_lines = read_lines(filename + '.tok')
    raw_lines = read_lines(filename + '.txt')
    if len(raw_lines) != len(tok_lines):
        raise Exception('line count not equal')
    if not tok_lines:
        return [[]]
    is_pos = all('_' in tok for tok in tok_lines[0].split(' ') if tok)

    tokens = []
    pos_tags = []
    for tok_line in tok_lines:
        sent_tokens = []
        sent_pos_tags = []
        for token in tok_line.rstrip().split(' '):
            if not token:
                continue
            if is_pos:
                split_index = token.rindex('_')
                sent_tokens.append(token[:split_index])
                sent_pos_tags.append(token[split_index + 1:])
            else:
                sent_tokens.append(token)
        if is_pos:
            pos_tags.append(sent_pos_tags)
        tokens.append(sent_tokens)

    result = {'tokens': tokens}
    if is_pos:
        result['pos_tags'] = pos_tags

    return result


def parse_ann_folder(dir_name, has_text=False):
    """
    parse brat folder to get entities
    :param dir_name: brat folder
    :param has_text: whether return the text correspondint to entities
    :return: parsed entities and text
    """
    filenames = set()
    data = []
    for filename in os.listdir(dir_name):
        if not filename.startswith('.') and filename.endswith('.ann'):
            filenames.add(dir_name + '/' + filename[:filename.rindex('.')])
    for filename in filenames:
        entities = parse_ann_file(filename)
        if has_text:
            text = read_file(filename + '.txt')
            data.append({'text': text, 'entities': entities, 'index': filename[filename.rindex('/') + 1:]})
        else:
            data.append(entities)
    return data


def get_brat_filename(dirname):
    """
    get brat filenames in folder, without suffix
    :param dirname: brat folder
    :return: brat filenames
    """
    filenames = set()
    for filename in get_filenames_in_folder(dirname):
        if filename.endswith(('.txt', '.ann')):
            filenames.add(filename[:filename.rindex('.')])
    for filename in filenames:
        if not os.path.exists(filename + '.txt') or not os.path.exists(filename + '.ann'):
            raise Exception('brat file does not exist.')
    return list(filenames)


def group_paragraphs(paragraphs, flatten_section=True):
    """
    group paragraphs by patent id
    :param paragraphs: paragraph list
    :param flatten_section: whether flatten section
    :return: grouped paragraphs
    """
    paragraph_dict = {}
    for paragraph in paragraphs:
        patent_id = paragraph['patent_id']
        section = paragraph['section']
        if patent_id not in paragraph_dict:
            paragraph_dict[patent_id] = {section: [paragraph]}
        elif section not in paragraph_dict[patent_id]:
            paragraph_dict[patent_id][section] = [paragraph]
        else:
            paragraph_dict[patent_id][section].append(paragraph)

    for patent in paragraph_dict.values():
        for section in patent.values():
            section.sort(key=lambda p: p['index'])

    if flatten_section:
        for patent_id, patent in paragraph_dict.items():
            paragraphs = []
            if 'title' in patent:
                paragraphs += patent['title']
            if 'abstract' in patent:
                paragraphs += patent['abstract']
            if 'claim' in patent:
                paragraphs += patent['claim']
            if 'description' in patent:
                paragraphs += patent['description']
            paragraph_dict[patent_id] = paragraphs

    return paragraph_dict


def split_into_lines(text):
    """
    split text into lines
    :param text: original text
    :return: line list
    """
    start = 0
    spans = []
    lines = []
    for line in text.splitlines(keepends=True):
        lines.append(line)
        end = start + len(line)
        spans.append((start, end))
        start = end
    return lines, spans


def select_entity_by_offset(entity_list, start, end):
    """
    select entity by start and end in entity list
    :param entity_list: entity object list
    :param start: start index
    :param end: end index
    :return: selected entities
    """
    new_entity_list = []
    for entity in entity_list:
        entity_start = entity['start']
        entity_end = entity['end']
        if start <= entity_start < entity_end <= end:
            new_entity_list.append(entity)
    return new_entity_list


def read_meta_info(filename):
    """
    read meta info in singe file
    :param filename: file path, without suffix
    :return: parsed meta info, flatten into list
    """
    paragraph_infos = []
    if not os.path.exists(filename + '.meta'):
        raise Exception('meta info file doesn\'t existed')
    for line in read_lines(filename + '.meta'):
        patent_id, section, index = line.split('\t')
        index = int(index)
        dirname, basename = os.path.split(filename)
        item = {'patent_id': patent_id, 'section': section, 'index': index,
                'dirname': dirname, 'filename': basename}
        paragraph_infos.append(item)

    return paragraph_infos


def read_meta_infos(filenames):
    """
    read meta info files
    :param filenames: meta info file paths
    :return: parsed meta info
    """
    data = {}
    for filename in filenames:
        data[filename] = read_meta_info(filename)
    return data


def parse_meta_info(filenames):
    """
    parse meta info files, group into patent id and section
    :param filenames: meta info filenames
    :return: parsed meta data
    """
    data = {}
    for filename in filenames:
        if not os.path.exists(filename + '.meta'):
            raise Exception('meta info file doesn\'t existed')
        filename += '.meta'
        for line_index, line in enumerate(read_lines(filename)):
            patent_id, section, index = line.split('\t')
            index = int(index)
            item = {'line_index': line_index, 'brat_filename': filename, 'index': index}
            if patent_id not in data:
                data[patent_id] = {section: [item]}
            elif section not in data[patent_id]:
                data[patent_id][section] = [item]
            else:
                data[patent_id][section].append(item)
    for item in data.values():
        for indices in item.values():
            indices.sort(key=lambda i: i['index'])
    return data
