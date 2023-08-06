# !/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import operator
import os
import pickle
import re
import string
import sys
from langdetect import detect_langs
from langdetect import DetectorFactory
import nltk
import tqdm
import spacy
import langdetect


def _is_anything(text):
    stripped = text.strip()
    letters = re.sub('[^a-zA-Z]+', '', stripped)
    return len(letters) > 1


def _is_probably_english(text):
    try:
        langs = detect_langs(text)
        lang_dict = {}
        for lang in langs:
            lang_dict[lang.lang] = lang.prob
        if 'en' not in lang_dict:
            return False
        most_likely_lang = max(lang_dict.iteritems(), key=operator.itemgetter(1))[0]
        if most_likely_lang == 'en':
            return True
        return abs(lang_dict['en'] - lang_dict[most_likely_lang]) < 0.1
    except langdetect.lang_detect_exception.LangDetectException:
        return False


def _should_normalise_text(text):
    if not _is_anything(text):
        return False
    if not _is_probably_english(text):
        return False
    return True


def _normalise_text(text, nlp):
    doc = nlp(text)
    replaced_text = []
    entity_text = text
    for entity in doc.ents:
        if not _is_anything(entity.text):
            continue
        new_text = '_'.join([entity.label_, entity.text.replace(' ', '_')])
        new_text = re.sub(r'[^\w\s]', ' ', new_text)
        entity_text = entity_text.replace(entity.text, new_text)
        replaced_text.append(new_text)
    tokenize = nltk.word_tokenize(entity_text)
    pos_tags = nltk.pos_tag(tokenize)
    pos_tokens = []
    for pos_tag in pos_tags:
        if not _is_anything(pos_tag[0]) or pos_tag[0] in replaced_text:
            pos_tokens.append(pos_tag[0])
            continue
        pos_tokens.append(u'{}_{}'.format(pos_tag[1], pos_tag[0]))
    lower_text = ' '.join(pos_tokens).lower()
    if lower_text[-1] != '\n':
        lower_text += '\n'
    return lower_text


def _run_normaliser(corpus_file, output_file):
    # Setup determinism
    DetectorFactory.seed = 0
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nlp = spacy.load('en_core_web_sm')
    # Read and write the normalised corpus
    with codecs.open(output_file, 'w', encoding='utf8') as output_handle:
        with codecs.open(corpus_file, 'r', encoding='utf8') as corpus_handle:
            for text in tqdm.tqdm(corpus_handle):
                if not _should_normalise_text(text):
                    continue
                normalised = _normalise_text(text, nlp)
                output_handle.write(normalised)


def _main():
    # Read arguments
    if len(sys.argv) != 3:
        print "textnormaliser [corpus-file] [output-file]"
        sys.exit(1)
    corpus_file = sys.argv[1]
    output_file = sys.argv[2]
    _run_normaliser(corpus_file, output_file)


if __name__ == "__main__":
    _main()
