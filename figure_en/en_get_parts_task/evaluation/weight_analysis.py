import joblib
from collections import Counter


MODEL_PATH = '/home/patsnap/PycharmProjects/crf/ner_figure_part/data/models/'
config = {'model_name': 'merge_data_v1.jl'}


def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-8s %s" % (weight, label, attr))


if __name__ == '__main__':
    crf = joblib.load(MODEL_PATH + config['model_name'])

    print("Top positive:")
    print_state_features(Counter(crf.state_features_).most_common(30))

    print("\nTop negative:")
    print_state_features(Counter(crf.state_features_).most_common()[-30:])
    # print(Counter(crf.state_features_).most_common()[-30:])