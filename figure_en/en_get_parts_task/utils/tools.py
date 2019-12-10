import re
import pandas as pd

HTML_TAG_PAT1 = re.compile(r"<b>|<\/b>|<\/i>|<i>|<sub>|<\/sub>")
# HTML_TAG_PAT2 = re.compile(r"<i>([A-Za-z]+\.?\s?)</i>")
HTML_TAG_RPL = r"\g<1>"
FIG_ID_PATTERN = re.compile(r"(\d{0,5})([A-Za-z]?)")
LETTER_NUMS = re.compile(r"([A-Za-z])(\d{0,4})")
MAX_CONTINUOUS_FIGS_NUM = 30
LETTER = re.compile(r"[A-Za-z]")
DOT = re.compile(r'\d+\.\d+')


def replace_html_part_id(entities):
    for i in entities:
        i['entity'] = replace_html_tag(i['entity'])
    return entities


def replace_html_tag(sentence):
    # replace the html tag to blank str
    # so that we could get the correct offset.
    new_sentence = re.sub(HTML_TAG_PAT1, '', sentence)
    return new_sentence


def get_original_index(tgt, ss, oss, tki, oi, ci):
    while ci < tgt:
        ci += len(ss[tki])
        oi += len(oss[tki])
        # print(tki, "#"+ss[tki]+ "#" +oss[tki]+"#", str(ci) + "="+ str(oi))
        tki += 1
    # assert ci == tgt, "can not match target index"
    return oi, tki, oi, ci


def get_id_group(fid):
    mt = FIG_ID_PATTERN.match(fid)
    if not mt: return ('', '')
    else: return mt.groups()


def get_id_range(s, e):
    if not s and not e: return []
    if not e: return [s]
    num_id = s.isdigit() and e.isdigit()
    if num_id and (not s or int(s)==0): return []
    # lower case
    if not num_id and s.islower() != e.islower(): s, e = s.lower(), e.lower()
    if num_id: s, e = int(s), int(e)
    else: s, e = ord(s), ord(e)
    if s > e: s, e = e, s # revert
    if num_id and (e-s) > MAX_CONTINUOUS_FIGS_NUM: return [str(s)]
    if num_id: return [str(n) for n in range(s, e+1)]
    else: return [chr(n) for n in range(s, e+1)]


def expand_ids(fig_id):
    # extend '图1到5' or '图1-5'
    ids = [it for it in fig_id.split("-") if it]
    if len(ids) < 2:
        return ids

    # X1-X1
    elif len(ids) == 2 and ids[0] == ids[1]:
        return [ids[0]]

    elif len(ids) == 2 and ids[0].isdigit() and LETTER.match(ids[1]):
        return [fig_id]

    # 11-15到20 just return 11-15
    s, e = ids[0], ids[1]

    # # a1 - a10
    # mt1 = LETTER_NUMS.match(s)
    # mt2 = LETTER_NUMS.match(e)
    # if mt1 and mt2:
    #     l = mt1.groups()[0]
    #     n_s = mt1.groups()[1]
    #     n_e = mt2.groups()[1]
    #     if n_e > n_s:
    #         return [l + i for i in get_id_range(n_s, n_e)]

    s_sid, s_ch = get_id_group(s)
    e_sid, e_ch = get_id_group(e)
    if not s_sid or int(s_sid)==0: return []
    if s_sid == e_sid and s_ch and e_ch:
        return [s_sid + c for c in get_id_range(s_ch, e_ch)]
    elif s_sid and not e_sid and s_ch and e_ch:
        return [s_sid + c for c in get_id_range(s_ch, e_ch)]
    elif s_sid and e_sid:
        if int(s_sid) > int(e_sid): return [fig_id]
        elif s_ch == e_ch: return [n+s_ch for n in get_id_range(s_sid, e_sid)]
        elif not s_ch and e_ch: return [n+e_ch for n in get_id_range(s_sid, e_sid)]
        else: return [n+s_ch for n in get_id_range(s_sid, e_sid)]
    elif s_sid and e_ch: return [fig_id.replace("-", "")]
    else: return []


def clean_part_id(id, _ie):
    if id.endswith(", "):
        id = id[:-2]
        _ie = _ie - 2

    elif id.endswith(" ") or id.endswith(","):
        id = id[:-1]
        _ie = _ie - 1

    id = id.replace("and", ",").replace("~", "-").replace(" ", "").replace("to", "-").replace(",,", ",")
    if "-" in id and ',' not in id:
        part_ids = expand_ids(id)
        for i in part_ids:
            if i == '':
                print('ex')
    elif "-" not in id:
        part_ids = id.split(",")
        for i in part_ids:
            if i == '':
                part_ids
    else:
        part_ids = []
    return part_ids, _ie


def merge_rule_crf(rule_entities, crf_entities):
    rule_id_l = [i['label_id'] for i in rule_entities]
    for i in crf_entities:
        if DOT.search(i['label_id']):
            for j in rule_entities:
                if j['items'][0]['label_id_start'] == i['items'][0]['label_id_start'] and j['items'][0]['label_id_end'] < i['items'][0]['label_id_end']:
                    rule_entities.remove(j)
        if i['label_id'] not in rule_id_l:
            rule_entities.append(i)
    return rule_entities


# def merge_rule_crf(rule_entities, crf_entities):
#     rule_start_map = {it["id_start"]: it for it in rule_entities}
#     # print(rule_start_map)
#     # new_rule_entities = rule_entities
#     # print(new_rule_entities)
#     for cit in crf_entities:
#         # add
#         if cit["id_start"] not in rule_start_map:
#             # new_rule_entities.append(cit)
#             rule_start_map[cit["id_start"]] = cit
#         # delete
#         elif DOT.search(cit["id"]):
#             # print(rit)
#             # new_rule_entities.remove(rule_start_map[cit["id_start"]])
#             rule_start_map.pop(cit["id_start"])
#         # update
#         elif cit["id_end"] > rule_start_map[cit["id_start"]]["id_end"]:
#             # new_rule_entities.remove(rule_start_map[cit["id_start"]])
#             # new_rule_entities.append(cit)
#             rule_start_map[cit["id_start"]] = cit
#     return list(rule_start_map.values())


def extract_single_patent(pn, src):
    f = pd.read_csv(src)

    for i in range(0, len(f['patent_number'])):
        if f.loc[i]['patent_number'] == pn:
            print(f.loc[i]['desc_text'])
    return f.loc[i]['desc_text']



def rule_entity_map(mapper, entities, text):
    if not mapper:
        return entities
    for entity in entities:
        entity['start'] = mapper[entity['start']]
        entity['end'] = mapper[entity['end'] - 1] + 1
        entity['entity'] = text[entity['start']:entity['end']]
    return entities


def voting(entities):
    if not entities: return []
    signs = {}
    for sign in entities:
        _sid = sign["id"]
        _sname = sign["name"]
        _tmp = {
            "label_id_start": sign["id_start"], "label_id_end": sign["id_end"],
            "label_txt_start": sign["name_start"], "label_txt_end": sign["name_end"],
            "label_txt": sign["name"], "label_id": _sid
        }
        if _sid in signs:
            signs[_sid]["items"].append(_tmp)
            if _sname in signs[_sid]["names"]:
                signs[_sid]["names"][_sname] += 1
            else:
                signs[_sid]["names"][_sname] = 1
        else:
            signs[_sid] = {"items": [_tmp], "names": {_sname: 1}}

    result = []
    for sid, sign in signs.items():
        _max = 0
        _name = ""
        for n, c in sign["names"].items():
            if c > _max: _name, _max = n, c
        res = {"label_id": sid, "representive_label_txt": _name, "items": []}
        for i in sign["items"]:
            i["representive"] = (i["label_txt"] == _name)
            res["items"].append(i.copy())
        result.append(res)
    return result

if __name__ == '__main__':
    cases = ['5-q', '2a-2e', 'S1-S10', '2-2', 'W\'- E\'', '8, 8\'','16\', 18\', 26\', and 27\'','13 and 13\'', '10-1']
    for fid in cases:
        print(fid, clean_part_id(fid))