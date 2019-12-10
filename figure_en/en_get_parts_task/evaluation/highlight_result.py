from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score
from figure_en.utils.io import read_json
from figure_en.crf_feature import CRFFeature
from figure_en.utils.evaluation import *
import joblib


class Evaluation():
    def recall(self, pred, true):
        tp_add_fn = 0
        tp = 0
        for i in range(0, len(true)):
            if true[i] != 'O':
                tp_add_fn += 1
                if true[i] == pred[i]:
                    tp += 1
        return tp / tp_add_fn

    def precision(self, pred, true):
        fp = 0
        tp = 0
        for i in range(0, len(true)):
            if true[i] == 'O' and pred[i] != 'O':
                fp += 1
            elif true[i] != 'O' and true[i] == pred[i]:
                tp += 1
        return tp / (tp + fp)

    def f1(self, pred, true):
        return 2 * self.precision(pred, true) * self.recall(pred, true) / (self.precision(pred, true) + self.recall(pred, true))

    def evaluate_result(self, pred, true):
        print('precision:', '{0:.4f}'.format(self.precision(pred, true)))
        print('recall:', '{0:.4f}'.format(self.recall(pred, true)))
        print('f1:', '{0:.4f}'.format(self.f1(pred, true)))


if __name__ == '__main__':
    # data = read_json('/home/patsnap/PycharmProjects/crf/figure_en/data/test_oov.json')
    # labels = [i['labels'] for i in data]
    #
    # features = []
    # for o in data:
    #     tokens = o['tokens']
    #     feat = CRFFeature(tokens).sent2feature()
    #     features.append(feat)
    #
    # crf = joblib.load('/home/patsnap/PycharmProjects/crf/figure_en/data/models/crf_rule_v1.jl')
    # predicted = crf.predict(features)
    #
    # predicted = [i for j in predicted for i in j]
    # labels1 = [i for j in labels for i in j]
    # print('macro:{}'.format(precision_score(labels1, predicted, average='macro')))
    # print('micro:{}'.format(precision_score(labels1, predicted, average='micro')))
    #
    # eva = Evaluation()
    # eva.evaluate_result(predicted, labels1)
    # model_result_highlight('crf', 'validation')
    # model_result_highlight('crf', 'test', RESULT_DISPLAY)
    model_result_highlight('crf', 'test', RESULT_MISSING)


