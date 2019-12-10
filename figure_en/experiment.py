# -*- coding: UTF-8 -*-
"""
experiment runner functions and settings
"""
from figure_en.crf_tagger import CRFTagger
from figure_en.utils.utils import *
from figure_en.utils.io import *
from figure_en.utils.constant import *
from figure_en.utils.evaluation import *
from figure_en.post_process import post_process
from figure_en.entity import Entity


class Experiment(object):
    def __init__(self, model_name):
        self.model_name = model_name

    def train(self, training_filename):
        raise NotImplementedError("train not implemented")

    def inference(self, text):
        raise NotImplementedError("inference not implemented")

    def inference_file(self, src_filename, dest_filename):
        raise NotImplementedError("inference_file not implemented")

    def evaluation(self, pred_data, true_data):
        raise NotImplementedError("evaluation not implemented")


class CRFExperiment(Experiment):
    def __init__(self, model_name, feature_sets, remark=''):
        super().__init__(model_name)
        if remark and not remark.startswith(('-', '_')):
            remark = '_' + remark
        self.remark = remark
        self.feature_sets = feature_sets
        self.basename = model_name + remark
        self.tagger = CRFTagger(self.basename, feature_sets=feature_sets)

    def train(self, filename=TRAINING_FILE):
        self.tagger.train(self.get_name(filename, self.remark))
        return self

    def inference(self, text):
        return self.tagger.inference(text)

    def inference_json(self, data):
        for paragraph in data:
            tokens = paragraph['tokens']
            text = paragraph['text']
            entities = self.tagger.inference_tokens(text, tokens)
            if EXP_CONFIG['postprocess']:
                entities = post_process(text, entities)
            paragraph['entities'] = entities
        return data

    def inference_file(self, src_filename, dest_filename):
        result = self.inference_json(read_json(src_filename))
        write_json(dest_filename, result, serialize_method=Entity.to_json)

    def evaluation(self, pred_data=None, true_data=None):
        validation_pred_filename = EVALUATION_DIR + self.basename + '_validation.json'
        validation_true_filename = DATA_DIR + EXP_CONFIG[VAR_VALIDATION_FILE]
        validation_oov_pred_filename = EVALUATION_DIR + self.basename + '_validation_oov.json'
        validation_oov_true_filename = DATA_DIR + EXP_CONFIG[VAR_VALIDATION_OOV_FILE]

        test_pred_filename = EVALUATION_DIR + self.basename + '_test.json'
        test_true_filename = DATA_DIR + EXP_CONFIG[VAR_TEST_FILE]
        test_oov_pred_filename = EVALUATION_DIR + self.basename + '_test_oov.json'
        test_oov_true_filename = DATA_DIR + EXP_CONFIG[VAR_TEST_OOV_FILE]

        self.inference_file(validation_true_filename, validation_pred_filename)
        if os.path.exists(validation_oov_true_filename):
            self.inference_file(validation_oov_true_filename, validation_oov_pred_filename)
        self.inference_file(test_true_filename, test_pred_filename)
        if os.path.exists(test_oov_true_filename):
            self.inference_file(test_oov_true_filename, test_oov_pred_filename)

        print('==================')
        print('validation result:')
        self.evaluation_from_file(validation_pred_filename,
                                  validation_true_filename,
                                  validation_oov_true_filename)
        print('=============')
        print('test result:')
        self.evaluation_from_file(test_pred_filename,
                                  test_true_filename,
                                  test_oov_true_filename)

    def evaluation_from_file(self, pred_filename, true_filename, oov_filename):
        pred_data = read_json(pred_filename)
        true_data = read_json(true_filename)
        if os.path.exists(oov_filename):
            oov_data = read_json(oov_filename)
        else:
            oov_data = None
        evaluate_result(pred_data, true_data, oov_data)

    def evaluation_from_object(self, pred_data, true_data):
        evaluate_result(pred_data, true_data)

    @staticmethod
    def get_name(filename, suffix):
        if suffix:
            return filename[:filename.rindex('.')] + suffix + filename[filename.rindex('.'):]
        else:
            return filename


if __name__ == '__main__':
    CRFExperiment('unigram', [UNIGRAM]).train().evaluation()
    # ret = CRFExperiment('unigram', [UNIGRAM]).inference_json(read_json(DATA_DIR+'validation.json'))
