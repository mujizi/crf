# -*- coding: UTF-8 -*-
"""
implement CRF training, inference.
"""
import joblib
from sklearn_crfsuite import CRF
from .crf_feature import CRFFeature
from .tokenizer import *
from .utils.utils import *
from .utils.io import read_json
# from .data_process.text_preprocess import *
from .pre_process import TextPreprocessor
from .utils.constant import *
from figure_en.data_process.label2entity import *
from figure_extractor_en.extractor import get_parts


class CRFTagger(object):
    def __init__(self,
                 model_name,
                 model_folder=MODEL_DIR,
                 label_schema=SEQ_BILOU,
                 is_load_model=False,
                 feature_sets=None):
        self.model_path = os.path.join(model_folder, model_name + '.jl')

        self.label_schema = label_schema
        if is_load_model:
            self.__load_model()
        self.tokenizer = EnglishTokenizer()
        self.feature_sets = feature_sets if feature_sets else []
        if self.feature_sets:
            if type(self.feature_sets) not in {list, tuple}:
                raise TypeError('feature sets must be list or tuple')
            CRFFeature.feature_sets = self.feature_sets
        self.preprocessor = TextPreprocessor()

    def __load_model(self):
        if not os.path.exists(self.model_path):
            raise Exception('model doesn\'t exist!! at {0}'.format(self.model_path))
        self.model = joblib.load(self.model_path)

    def train(self, src_filename, max_iter=200):
        sents = read_json(src_filename)
        labels = [sent['labels'] for sent in sents]
        features = []

        for sent in sents:
            sent_tokens = sent['tokens']
            feat = CRFFeature(sent_tokens).sent2feature()
            features.append(feat)
        crf = CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=max_iter,
            all_possible_transitions=True,
        )
        crf.fit(features, labels)
        joblib.dump(crf, self.model_path)

    def inference(self, text, is_check_entity=False, rule_entity=False):
        if not hasattr(self, 'model') or not self.model:
            self.__load_model()
        # preprocess text, normalize characters, remove spaces and keep offset mapping
        lines, index_mapper = self.preprocessor.process(text,
                                                        is_split_line=True,
                                                        is_normalize_text=False,
                                                        is_skip_empty_line=True,
                                                        is_remove_html_tag=True,
                                                        is_remove_space=False)
        # tokenize text, return tokens, pos tags and token offsets
        # self.tokens = self.tokenizer.tokenize_sentences([l['text'] for l in lines])
        crf_entities = []
        rule_entities = []
        for line in lines:
            if not line["text"].strip(): continue
            tokens, doc = self.tokenizer.tokenize_sentence(line["text"], with_doc=True)
            # do not run rule entity when debug
            if rule_entity:
                rule_ents = get_parts(line["text"], line["start"], ext_doc=doc)
                rule_entities.extend(rule_ents)
            if not tokens: continue
            sent_entities = self.inference_tokens(line['text'], tokens)
            for e in sent_entities:
                e['start'] += line['start']
                e['end'] += line['start']
            crf_entities.extend(sent_entities)

        if index_mapper:
            for entity in crf_entities:
                entity['start'] = index_mapper[entity['start']]
                entity['end'] = index_mapper[entity['end'] - 1] + 1
                entity['entity'] = text[entity['start']:entity['end']]
            for entity in rule_entities:
                entity['id_start'] = index_mapper[entity['id_start']]
                entity['id_end'] = index_mapper[entity['id_end'] - 1] + 1
                entity['name_start'] = index_mapper[entity['name_start']]
                entity['name_end'] = index_mapper[entity['name_end'] - 1] + 1
        if is_check_entity:
            check_entities(crf_entities, text)
            check_entities(crf_entities, rule_entities)
        return crf_entities, rule_entities

    def inference_sentence(self, sentence):
        if not hasattr(self, 'model') or not self.model:
            self.__load_model()
        tokens, pos_tags = self.tokenizer.tokenize_sentence(sentence)
        entities = self.inference_tokens(tokens, pos_tags)
        return entities

    def inference_tokens(self, text, tokens, return_labels=False):
        if not hasattr(self, 'model') or not self.model:
            self.__load_model()
        features = CRFFeature(tokens).sent2feature()
        pred_labels = self.model.predict_single(features)

        if return_labels:
            return pred_labels
        else:
            return label2entity(text, tokens, pred_labels, self.label_schema)

    def get_weights(self, tokens):
        features = CRFFeature(tokens)
