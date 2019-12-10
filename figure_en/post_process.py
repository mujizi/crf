# -*- coding: UTF-8 -*-
from figure_en.en_get_parts_task.predict.relation_pairs import *
from figure_en.en_get_parts_task.utils.tools import *


def post_process(entities, tokens=None):
    new_entities = replace_html_part_id(entities)
    pair_dic = relation_pair(new_entities)
    crf_entities = voting(pair_dic)
    return crf_entities


