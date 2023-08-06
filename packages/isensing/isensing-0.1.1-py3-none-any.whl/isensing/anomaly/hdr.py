# -*- coding: utf-8 -*-
"""
This module contains the High-Density Regions (HDR) class-object which computes
representation of a kernel-density estimate using Gaussian kernels to detect
outliers in sparse regions.

Libraries used:
    numpy
    scipy.stats
    matplotlib
    
"""

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

class HDR:
    """Perform outlier detections using High-Density Regions (HDR) from a given
    set of 2-dimensional data points.
    
    HDR - Compute High-Density Regions from the representation of a kernel-density
    estimate using Gaussian kernels where outliers are detected in the sparse regions. 
    Kernel density estimation is a way to estimate the probability density function 
    (PDF) of a random variable in a non-parametric way.
    
    Parameters
    ----------
    n : int, optional
        The number of outliers to be identify
        
    Attributes
    ----------
    X : array, shape = (n_samples, 2)
        Input data X
                
    outliers : arrary, shape = (n, 2)
        The list of n outliers with its x,y coordinates.
        
    outliers_scores : array, shape = (n, 1)
        The distances metric associated with the identified outliers and the
        alpha-shape.
                   
    """
    
    def __init__(self, n=10):
        self.n = n
        pass
    
    def __plot_outliers(self):
        plt.scatter(self.X[:, 0], self.X[:, 1], marker='.', c='blue')
        plt.scatter(self.outliers[:, 0], self.outliers[:, 1], marker='x', c='red')
        plt.title("High Density Regions")
        plt.show()      
        
    def fit(self, X, plot_outliers=False):
        """Perform outlier detections using HDR from the 2-dimensional data points.

        Parameters
        ----------
        X : array of shape (n_samples, 2)
            A feature array or 2D array of samples.

        plot_outliers : boolean
            True if plotting of the outliers is required.
            
        Returns
        -------
        outliers : ndarray, shape (n_samples, 2)
            A n_samples of outliers.  

        """
        assert X.ndim == 2, "Input data must be 2-dimensional data."
        assert X.shape[1] == 2, "Input data must be 2-dimensional data."
        
        self.X = X
        
        kernel = stats.gaussian_kde(X.T)
        scores = kernel(X.T)
        outliers = np.concatenate((X, np.expand_dims(scores, axis=1)), axis=1)
        outliers = outliers[outliers[:, 2].argsort()[:self.n]]
        self.outliers = outliers[:, 0:2]
        self.outliers_scores = outliers[:, -1]
        
        if plot_outliers:
            self.__plot_outliers()
        return self.outliers