import pandas as pd
import json
from figure_en.utils import io
from figure_en.tokenizer import Tokenizer
from figure_en.data_process.entity2label import *
from figure_en.utils.constant import *

f = pd.read_csv('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/all_parts')
f2 = io.read_jsonline('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/en_all_desc_for_validtion.json')
f3 = io.read_jsonline('/home/patsnap/PycharmProjects/crf/figure_en/data/figure_en/get_part_data/format_48.json')
pn_list = f['PN'].tolist()
id_list = f['ID'].tolist()
pid_list = f['PID'].tolist()

# for i in f2:
#     print(f2[0]['pid'])
#     for j in range(0, len(pn_list)):
#         if f2[i]['pid'] ==

f.dropna(axis=0, inplace=True)

print(len(f['ID'].tolist()))

for i in f2:
    for j in range(0, len(pn_list)):
        if i['pid'] == pid_list[j]:
            i['pn'] = pn_list[j]

new_pid = []
new_pn = []
new_text = []

for i in f2:
    new_pid.append(i['pid'])
    new_pn.append(i['pn'])
    new_text.append(i['desc'])

data = {'pn':new_pn, 'pid': new_pid, 'text':new_text}

df = pd.DataFrame(data=data, columns=['pn', 'pid', 'text'])
df.to_csv('../../data/figure_en/get_part_data/en_pn.csv')

print(new_pid)
print(new_pn)
zip_list = set(list(zip(new_pid, new_pn)))

n = 0
for i in f3:
    for j in range(0, len(new_pn)):
        if i['pid'] == new_pid[j]:
            i['pn'] = new_pn[j]

with open('../../data/figure_en/get_part_data/text_48.json', 'w') as f:

    json.dump(f3, f)