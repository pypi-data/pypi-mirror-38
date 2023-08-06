
# Author: Hirotaka Niitsuma
# @2018 Hirotaka Niirtsuma
#
# You can use this code olny for self evaluation.
# Cannot use this code for commercial and academical use.
# pantent pending
#  https://patentscope2.wipo.int/search/ja/detail.jsf?docId=JP225380312
#  Japan patent office patent number 2017-007741

import sys

import math

import numpy as np

from scipy.sparse import csr_matrix,csc_matrix,dok_matrix,issparse,coo_matrix
import scipy.sparse

from sklearn import base
from sklearn import utils

from delayedsparse import delayedspmatrix,delayedspmatrix_t,isdelayedspmatrix
from delayedsparse import safe_sparse_dot as sdot

import extmath2

from . import ca


class MCA(ca.CA):
    def fit(self, X, y=None):

        # One-hot encode the data
        self.one_hot_ = one_hot.OneHotEncoder().fit(X)

        # Apply CA to the indicator matrix
        super().fit(self.one_hot_.transform(X))


        return self
