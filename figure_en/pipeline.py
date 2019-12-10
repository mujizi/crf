# -*- coding: UTF-8 -*-
from figure_en.utils.constant import *
from figure_en.post_process import post_process
from figure_en.crf_tagger import CRFTagger


def pipeline(text, model_name, model_dir, print_result=True):
    """
    NER model pipeline interface
    :param text: input text
    :param model_name: model name
    :param model_dir: model directory
    :return: extracted entities
    """
    tagger = CRFTagger(model_name, model_dir)
    entities = tagger.inference(text)
    final_entities = post_process(text, entities)
    if print_result:
        print(final_entities)
    return final_entities


if __name__ == '__main__':
    pipeline('example_text', 'unigram', MODEL_DIR)
