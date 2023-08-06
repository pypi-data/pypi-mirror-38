# -*- coding: utf-8 -*-
# Based https://pytorch.org/tutorials/beginner/nlp/advanced_tutorial.html
# Modified by InfinityFuture

import math
from tqdm import tqdm
from sklearn.base import BaseEstimator
import numpy as np
import sklearn_crfsuite

from skcrf_tagger.utils import extrat_entities
from skcrf_tagger.utils import sent2features

class Tagger(BaseEstimator):
    """scikit-learn compatible Tagger"""

    def __init__(
        self,
        algorithm='lbfgs',
        c1=0.,
        c2=1.,
        verbose=1,
        max_iterations=None,
        model=None,
        ):
        """init"""
        self.params = {
            'algorithm': algorithm, # lbfgs, l2sgd, ap, pa, arow
            'c1': c1,
            'c2': c2,
            'verbose': verbose,
            'max_iterations': max_iterations,
        }
        self.model = model

    def get_params(self, deep=True):
        """Get params for scikit-learn compatible"""
        params = self.params
        if deep:
            params['model'] = self.model
        return params

    def set_params(self, **parameters):
        """Set params for scikit-learn compatible"""
        for k, v in parameters.items():
            if k in self.params:
                self.params[k] = v
        return self

    def __getstate__(self):
        """Get state for pickle"""
        state = {
            'params': self.params,
            'model': self.model,
        }
        return state
    
    def __setstate__(self, state):
        """Get state for pickle"""
        self.params = state['params']
        if state['model'] is not None:
            self.model = state['model']
            if self.model is None:
                self.apply_params()
    
    def apply_params(self):
        """Apply params and build RNN-CRF model"""
        algorithm = self.params['algorithm']
        c1 = self.params['c1']
        c2 = self.params['c2']
        verbose = self.params['verbose']
        max_iterations = self.params['max_iterations']
        model = sklearn_crfsuite.CRF(
            algorithm=algorithm,
            c1=c1,
            c2=c2,
            max_iterations=max_iterations,
            all_possible_transitions=True,
            verbose=verbose,
        )
        self.model = model
    
    def fit(self, X, y):
        """Fit the model"""
        assert len(X) > 0, 'X must size > 0'
        assert len(y) > 0, 'y must size > 0'
        assert len(X) == len(y), 'X must size equal to y'
        X_train = [sent2features(s) for s in X]
        y_train = y
        self.apply_params()
        self.model.fit(X_train, y_train)

    def predict(self, X, batch_size=32, verbose=0):
        """Predict tags"""
        assert len(X) > 0, 'predict empty'
        model = self.model
        X_test = [sent2features(s) for s in X]
        return model.predict(X_test)

    def score(self, X, y, batch_size=None, verbose=0, detail=False): # pylint: disable=invalid-name,too-many-locals
        """Calculate NER F1
        Based CONLL 2003 standard
        """
        def _get_sets():
            preds = self.predict(X, verbose=verbose, batch_size=batch_size)
            pbar = enumerate(zip(preds, y))
            if verbose > 0:
                pbar = tqdm(pbar, ncols=0, total=len(y))

            apset = []
            arset = []
            for i, (pred, y_true) in pbar:
                pset = extrat_entities(pred)
                rset = extrat_entities(y_true)
                for item in pset:
                    apset.append(tuple(
                        [i] + list(item)
                    ))
                for item in rset:
                    arset.append(tuple(
                        [i] + list(item)
                    ))
            return apset, arset

        apset, arset = _get_sets()
        pset = set(apset)
        rset = set(arset)
        inter = pset.intersection(rset)
        precision = len(inter) / len(pset) if pset else 1
        recall = len(inter) / len(rset) if rset else 1
        f1score = 0 
        if precision + recall > 0:
            f1score = 2 * ((precision * recall) / (precision + recall))
        if detail:
            return precision, recall, f1score
        return f1score
