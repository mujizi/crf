# -*- coding: UTF-8 -*-
import sys
import copy
import unicodedata
from ..utils.utils import *
from ..utils.io import *
from ..utils.constant import *
from .json2brat import prepare_brat_data, prepare_brat_file_pair
from .brat2json import parse_ann_file, get_brat_filename
from .text_preprocess import *


def transform_into_paragrahs_from_dir(dirname, dest_filename, is_preprocess=True):
    filenames = get_filenames_in_folder(dirname)
    transform_into_paragraphs_from_files(filenames, dest_filename, is_preprocess)


def transform_into_paragraphs_from_files(filenames, dest_filename, is_preprocess=True):
    dest_file = open(dest_filename, 'w', encoding='utf-8')

    first = True
    for filename in filenames:
        paragraphs = patent_preprocess(filename, is_preprocess=is_preprocess)
        paragraph_strs = '\n'.join(json.dumps(para) for para in paragraphs)
        if not first:
            paragraph_strs = '\n' + paragraph_strs
        else:
            first = False
        dest_file.write(paragraph_strs)
    dest_file.close()


def patent_preprocess(filename, is_preprocess=True):
    paragraphs = []

    for paragraph in split_patent_into_paragraph(filename=filename):
        if is_preprocess:
            paragraph = normalize_text(paragraph, False)
        if not paragraph['text'].strip():
            continue
        paragraphs.append(paragraph)
        check_entities(paragraph['entities'], paragraph['text'])
    return paragraphs


def split_patent_into_paragraph(patent=None, filename=None):
    if patent and filename:
        raise Exception('provide two parameters')
    elif not patent and not filename:
        raise Exception('no parameter provided')
    elif not patent:
        patent = read_json(filename)
    paragraphs = []
    if 'text' in patent and 'entities' in patent:
        paragraphs = split_section_data(patent, 'None', patent['patent_id'])
    else:
        for section in PATENT_SECTIONS:
            paragraphs.extend(split_section_data(patent[section], section, patent['patent_id']))

    return paragraphs


def split_section_data(data, section_name, patent_id):
    paragraphs = split_into_paragraph(data)
    for paragraph_index, paragraph in enumerate(paragraphs):
        paragraph['section'] = section_name
        paragraph['index'] = paragraph_index
        paragraph['patent_id'] = patent_id
    return paragraphs


def split_into_paragraph(data):
    text = data['text']
    entities = data['entities']

    paragraphs = []
    for line, (start, end) in zip(*split_into_lines(text)):
        new_line = line.rstrip()
        new_end = start + len(new_line)
        para_entities = []
        for entity in select_entity_by_offset(entities, start, end):
            if entity['end'] > new_end:
                entity['end'] = new_end
            entity['start'] -= start
            entity['end'] -= start
            para_entities.append(entity)
        paragraph = {'text': new_line + '\n', 'entities': para_entities}
        check_entities(para_entities, new_line + '\n')
        paragraphs.append(paragraph)
    return paragraphs


def split_into_lines(text):
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
    new_entity_list = []
    for entity in entity_list:
        entity_start = entity['start']
        entity_end = entity['end']
        if start <= entity_start < entity_end <= end:
            new_entity_list.append(entity)
    return new_entity_list
