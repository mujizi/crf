# -*- coding: UTF-8 -*-
import copy
import sys
from shutil import copyfile
from ..utils.utils import *
from ..utils.io import *
from ..utils.constant import *
from ..tokenizer import Tokenizer


def prepare_brat_data(src_filename, dest_dirname, file_size_threshold=40):
    """
    prepare brat annotation data
    :param src_filename: source json line file with paragraph list
    :param dest_dirname: destination brat folder path
    :param file_size_threshold: every txt file size of brat
    :return: None
    """
    tokenizer = Tokenizer()
    if not os.path.exists(dest_dirname):
        os.mkdir(dest_dirname)
    segments = allocate_annotation_data(src_filename, file_size_threshold)
    for segment_index, segment in enumerate(segments, 1):
        file_basename = dest_dirname + str(segment_index)
        prepare_brat_file_pair(segment['text'], segment['entities'], file_basename)
        write_file(file_basename + '.tok', tokenizer.tokenize(segment['text']))
        infos = ['\t'.join([info['patent_id'], info['section'], str(info['index'])]) for info in segment['info']]
        write_file(file_basename + '.meta', '\n'.join(infos))
    copy_config(dest_dirname)


def allocate_annotation_data(src_jsonl_filename, text_size_threshold=40):
    """
    aggregate paragraph items into segment by text size (kb), used to restrict brat txt file size.
    This method's intuition is brat webpage will be very slow when text is large.
    :param src_jsonl_filename: json line file path which stores the paragraph list
    :param text_size_threshold: text threshold in every brat txt file
    :return: allocated segment list
    """
    offset = 0
    text = ''
    entities = []
    meta_info = []
    segments = []
    file = open(src_jsonl_filename)
    for para_index, line in enumerate(file):
        paragraph = json.loads(line)
        check_entities(paragraph['entities'], paragraph['text'])
        para_text = paragraph['text']
        para_entities = paragraph['entities']
        info = {'patent_id': paragraph['patent_id'], 'section': paragraph['section'], 'index': paragraph['index']}
        if get_text_size(para_text) > text_size_threshold * 0.75:
            segment = {'text': para_text, 'entities': para_entities, 'info': [info]}
            segments.append(segment)
        else:
            para_entities = add_offset_on_entities(copy.deepcopy(paragraph['entities']), offset)
            offset += len(para_text)
            text += para_text
            entities.extend(para_entities)
            meta_info.append(info)
            if sys.getsizeof(text) // 1024 > text_size_threshold:
                segment = {'text': text, 'entities': entities, 'info': meta_info}
                segments.append(segment)
                text = ''
                entities = []
                offset = 0
                meta_info = []
    file.close()
    return segments


def get_text_size(text):
    return sys.getsizeof(text) // 1024


def get_file_size(filename):
    return os.stat(filename + '.txt').st_size


def prepare_brat_file_pair(text, entities, filename):
    """
    transform text and entities into brat txt and ann files
    :param text: original text
    :param entities: entities in text
    :param filename: brat destination filename, without suffix
    :return: None
    """
    ann_lines = []
    existed_ids = []
    ent_index = 1
    for entity in entities:

        e_id = get_entity_id(entity, ent_index)
        while e_id in existed_ids:
            ent_index += 1
            e_id = get_entity_id(entity, ent_index)

        existed_ids.append(e_id)
        type_and_bound = entity['type'] + ' ' + str(entity['start']) + ' ' + str(entity['end'])
        ann_line = '\t'.join((e_id, type_and_bound, entity['entity']))
        ann_lines.append(ann_line)
        ent_index += 1

    write_file(filename + '.txt', text)
    write_file(filename + '.ann', '\n'.join(ann_lines))


def get_entity_id(entity, index):
    """
    get entity id, if entity object has an id, return it. If no id in entity, return 'T' + index
    :param entity: entity object
    :param index: entity index candidate
    :return: calculated entity id
    """
    if 'id' in entity and entity['id'].startswith('T'):
        e_id = entity['id']
    else:
        e_id = 'T' + str(index)
    return e_id


def add_offset_on_entities(entities, offset):
    """
    add offset on entity object
    :param entities: entity list
    :param offset: offset value
    :return: processed entity list
    """
    for e in entities:
        e['start'] += offset
        e['end'] += offset
    return entities


def copy_config(dest_dir):
    """
    copy brat config file into dest folder -- brat folder
    :param dest_dir: brat destination folder
    :return:
    """
    ann_conf_file = dest_dir + 'annotation.conf'
    tool_conf_file = dest_dir + 'tools.conf'
    if not os.path.exists(ann_conf_file):
        copyfile(BRAT_CONFIG_DIR + 'annotation.conf', ann_conf_file)
    if not os.path.exists(tool_conf_file):
        copyfile(BRAT_CONFIG_DIR + 'tools.conf', tool_conf_file)
