# -*- coding: UTF-8 -*-
import re
import unicodedata


class TextPreprocessor(object):
    html_tag_regex = re.compile(
        '<div[^>]*>|</div>|<math[^>]*>[^<>]*</math(s)?>|<dl[^>]*>|</dl>|<dt[^>]*>|</dt>|'
        '<dd[^>]*>|</dd>|<ul[^>]*>|</ul>|<li[^>]*>|</li>|<ol[^>]*>|</ol>|'
        '<span[^>]*>|</span>|<sup>|</sup>|<sub>|</sub>|<!--[^!]*-->|'
        '<u>|</u>|<b>|</b>|<i>|</i>|<br ?/>|<table[^>]*>|</table>|<tr[^>]*>|</tr>|<td[^>]*>|</td>')
    whitespace_regex = re.compile(r' +')

    def process(self, text,
                is_split_line=True,
                is_normalize_text=True,
                is_skip_empty_line=True,
                is_remove_html_tag=True,
                is_remove_space=False):
        """
        process input text
        :param text: input raw text
        :param is_split_line: whether split text into lines (final step)
        :param is_normalize_text: whether normalize text
        :param is_skip_empty_line: whether skip empty lines (only work when is_split_line=True)
        :param is_remove_html_tag: whether remove html tag
        :param is_remove_space: whether remove whitespace
        :return processed text and index mapper (processed text to input text, character level)
        """

        raw_text = text
        index_mapper_queue = []
        if is_normalize_text:
            text, norm_index_mapper = self.normalize_text(text, True)
            index_mapper_queue.append(norm_index_mapper)
        if is_remove_html_tag:
            text, rm_html_mapper = self.remove_html_tag(text)
            index_mapper_queue.append(rm_html_mapper)
        if is_remove_space:
            text, rm_space_mapper = self.remove_space(text)
            index_mapper_queue.append(rm_space_mapper)
        index_mapper = self.build_index_mapper(index_mapper_queue, len(raw_text))
        if is_split_line:
            lines = split_lines(text, skip_empty=is_skip_empty_line)
            return lines, index_mapper
        else:
            return text, index_mapper

    @classmethod
    def normalize_text(cls, text, return_index_mapper=False):
        if not return_index_mapper:
            return unicodedata.normalize('NFKD', text)
        mapper = {}
        normalized_text = ''
        norm_ch_offset = 0

        for char_index, char in enumerate(text):
            normalized_char = unicodedata.normalize('NFKD', char)
            normalized_text += normalized_char
            for char in normalized_char:
                mapper[norm_ch_offset] = char_index
                norm_ch_offset += 1

        return normalized_text, mapper

    @classmethod
    def remove_space(cls, text):
        return remove_chars_by_regex(cls.whitespace_regex, text)

    @classmethod
    def remove_html_tag(cls, text):
        return remove_chars_by_regex(cls.html_tag_regex, text)

    @classmethod
    def build_index_mapper(cls, index_mapper_queue, text_len):
        if not index_mapper_queue:
            final_mapper = {char_idx: char_idx for char_idx in range(text_len)}
        elif len(index_mapper_queue) == 1:
            final_mapper = index_mapper_queue.pop()
        else:
            final_mapper = index_mapper_queue.pop(0)
            for mapper in index_mapper_queue:
                iter_mapper = {}
                for k, v in mapper.items():
                    iter_mapper[k] = final_mapper[v]
                final_mapper = iter_mapper
        return final_mapper


class TextEntityProcessor(TextPreprocessor):
    def process_data(self, data,
                     is_normalize_text=True,
                     is_remove_html_tag=True,
                     is_remove_space=False):
        """
        process data with text and entities (normalize text and entities at the same time)
        :param data: input data to be processed
        :param is_normalize_text: whether normalize text
        :param is_remove_html_tag: whether remove html tag
        :param is_remove_space: whether remove whitespace
        :return: processed data
        """
        text = data['text']
        entities = data['entities']
        text, index_mapper = super().process(text,
                                             is_split_line=False,
                                             is_normalize_text=is_normalize_text,
                                             is_remove_html_tag=is_remove_html_tag,
                                             is_remove_space=is_remove_space)
        reversed_mapper = reverse_index_mapper(index_mapper)
        for entity in entities:
            start = reversed_mapper[entity['start']]
            end = reversed_mapper[entity['end']]
            entity['entity'] = text[start:end]
            entity['start'] = start
            entity['end'] = end
        data['text'] = text
        return data


def remove_chars_by_regex(regex, text):
    """
    remove matched text of regex, return new text and index mapper
    :param regex: regex to do text removing
    :param text: original text
    :return: processed text and index mapper (processed text to input text, character level)
    """
    offset = 0
    new_text = ''
    last_end = 0
    mapper = {}
    for item in regex.finditer(text):
        start = item.start()
        end = item.end()
        new_text += text[last_end:start]
        for idx in range(last_end, start):
            mapper[idx - offset] = idx
        offset += end - start
        last_end = end

    if last_end < len(text):
        new_text += text[last_end:]
        for idx in range(last_end, len(text)):
            mapper[idx - offset] = idx

    return new_text, mapper


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

