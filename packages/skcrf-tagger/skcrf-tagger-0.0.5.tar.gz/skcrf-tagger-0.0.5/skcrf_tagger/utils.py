# -*- coding: utf-8 -*-
# From https://pytorch.org/tutorials/beginner/nlp/advanced_tutorial.html
# Modified by InfinityFuture

from collections import Counter
import numpy as np

def default_spliter(x) -> list:
    """Default sentence spliter"""
    return x.split()

def text_reader(path, spliter=default_spliter):
    """Read a text file, and return data
    data should follow this format:
    I want to New York
    O O O CityB CityI
    """
    with open(path, 'r') as fp:
        lines = []
        for l in fp:
            l = l.strip()
            if len(l):
                lines.append(l)
    assert len(lines) > 0, 'text file empty "{}"'.format(path)
    assert len(lines) % 2 == 0, 'text file should have even lines "{}"'.format(path)
    x_data = []
    y_data = []
    for i, l in enumerate(lines):
        if i % 2 == 1:
            line = lines[i - 1]
            tag = l
            line = spliter(line)
            tag = spliter(tag)
            x_data.append(line)
            y_data.append(tag)
            assert len(line) == len(tag), 'line "{}" and "{}" do not match'.format(i - 1, i)
    return x_data, y_data

def word2features(sent, i):
    word = sent[i]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }
    if i > 0:
        word1 = sent[i-1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1/0:word.lower()': sent[i-1].lower() + '|' + sent[i].lower()
        })
    else:
        features['BOS'] = True
    if i > 1:
        word2 = sent[i-2]
        features.update({
            '-2:word.lower()': word2.lower(),
            '-2:word.istitle()': word2.istitle(),
            '-2:word.isupper()': word2.isupper(),
            '-2/-1:word.lower()': sent[i-2].lower() + '|' + sent[i-1].lower(),
        })
    else:
        features['BBOS'] = True
    if i < len(sent)-1:
        word1 = sent[i+1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '0/+1:word.lower()': sent[i].lower() + '|' + sent[i+1].lower(),
        })
    else:
        features['EOS'] = True
    if i < len(sent)-2:
        word2 = sent[i+2]
        features.update({
            '+2:word.lower()': word2.lower(),
            '+2:word.istitle()': word2.istitle(),
            '+2:word.isupper()': word2.isupper(),
            '+1/+2:word.lower()': sent[i+1].lower() + '|' + sent[i+2].lower(),
        })
    else:
        features['EEOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def extrat_entities(seq: list) -> list:
    """Extract entities from a sequences

    ---
    input: ['B', 'I', 'I', 'O', 'B', 'I']
    output: [(0, 3, ''), (4, 6, '')]
    ---
    input: ['B-loc', 'I-loc', 'I-loc', 'O', 'B-per', 'I-per']
    output: [(0, 3, '-loc'), (4, 6, '-per')]
    """
    ret = []
    start_ind, start_type = -1, None
    for i, tag in enumerate(seq):
        if tag.startswith('S'):
            ret.append((i, i + 1, tag[1:]))
            start_ind, start_type = -1, None
        if tag.startswith('B') or tag.startswith('O'):
            if start_ind >= 0:
                ret.append((start_ind, i, start_type))
                start_ind, start_type = -1, None
        if tag.startswith('B'):
            start_ind = i
            start_type = tag[1:]
    if start_ind >= 0:
        ret.append((start_ind, len(seq), start_type))
        start_ind, start_type = -1, None
    return ret
