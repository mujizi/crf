# -*- coding: utf-8 -*-
import os
from modelhub.framework import ApiModel
from figure_en.utils.constant import EXP_CONFIG
from figure_en.crf_tagger import CRFTagger
from figure_en.post_process import post_process
from figure_en.en_get_parts_task.utils.tools import *

class Model(ApiModel):
    model_name = "figure_en"
    model_version = 1
    INPUTS_SAMPLE = {'text': 'accompanied with guide rails <b>56</b>, <b>57</b> and <b>666</b>. recording unit <b>24</b>,'}
    OUTPUTS_SAMPLE = {'result': []}

    def prepare(self):
        super().prepare()
        EXP_CONFIG['experiment'] = False
        model_path = os.path.join(self.model_path, 'variables/')
        self.tagger = CRFTagger('model', model_path, is_load_model=True)

    def is_ready(self):
        if not self.tagger or not self.tagger.model:
            raise Exception('model loading error.')
        return True

    def validate_input_data(self, raw_input):
        # do validation
        if not isinstance(raw_input, dict):
            raise Exception('input is not dict')
        if not raw_input.get('text'):
            raise Exception('key "text" is not in input data')
        if not isinstance(raw_input['text'], str):
            raise Exception('value of key "text" is not string.')
        return True

    def preprocess(self, raw_input):
        return raw_input['text']

    def run_model(self, preprocessed_data):
        return self.tagger.inference(preprocessed_data, rule_entity=True)

    def postprocess(self, result, raw_input, preprocessed_data):
        crf_ents, rule_ents = result
        final_crf_entities = post_process(crf_ents)
        final_rule_entities = voting(rule_ents)
        final_entities = merge_rule_crf(final_rule_entities, final_crf_entities)
        return final_entities


if __name__ == "__main__":
    model = Model()
    output = model.run(model.INPUTS_SAMPLE)
    print(output)
