import pandas as pd
from figure_en.utils.io import *
import re
ID_FILTER = re.compile('<div[^>]*>|</div>|<math[^>]*>[^<>]*</math(s)?>|<dl[^>]*>|</dl>|<dt[^>]*>|</dt>|'
                       '<dd[^>]*>|</dd>|<ul[^>]*>|</ul>|<li[^>]*>|</li>|<ol[^>]*>|</ol>|'
                       '<span[^>]*>|</span>|<sup>|</sup>|<sub>|</sub>|<!--[^!]*-->|'
                       '<u>|</u>|<b>|</b>|<i>|</i>|<br ?/>|<table[^>]*>|</table>|<tr[^>]*>|</tr>|<td[^>]*>|</td>')


def replace_html_tag(text):
    return ID_FILTER.sub('', text)


def get_text2json(src_text, src_json, dest):
    f2 = read_json(src_text)
    if src_json.endswith('.jsonl'):
        f = read_jsonline(src_json)
        for i in f:
            for j in f2:
                if i['pn'] == j['pn']:
                    i['text'] = j['text']
                    continue
    elif src_json.endswith('.json'):
        f = read_json(src_json)
        for i in f:
            for j in f2:
                if i['pn'] == j['pn']:
                    i['text'] = j['text']
                    continue

    write_jsonline(dest, f)


def index_test(src, name_index=True, id_index=True):
    f = read_jsonline(src)
    n = 0
    for i in f:
        get_parts = i['get_parts']
        pn = i['pn']
        text = i['text']
        for j in get_parts:
            if name_index:
                if text[j['items'][0]['label_txt_start']:j['items'][0]['label_txt_end']] != j['representive_label_txt']:
                    print(pn)
                    print(text[j['items'][0]['label_txt_start'] - 40 :j['items'][0]['label_txt_end'] + 40])
                    print(text[j['items'][0]['label_txt_start']:j['items'][0]['label_txt_end']])
                    print(j['representive_label_txt'])
                    n += 1
            elif id_index:
                if j['label_id'] not in replace_html_tag(text[j['items'][0]['label_id_start']:j['items'][0]['label_id_end']])  :
                    print(replace_html_tag(text[j['items'][0]['label_id_start']:j['items'][0]['label_id_end']]))
                    print(j['label_id'])
                    n += 1
    print('nums: %s' % (n))

if __name__ == '__main__':
    src_text = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/63_raw/batch_patent.json'
    src_json = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/new_map_result_6_5.json'
    src = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/new_map_result_text_6_5.json'
    index_test(src, id_index=True, name_index=False)

    # src_json = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/new_map_result_6_5.json'
    # dest = '/home/patsnap/PycharmProjects/crf/ner_figure_part/figure_en/en_get_parts_task/data/pre/new_map_result_text_6_5.json'
    # get_text2json(src_text, src_json, dest)
