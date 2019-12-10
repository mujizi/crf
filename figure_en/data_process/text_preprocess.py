# -*- coding: UTF-8 -*-
import re
import unicodedata


def text_preprocess(text, norm_text=False, skip_empty=True):
    """
    text preprocess function, including normalize text, remove whitespaces, split lines
    function will return processed lines, their spans in processed lines
    and all characters mapper between original text and lines
    :param text: original text to be processed
    :param norm_text: whether normalize text, default is False (EN). This is useful for CN
    :param skip_empty:  whether skip empty lines in result
    :return: processed lines, line spans in original text and character mapper between original text and lines
    """
    if norm_text:
        text, mapper = normalize_text(text)
    else:
        mapper = None
    lines = split_lines(text, skip_empty)

    return lines, mapper


def split_lines(text, skip_empty=True):
    """
    split text into lines, return lines and spans
    :param text: original text to be split
    :param skip_empty: whether skip empty lines in result
    :return: split lines and line spans
    """
    lines = []
    offset = 0
    for line_text in text.splitlines(keepends=True):
        if skip_empty and line_text.rstrip() or not skip_empty:
            line = {'text': line_text.rstrip(), 'start': offset,
                    'end': offset + len(line_text.rstrip())}
            lines.append(line)

        offset += len(line_text)

    return lines


SPACE_REGEX = re.compile(' +')
HTML_TAG_REGEX = re.compile(
    '<div[^>]*>|</div>|<math[^>]*>[^<>]*</math(s)?>|<dl[^>]*>|</dl>|<dt[^>]*>|</dt>|'
    '<dd[^>]*>|</dd>|<ul[^>]*>|</ul>|<li[^>]*>|</li>|<ol[^>]*>|</ol>|'
    '<span[^>]*>|</span>|<sup>|</sup>|<sub>|</sub>|<!--['
    '^!]*-->|<u>|</u>|<b>|</b>|<i>|</i>')

EN_PATTERN_START = re.compile('^[a-zA-Z]+')
EN_PATTERN_END = re.compile('[a-z]+$')


def normalize_text(text, return_mapper=True):
    """
    normalize text and remove redundant whitespaces
    :param text: text to be process
    :param return_mapper: whether return mapper index
    :return: processed text
    """
    mapper = {}
    norm_ch_offset = 0
    ori_text = text
    new_text = ''
    for ch_index, ch in enumerate(ori_text):
        normalized_ch = unicodedata.normalize('NFKD', ch)
        new_text += normalized_ch
        for ch in normalized_ch:
            mapper[norm_ch_offset] = ch_index
            norm_ch_offset += 1

    # select characters to be replaced, every item in replace position, original characters and replaced characters
    replace_configs = []
    for item in SPACE_REGEX.finditer(new_text):
        start = item.start()
        end = item.end()
        start_text = new_text[:start]
        end_text = new_text[end:]

        if EN_PATTERN_END.search(start_text) and EN_PATTERN_START.search(end_text):
            if end - start > 1:
                replace_configs.append((item.start(), item.group(), ' '))
        else:
            replace_configs.append((item.start(), item.group(), ''))
    for item in HTML_TAG_REGEX.finditer(new_text):
        replace_configs.append((item.start(), item.group(), ''))

    replace_configs = dedupe_replace_config(replace_configs)
    # replace characters
    if replace_configs:
        ori_text = new_text
        ori_mapper = mapper
        next_starts = [start for start, _, _ in replace_configs][1:] + [len(ori_text)]
        new_text = ori_text[:replace_configs[0][0]]
        new_mapper = {idx: idx for idx in range(0, replace_configs[0][0])}
        new_offset = 0

        for (start, ori_chars, replace_chars), next_start in zip(replace_configs, next_starts):
            end = start + len(ori_chars)
            new_text += replace_chars + ori_text[end:next_start]
            for char_index, char in enumerate(replace_chars):
                new_mapper[char_index + start - new_offset] = char_index + start
            for char_index, char in enumerate(ori_text[end:next_start]):
                new_mapper[start + char_index + len(replace_chars) - new_offset] = end + char_index
            new_offset += end - start - len(replace_chars)

        mapper = {new_idx: ori_mapper[old_idx] for new_idx, old_idx in new_mapper.items()}

    if return_mapper:
        return new_text, mapper
    else:
        return new_text


def data_preprocess(data):
    """
    text and entities preprocess simultaneously
    :param data: original data
    :return: processed data
    """
    text = data['text']
    entities = data['entities']
    new_text, mapper = normalize_text(text)

    mapper = reverse_index_mapper(mapper)
    for entity in entities:
        entity['start'] = mapper[entity['start']]
        entity['end'] = mapper[entity['end']]
        entity['entity'] = new_text[entity['start']:entity['end']]
    data['text'] = new_text
    data['entities'] = entities
    return data


def reverse_index_mapper(mapper):
    """
    reverse index mapper from new_index=>old_index to old_index=>new_index
    **notice**
        The most importance thing is some characters will become several characters.
        Therefore, new index should select the smallest value in this situation.
    :param mapper: mapper require to be reversed
    :return: reversed mapper
    """
    new_mapper = {}
    for new_index, old_index in mapper.items():
        if old_index not in new_mapper:
            new_mapper[old_index] = new_index
        elif new_mapper[old_index] > new_index:
            new_mapper[old_index] = new_index

    return new_mapper


def dedupe_replace_config(replace_configs):
    """
    dedupe the replace config spans
    :param replace_configs:
    :return:
    """
    replace_configs = sorted(set(replace_configs), key=lambda i: i[0])
    if not replace_configs:
        return replace_configs
    mapper = [0] * (replace_configs[-1][0] + len(replace_configs[-1][1]))
    replace_config_dict = {}
    for replace_config_item in replace_configs:
        offset_start, old_chars, new_chars = replace_config_item
        offset_end = offset_start + len(old_chars)
        bit_sum = sum(mapper[offset_start:offset_end])
        if not bit_sum:
            replace_config_dict[offset_start] = replace_config_item
            mapper[offset_start:offset_end] = [1] * (offset_end - offset_start)
        else:
            if bit_sum < len(old_chars):
                if offset_start in replace_config_dict:
                    replace_config_dict[offset_start] = replace_config_item
                else:
                    raise Exception('cross boundary')
    return sorted(replace_config_dict.values(), key=lambda i: i[0])


def replace_chars_in_text(text, replace_configs, is_dedeque=False):
    if is_dedeque:
        replace_configs = dedupe_replace_config(replace_configs)
    if not replace_configs:
        return text

    next_starts = [start for start, _, _ in replace_configs][:-1] + [len(text)]
    new_text = text[:replace_configs[0][0]]
    for (start, end, replace_ch), next_start in zip(replace_configs, next_starts):
        new_text += replace_ch + text[end:next_start]
    return new_text


def replace_chars_in_list(entity_list, replace_config, text):
    replace_config = sorted(replace_config, key=lambda c: c[0])
    index = 0

    while index < len(replace_config):
        offset_start, old_chars, new_chars = replace_config[index]
        entity_list = replace_chars(entity_list, offset_start, old_chars, new_chars, text)
        text = text[:offset_start] + new_chars + text[offset_start + len(old_chars):]
        offset_diff = len(new_chars) - len(old_chars)
        for conf_idx, (offset_start, old_chars, new_chars) in enumerate(replace_config[index + 1:], index + 1):
            replace_config[conf_idx] = (offset_start + offset_diff, old_chars, new_chars)
        index += 1
    return entity_list, text


def replace_chars(entity_list, offset_start, old_chars, new_chars, text):
    """

    :param entity_list: entity list
    :param offset_start: start position of replacement
    :param old_chars: old characters to be replaced
    :param new_chars: new characters to replace
    :param text: original text corresponding to entity list
    :return: replaced entity list
    """

    text_len = len(text)

    if text_len < offset_start:
        raise Exception('offset cross boundary')
    elif text[offset_start:offset_start + len(old_chars)] != old_chars:
        raise Exception('offset is not corresponding to old characters')

    str_len_diff = len(old_chars) - len(new_chars)
    offset_len_old = len(old_chars)
    offset_len_new = len(new_chars)
    offset_end = offset_start + offset_len_old
    new_entity_list = []
    for entity in entity_list:
        entity_start = entity['start']
        entity_end = entity['end']
        if offset_end <= entity_start:
            entity['start'] -= str_len_diff
            entity['end'] -= str_len_diff
        elif offset_start < entity_start < offset_end < entity_end:
            entity['end'] -= str_len_diff
            if offset_end - entity_start < str_len_diff:
                entity['start'] -= entity_start - offset_start + offset_len_new
                prefix = ''
            else:
                prefix = new_chars[offset_start + offset_len_new - entity_start:]

            entity['entity'] = prefix + entity['entity'][offset_end - entity_start:]
        elif entity_start <= offset_start < offset_end < entity_end:
            entity['end'] -= str_len_diff
            prefix = entity['entity'][:offset_start - entity_start]
            suffix = entity['entity'][offset_end - entity_start:]
            entity['entity'] = prefix + new_chars + suffix
        elif entity_start < offset_start < entity_end <= offset_end:
            entity['end'] = offset_start + offset_len_new
            entity['entity'] = entity['entity'][:offset_start - entity_start] + new_chars
        elif offset_start <= entity_start < entity_end <= offset_end:
            if not new_chars:
                continue
            entity['entity'] = new_chars
            entity['start'] = offset_start
            entity['end'] = offset_start + offset_len_new
        new_entity_list.append(entity)

    return new_entity_list


def adjust_entity_offset(entity_list, offset_start, offset_len=1):
    """

    :param entity_list:
    :param offset_start:
    :param offset_len:
    :return:
    """
    new_entity_list = []
    offset_end = offset_start + offset_len
    for entity in entity_list:
        entity_start = entity['start']
        entity_end = entity['end']
        if offset_end <= entity_start:
            entity['start'] -= offset_len
            entity['end'] -= offset_len
        elif offset_start <= entity_start < offset_end < entity_end:
            entity['start'] = offset_end
            entity['entity'] = entity['entity'][offset_end - entity_start:]
        elif entity_start < offset_start < offset_end < entity_end:
            entity['end'] -= offset_len
            entity['entity'] = entity['entity'][:offset_start - entity_start] + entity['entity'][
                                                                                offset_end - entity_start:]
        elif entity_start < offset_start < entity_end <= offset_start + offset_len:
            entity['end'] = offset_start
            entity['entity'] = entity['entity'][:offset_start - entity_start]
        else:
            continue

        new_entity_list.append(entity)
    return new_entity_list


if __name__ == '__main__':
    text = 'The oxide semiconductor layers <b>830</b><i>a </i>and <b>830</b><i>c </i>are'
    r = normalize_text(text)
    print(r)