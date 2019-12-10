from figure_en.en_get_parts_task.utils.tools import *
import re

FILTER_ID = re.compile(r"\”|\“|\@|\!|\#|\$|\%|\^|\&|\*|\+|\<|\>|\?|\;|\:|\—|\°C|[A-Z]{3,6}|OF")
# FILTER_NAME = re.compile(r"([a-z])\1{2}|\d")
FILTER_NAME = re.compile(r"(?: at\b| is\b| by\b| in\b| of\b| are\b| was\b| No\b|^No$| of\b|[Rr]ange|[Ff]ormula|[Nn]umeral|\#|\!|\:|\%|\;|\+|\@|\?|\$|\*|[A-Z]{5,15}|\d|([a-z])\1{2}|[Ff]igures?|FIGURES?|^[Ff]igs?|FIGS?)")


def relation_pair(entities):
    new = []
    for entity in entities:
        if entity['type'] == 'part_id':
            # print(entity['entity'])
            ie = entity['end']
            part_ids, ie = clean_part_id(entity['entity'], ie)
            for part_id in part_ids:
                dic = {'entity': part_id,
                       'start': entity['start'],
                       'end': ie,
                       'type': 'part_id'}
                new.append(dic)
        elif entity['type'] == 'part_name':
            new.append(entity)

    new.sort(key=(lambda i: i['end']))
    new_pair = []
    for i in range(0, len(new)):
        if new[i]['type'] == 'part_id' and (not FILTER_ID.search(new[i]['entity'])) and (len(new[i]['entity']) < 7):
            if new[i - 1]['type'] == 'part_name' and (not FILTER_NAME.search(new[i - 1]['entity'])):
                pair = {'id': new[i]['entity'],
                        'name': new[i - 1]['entity'],
                        'id_start': new[i]['start'],
                        'id_end': new[i]['end'],
                        'name_start': new[i - 1]['start'],
                        'name_end': new[i - 1]['end']
                        }
                new_pair.append(pair)

            elif new[i - 1]['type'] == 'part_id' and (not FILTER_ID.search(new[i - 1]['entity'])) and (len(new[i - 1]['entity']) < 7):
                for j in new[:i - 1][::-1]:
                    if j['type'] == 'part_name' and (not FILTER_NAME.search(j['entity'])):
                        pair = {'id': new[i]['entity'],
                                'name': j['entity'],
                                'id_start': new[i]['start'],
                                'id_end': new[i]['end'],
                                'name_start': j['start'],
                                'name_end': j['end']
                                }
                        new_pair.append(pair)
                        break

    return new_pair


def relation_repeat(new):
    new.sort(key=(lambda i: i['end']))
    new_pair = []
    for i in range(0, len(new)):
        if new[i]['type'] == 'part_id':
            if new[i - 1]['type'] == 'part_name':
                pair = {'id': new[i]['entity'],
                        'name': new[i - 1]['entity'],
                        'id_s': new[i]['start'],
                        'id_e': new[i]['end'],
                        'name_s': new[i - 1]['start'],
                        'name_e': new[i - 1]['end']
                        }
                new_pair.append(pair)

            elif new[i - 1]['type'] == 'part_id':
                for j in new[:i - 1][::-1]:
                    if j['type'] == 'part_name':
                        pair = {'id': new[i]['entity'],
                                'name': j['entity'],
                                'id_s': new[i]['start'],
                                'id_e': new[i]['end'],
                                'name_s': j['start'],
                                'name_e': j['end']
                                }
                        new_pair.append(pair)
                        break

    return new_pair
