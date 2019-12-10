# -*- coding: UTF-8 -*-
from figure_en.utils.exception import *
from figure_en.entity import Entity
from figure_en.utils.constant import DEFAULT_TYPE, SEQ_BILOU, SEQ_BIO


def label2entity(text, tokens, labels, label_schema=SEQ_BILOU, entity_in_dict=True):
    if label_schema == SEQ_BILOU:
        entities = label2entity_bilou(text, tokens, labels)
    elif label_schema == SEQ_BIO:
        entities = label2entity_bio(text, tokens, labels)
    else:
        raise ValueError('label schema is not support')
    if entity_in_dict:
        entities = [e.to_json() for e in entities]
    return entities


def label2entity_bio(text, tokens, labels):
    if len(tokens) != len(labels):
        raise LengthNotEqualException('label2entity: token and label count are not equal.')
    entities = []
    start = -1
    entity_text = ''
    prev_labels = ['S'] + labels[:-1]

    for index, (token, prev_label, label) in enumerate(zip(tokens, prev_labels, labels)):
        if label.startswith('O'):
            if entity_text:
                end = tokens[index - 1]['end']
                entity = Entity(text[start:end], start, end, label2entity_type(label))
                entities.append(entity)
                entity_text = ''
        elif label.startswith('B'):
            if entity_text:
                entity = Entity(entity_text, start, start + len(entity_text),
                                label2entity_type(label))
                entities.append(entity)
            entity_text = token['text']
            start = token['start']
        elif label.startswith('I'):
            entity_text += token['text']

    if entity_text:
        end = tokens[-1]['end']
        entity = Entity(text[start:end], start, end, label2entity_type(labels[-1]))
        entities.append(entity)
    return entities


def label2entity_bilou(text, tokens, labels):
    if len(tokens) != len(labels):
        raise LengthNotEqualException('label2entity: token and label count are not equal.')
    entities = []
    start = -1
    entity_text = ''
    prev_labels = ['S'] + labels[:-1]

    for token, prev_label, label in zip(tokens, prev_labels, labels):
        if label.startswith('U'):
            entity = Entity(token['text'], token['start'], token['end'], label2entity_type(label))
            entities.append(entity)
            entity_text = ''
        elif label.startswith('B'):
            start = token['start']
            entity_text = token['text']
        elif label.startswith('L'):
            if prev_label[0] in {'S', 'O', 'U'}:
                start = token['start']
            end = token['end']
            entity = Entity(text[start:end], start, end, label2entity_type(label))
            entities.append(entity)
            entity_text = ''
        elif label.startswith('I'):
            if prev_label[0] in {'S', 'O', 'U'}:
                start = token['start']
                entity_text = token['text']
            else:
                entity_text += token['text']
    if entity_text:
        end = tokens[-1]['end']
        entity = Entity(text[start:end], start, end, label2entity_type(labels[-1]))
        entities.append(entity)
    return entities


def label2entity_type(label):
    if len(label) > 2:
        entity_type = label[2:]
    else:
        entity_type = DEFAULT_TYPE
    return entity_type
