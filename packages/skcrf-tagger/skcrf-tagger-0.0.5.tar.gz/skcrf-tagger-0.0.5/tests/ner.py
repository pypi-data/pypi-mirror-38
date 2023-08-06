# -*- coding: utf-8 -*-

import os
import pickle

from skcrf_tagger import Tagger
from skcrf_tagger.utils import text_reader


def test_ner():
    x_data, y_data = text_reader('/tmp/train.txt')
    tag = Tagger()
    tag.fit(x_data, y_data)

    with open('/tmp/test_ner_skcrf.pkl', 'wb') as fp:
        pickle.dump(tag, fp)

    tag = None
    tag = pickle.load(open('/tmp/test_ner_skcrf.pkl', 'rb'))

    acc, rec, f1s = tag.score(x_data, y_data, detail=True, verbose=1)
    print('train precision: {}, recall: {}, f1: {}'.format(acc, rec, f1s))

    x_data, y_data = text_reader('/tmp/test.txt')
    tag = pickle.load(open('/tmp/test_ner_skcrf.pkl', 'rb'))

    acc, rec, f1s = tag.score(x_data, y_data, detail=True, verbose=1)
    print('test precision: {}, recall: {}, f1: {}'.format(acc, rec, f1s))

if __name__ == '__main__':
    test_ner()
