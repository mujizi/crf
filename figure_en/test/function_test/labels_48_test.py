import json

with open('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/labels_48.json', 'r') as f:
    o = json.load(f)
n = 0
for i in o:
    n += 1
print(n)
print(len(o[0]['labels']))
print(o[0]['entities'])
print(o[0]['tokens'])

# print(o[0]['labels'].keys())