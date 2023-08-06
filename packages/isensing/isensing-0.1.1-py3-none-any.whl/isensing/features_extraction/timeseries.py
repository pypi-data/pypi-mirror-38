# -*- coding: utf-8 -*-
"""
"""

from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from scipy.stats.stats import pearsonr
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def __remove_na(x):
    
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    
    if x.isnull().values.any():
        x = x.interpolate().dropna()
        
    return x
    

def multiple_regression(X, y, ret_intercept=True):
    """
    Performs linear/mulitple regression on time series data and calculate their
    coefficients and intercept for features extraction.
    
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Data, where n_samples is the number of samples and n_features is the number
        of features.
        
    y : array-like, shape (n_samples) or (n_samples, n_outputs)
        True values for X.
        
    ret_intercept : boolean, optional (default True)
        If True, return intercept value of the regression.  
        
    Returns
    -------
    coef : array-like, shape (n_features,) or (n_features+1,) if ret_intercept = True
        Returns estimated coefficients for the linear regression. If ret_intercept
        is set to True, returns the intercept of the linear regression.
    """
    
    linear_regression = LinearRegression()
    linear_regression.fit(X, y)
    
    coef = linear_regression.coef_
    if ret_intercept:
        return np.append(coef, linear_regression.intercept_)
    return coef

def fast_DTW(x, y, distance=None):
    """
    Performs Dynamic Time Warping (DTW) to calculate the distance between two 
    time series data.
    
    Parameters
    ----------
    x : array-like time series data
        Time series input 1.
        
    y : array-like time series data
        Time series input 2.
        
    distance : function or int (default None)
        Method for calculating the distance between x and y.
        
        1) If distance is an int of value p > 0,
            then the p-norm will be used.
        
        2) If distance is a function,
            then distance() will be used.
            
        3) If distance is None,
            then abs(x[i] - y[j]) will be used.
            
    Returns
    -------
    dist : float
        The estimated distance between the two time series.
    """
    
    x = __remove_na(x)
    y = __remove_na(y)
    
    dist, _ = fastdtw(x, y, dist=distance)
    
    return dist

def pearsonr_correlation(x, y):
    """
    Calculates Pearsonr Correlation between two time series. Both time series
    have to the same length. 
        
    Parameters
    ----------
    x : array-like time series data
        Time series input 1.
        
    y : array-like time series data
        Time series input 2.
            
    Returns
    -------
    cor : float
        The correlation value between two time series.
    """
    
    x = __remove_na(x)
    y = __remove_na(y)
    
    if x.size == y.size:
        cor_coef, p = pearsonr(x, y)
    else:
        if x.size < y.size:
            sel_index = x.index
        else:
            sel_index = y.index
        cor_coef, p = pearsonr(x[sel_index], y[sel_index])
        
    return cor_coef