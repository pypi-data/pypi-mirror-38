# -*- coding: utf-8 -*-
from .timeseries import multiple_regression
from .timeseries import fast_DTW
from .timeseries import pearsonr_correlation

__all__ = ['multiple_regression',
           'fast_DTW',
           'pearsonr_correlation']