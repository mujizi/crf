from figure_en.utils.io import *


# f = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/evaluation/crf_validation.json')
# print(len(f))

# training_file = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/training.json')
validation_file = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/validation.json')
test_file = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/test.json')

train_entities = []
for line in validation_file:
    if line['entities'] != []:
        train_entities.extend(line['entities'])

print(len(train_entities)/2)
# print(train_entities)