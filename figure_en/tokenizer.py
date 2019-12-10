import spacy
from figure_en.utils.singleton import *
from spacy.tokenizer import Tokenizer as TK
import re
import en_core_web_sm

CUT_TOKEN_PATTERN = re.compile(r"(\s|,|\(|\)|\.|\]|\[)")
prefix_re = re.compile(r'^(\s|\(|\[)')
suffix_re = re.compile(r'(\s|,|\.|\)|;|\]|:|\?|\!|\]|\[)$')
infix_re = re.compile(r'\[|\]|\"|\)|\(|\,')
simple = re.compile(r'\@')


class Tokenizer(object):
    def __init__(self):
        """
        initialize tokenizer model
        """
        pass

    def tokenize(self, text, pos_tagging=True):
        """
        main logic of tokenizer, tokenize text which contains line break
        :param text: text to be tokenized
        :param pos_tagging: whether return pos tags
        :return:
        """
        pass

    def tokenize_sentences(self, sentences, pos_tagging=True):
        """
        tokenize sentences
        :param sentences: sentences text list
        :param pos_tagging:
        :return:
        """
        return [self.tokenize_sentence(sent, pos_tagging) for sent in sentences]

    def tokenize_sentence(self, sentence, pos_tagging=True):
        """
        tokenize sentence (without line break character)
        :param sentence:
        :param pos_tagging:
        :return: tokenized text
        """
        token_texts = sentence.split(' ')
        tokens = []
        offset = 0
        for token_text in token_texts:
            token = {'text': token_text, 'start': offset, 'end': offset + len(token_text)}
            if pos_tagging:
                token['pos_tag'] = 'x'
            tokens.append(token)
            offset += len(token_text)
        return tokens

    def regx_tokenize_sentence(self, sentence):
        token_texts = CUT_TOKEN_PATTERN.split(sentence)
        tokens = []
        offset = 0
        for token_text in token_texts:
            if token_text != '' and token_text != ' ':
                token = {'text': token_text, 'start': offset, 'end': offset + len(token_text)}
                tokens.append(token)
                offset += len(token_text)
            elif token_text == ' ':
                offset += len(token_text)

        return tokens


class SingletonSpacy(metaclass=SingletonType):
    # NLP = spacy.load('en', disbale=['ner', 'parser', 'textcat'])
    NLP = en_core_web_sm.load()

    def __call__(self, *args, **kwargs):
        return self.NLP


def custom_tokenizer(n):
    return TK(n.vocab,
              rules={},                             # this is a necessary args in spacy 1.10, optional args in spacy 2.x
              prefix_search=prefix_re.search,
              suffix_search=suffix_re.search,
              infix_finditer=infix_re.finditer)


nlp = SingletonSpacy()()
nlp.tokenizer = custom_tokenizer(nlp)


class EnglishTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()

    def tokenize(self, text, pos_tagging=True):
        return self.tokenize_sentence(text, pos_tagging)

    def tokenize_sentences(self, sentences, pos_tagging=True):
        sent_tokens = []
        for sentence in sentences:
            sent_tokens.append(self.tokenize_sentence(sentence, pos_tagging))
        return sent_tokens

    def parse_doc(self, doc, pos_tag=True):
        tokens = []
        for token in doc:
            dic = {'text': token.text,
                   'start': token.idx,
                   'end': token.idx + len(token)}

            if pos_tag:
                dic['pos_tag'] = token.tag_
            tokens.append(dic)
        return tokens

    def tokenize_sentence(self, sentence, pos_tag=True, with_doc=False):
        doc = nlp(sentence)
        tokens = self.parse_doc(doc, pos_tag=pos_tag)
        if with_doc: return tokens, doc
        return tokens


        # tokens = []
        # for token in nlp(sentence):
        #     new_token = {'text': token.text, 'start': token.idx,
        #                  'end': token.idx + len(token.text)}
        #     if pos_tag:
        #         new_token['pos_tag'] = token.tag_
        #     tokens.append(new_token)








    # def tokenize_sentence(self, sentence, pos_tagging=True):
    #     def custom_tokenizer(nlp):
    #         return TK(nlp.vocab, prefix_search=prefix_re.search, suffix_search=suffix_re.search, infix_finditer=infix_re.finditer)
    #
    #     nlp.tokenizer = custom_tokenizer(nlp)
    #     tokens = []
    #     for token in nlp(sentence):
    #         dic = {'text': token.text,
    #                'start': token.idx,
    #                'end': token.idx + len(token)}
    #         if pos_tagging:
    #             dic['pos_tag'] = token.tag_
    #         tokens.append(dic)
    #     return tokens


Tokenizer = EnglishTokenizer


if __name__ == '__main__':
    s ='the [ratio] 11 what<b> versus 15 an,gle.15,16, 17, 20. and 666 ?'
    kk = EnglishTokenizer()
    # o = kk.regx_tokenize_sentence(s)
    r = kk.tokenize_sentence(s)
    # print(o)
    print(r)
    print([i['text'] for i in r])


# # -*- coding: UTF-8 -*-
# """encapsulate Tokenizer interface"""
# from itertools import accumulate
# from spacy.tokenizer import Tokenizer
# import re
#
#
# prefix_re = re.compile(r'(\s|\(|\[)')
# suffix_re = re.compile(r'(\s|,|\.|\)|;|\]|:|\?|\!)')
#
#
# class Tokenizer(object):
#     def __init__(self):
#         """
#         initialize tokenizer model
#         """
#         pass
#
#     def tokenize(self, text, pos_tagging=True):
#         """
#         main logic of tokenizer, tokenize text which contains line break
#         :param text: text to be tokenized
#         :param pos_tagging: whether return pos tags
#         :return:
#         """
#         pass
#
#     def tokenize_sentences(self, sentences, pos_tagging=True):
#         """
#         tokenize sentences
#         :param sentences: sentences text list
#         :param pos_tagging:
#         :return:
#         """
#         return [self.tokenize_sentence(sent, pos_tagging) for sent in sentences]
#
#     def tokenize_sentence(self, sentence, pos_tagging=True):
#         """
#         tokenize sentence (without line break character)
#         :param sentence:
#         :param pos_tagging:
#         :return: tokenized text
#         """
#         token_texts = sentence.split(' ')
#         tokens = []
#         offset = 0
#         for token_text in token_texts:
#             token = {'text': token_text, 'start': offset, 'end': offset + len(token_text)}
#             if pos_tagging:
#                 token['pos_tag'] = 'x'
#             tokens.append(token)
#             offset += len(token_text)
#         return tokens
#
#
# import spacy
# from .utils.singleton import *
#
#
# class SingletonSpacy(metaclass=SingletonType):
#     NLP = spacy.load('en', disbale=['ner', 'parser', 'textcat'])
#
#     def __call__(self, *args, **kwargs):
#         return self.NLP
#
#
# nlp = SingletonSpacy()()
#
#
# class EnglishTokenizer(Tokenizer):
#     def __init__(self):
#         super().__init__()
#
#     def tokenize(self, text, pos_tagging=True):
#         return self.tokenize_sentence(text, pos_tagging)
#
#     def tokenize_sentences(self, sentences, pos_tagging=True):
#         sent_tokens = []
#         for sentence in sentences:
#             sent_tokens.append(self.tokenize_sentence(sentence, pos_tagging))
#         return sent_tokens
#
#     def tokenize_sentence(self, sentence, pos_tagging=True):
#         tokens = []
#         for token in nlp(sentence):
#             new_token = {'text': token.text, 'start': token.idx,
#                          'end': token.idx + len(token.text)}
#             if pos_tagging:
#                 new_token['pos_tag'] = token.tag_
#             tokens.append(new_token)
#         return tokens
#
#     def custom_tokenize_sentence(self, sentence, pos_tag=None):
#         def custom_tokenizer(nlp):
#             return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
#                              suffix_search=suffix_re.search, )
#
#         self.NLP.tokenizer = custom_tokenizer(self.NLP)
#         tokens = []
#         for token in self.NLP(sentence):
#             dic = {'text': token,
#                    'start': token.idx,
#                    'end': token.idx + len(token)}
#
#             if pos_tag:
#                 dic['pos_tag'] = token.tag_
#             tokens.append(dic)
#             print(token)
#
#         return tokens
#
#
# Tokenizer = EnglishTokenizer
