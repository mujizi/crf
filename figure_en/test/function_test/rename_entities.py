import json
from figure_en.utils.io import read_json

f = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/result_48.json')
print(f[0].keys())
print(f[0]['get_parts'])
print(len(f[0]['get_parts']))

res_list = []
for patent in f:
    res = {}
    res['pn'] = patent['pn']
    res['pid'] = patent['pid']
    res['text'] = patent['text']
    entities = []
    for entity in patent['get_parts']:
        id_dic = {}
        name_dic = {}
        id_dic['entity'] = entity['id']
        id_dic['start'] = entity['i_s']
        id_dic['end'] = entity['i_e']
        id_dic['type'] = 'part_id'

        name_dic['entity'] = entity['name']
        name_dic['start'] = entity['n_s']
        name_dic['end'] = entity['n_e']
        name_dic['type'] = 'part_name'

        entities.append(name_dic)
        entities.append(id_dic)

    res['entities'] = entities
    res_list.append(res)

print(len(res_list))

with open('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/entities_48.json', 'w') as f:
    json.dump(res_list, f)