# -*- coding: utf-8 -*-
"""
This module contains the functions to perform outliers and anomalies detections
based on algorithms such as Isolation Forest, alpha-hull and high-density regions.

The functions are:

    outlier_detection() :
        A function that uses either AlphaHull or High-Density Regions (HDR) algorithms 
        to detect outliers. Decomposition using Principal Component Analysis (PCA) or 
        Robust PCA is performed on the input data before the running outliers-detection
        algorithm.
    
    isensing_anomalies() :
        A function that uses all three algorithms: Isolation Forest, AlphaHull and HDR
        to detect anomalies in the data. This function is able to plot the results in 
        the two dimensional space leveraging on "plotly" package. This function is also
        able to identify features or columns that causes the data point to be an anomaly. 
        
"""

from .alphahull import AlphaHull
from .hdr import HDR
from isensing.decomposition import RobustPCA
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go

def __normalize(X, center=True, scale=True):
    if center: X = X - np.mean(X, axis=0)
    if scale: X = X / np.std(X, axis=0, ddof=1)
    return X

def outlier_detection(X, num_outliers=20, method='alpha', alpha=2, plot=False,
                      normalize=True, center=True, scale=True, 
                      robust=True, robust_tol=1e-8, robust_max_step=200,
                      ret_errors=False, ret_prin_comp=False):
    """
    Performs outlier detection using AlphaHull or HDR from a given set data points.
    
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Data, where n_samples is the number of samples and n_features is the number
        of features.
        
    num_outliers : int, optional (default 20)
        The number of outliers to be identify.
        
    method : string {'alpha', 'hdr'} (default 'alpha')
        alpha : 
            Apply alpha-hull algorithm to detect outliers. 
        hdr :
            Apply high-density regions algorithm to detect outliers.
            
    alpha : float, optional (default 2)
         The alpha value that controls the level of details or how tightly the
         boundary fits around the 2-dimensional data points.
         Only in use if method = 'alpha'.
            
    plot : boolean, optional (default False)
        If True, plot the results of the outliers identify in 2-dimensional space.
        
    normalize : boolean, optional (default True)
        If True, perform normalization on the input data.
        
    center : boolean, optional (default True)
        If True, center the data before scaling.
        
    scale : boolean, optional (default True)
        If True, scale the data to unit variance with Delta Degrees of Freedom (DDOF) of 1.
        
    robust : boolean, optional (default True)
        If True, perform decomposition using RobustPCA instead of PCA
        
    robust_tol : float, optional (default 1e-8)
        Tolerance value that is used internally for checking convergence.
      
    robust_max_step : int, optional (default 200)
        The maximum number of iterations to compute the principal components.

    ret_errors : boolean, optional (default False)
        If True, return the reconstructed errors, difference between original data and
        reconstructed matrix data using PCA/RobustPCA principle components.
        
    ret_prin_comp : boolean, optional (default False)
        If True, return the PCA/RobustPCA principle components
    
    Returns
    -------
    results : dict {outliers, ^errors, ^prin_comp}
    
        outliers : list (num_outliers)
            A list of outliers identified by their labels if input data is pandas Dataframe
            else by their index.
                    
        errors : array-like, shape (n_samples, n_features)
            A matrix of reconstructed errors, calculated from the difference between original
            data and reconstructed matrix data using PCA/RobustPCA principle components.
            ^ Return only if ret_errors is True.
            
        prin_comp : components, shape (n_samples, 2)
            2-Dimensional PCA/RobustPCA principle components.
            ^ Return only if ret_prin_comp is True
        
    """
    results = dict()
    
    # check if method argument is correct
    methods = {'alpha', 'hdr'}
    if method not in methods:
        raise ValueError("Method must be one of %r." % methods)
    
    #check if input is Pandas Dataframe instance
    find_df_index = False
    if isinstance(X, pd.DataFrame):
        df_index = list(X.index)
        X = X.values
        find_df_index = True
    
    # normalize the input data    
    if normalize:
        X = __normalize(X, center, scale)
        
    # decompose input data into 2 dimensions data using robustPCA or PCA
    if robust:
        pca= RobustPCA(tol=robust_tol, max_step=robust_max_step, n_components=2)
    else:
        pca = PCA(n_components=2)
    y = pca.fit_transform(X)

    # run Alpha-hull or HDR algorithm    
    if method == 'alpha':
        alh = AlphaHull(n=num_outliers, alpha=alpha)
        outliers = alh.fit(y, plot_outliers=plot)
    else:
        hdr = HDR(n=num_outliers)
        outliers = hdr.fit(y, plot_outliers=plot)
        
    out_index = [np.where(y==o)[0][0] for o in outliers]
    if find_df_index:
        out_index = [df_index[i] for i in out_index]
        
    results['outliers'] = out_index
        
    if ret_errors:
        prin_comp = pca.components_
        X_ = np.matmul(y, prin_comp)
        # calculate PCA reconstruction errors
        errors = np.abs(X - X_)
        results['errors'] = errors
    
    if ret_prin_comp:
        results['prin_comp'] = y
        
    return results

def isensing_anomalies(X, num_outliers=20, ret_errors=False,
                       normalize=True, center=True, scale=True, alpha=2,
                       robust=True, robust_tol=1e-8, robust_max_step=200,
                       isf_n_estimators=200, isf_seed=1,
                       plot=False, ipynb=False, plot_filename=None):
    
    """
    Using 3 algorithms; Isolation Forest, AlphaHull and High-density Regions (HDR)
    to detect anomalies and plot the results using the plotly package in a 2-dimensional
    scatter plots. This function also helps to identify which features or columns is
    causing the data point to be an anomaly.
    
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Data, where n_samples is the number of samples and n_features is the number
        of features.
        
    num_outliers : int, optional (default 20)
        The number of outliers to be identify.
        
    ret_errors : boolean, optional (default False)
        If True, return the reconstructed errors, difference between original data and
        reconstructed matrix data using PCA/RobustPCA principle components.
                    
    normalize : boolean, optional (default True)
        If True, perform normalization on the input data.
        
    center : boolean, optional (default True)
        If True, center the data before scaling.
        
    scale : boolean, optional (default True)
        If True, scale the data to unit variance with Delta Degrees of Freedom (DDOF) of 1.
        
    alpha : float, optional (default 2)
         The alpha value that controls the level of details or how tightly the
         boundary fits around the 2-dimensional data points using AlphaHull algorithm.
        
    robust : boolean, optional (default True)
        If True, perform decomposition using RobustPCA instead of PCA
        
    robust_tol : float, optional (default 1e-8)
        Tolerance value that is used internally for checking convergence.
      
    robust_max_step : int, optional (default 200)
        The maximum number of iterations to compute the principal components.
        
    isf_n_estimators : int, optional (default 200)
        The number of base estimators in the ensemble.
        
    isf_seed : int, optional (default 1)
        Random seed for Isolation Forest algorithm.
        
    plot : boolean, optional (default False)
        If True, plot the all outliers results in a scatter plot using plotly package.
        
    ipynb : boolean, optional (default False)
        If True, plot the results in iPython notebook.
    
    plot_filename : str, optional
        File name of the plot.
            
    Returns
    -------
    results : dict {outliers, ^errors}
    
        outliers : list (num_outliers)
            A list of outliers identified by all three algorithms. The results are their labels 
            if input data X is DataFrame from Pandas package otherwise will be their array index.
        
        errors : Dataframe, shape (n_samples, n_features)
            Dataframe of reconstructed errors, calculated from the difference between original
            data and reconstructed matrix data using PCA/RobustPCA principle components.
            ^ Return only if ret_errors is True.
            
    """
    
    results = dict()
    
    #check if input is Pandas Dataframe instance
    find_df_index = False
    if isinstance(X, pd.DataFrame):
        df_index = list(X.index)
        df_cols = list(X.columns)
        X = X.values
        find_df_index = True
    else:
        df_index = list(range(X.shape[0]))
        df_cols = list()
        for i in range(X.shape[1]):
            df_cols.append("col_"+str(i+1))
        
    # run Isolation Forest algorithm
    rng = np.random.RandomState(isf_seed)
    isf = IsolationForest(n_estimators=isf_n_estimators, random_state=rng)
    isf.fit(X)
    isf_scores = isf.decision_function(X)
    isf_outliers = isf.predict(X)
    
    isf_df = pd.DataFrame({'isf_outliers':isf_outliers}, index=df_index)
    isf_outliers = list(isf_df[isf_df['isf_outliers']==-1].index)
    
    # run Alpha-Hull algorithm
    alh_results = outlier_detection(X, num_outliers, method='alpha',
                      normalize=normalize, center=center, scale=scale, 
                      robust=robust, robust_tol=robust_tol, robust_max_step=robust_max_step,
                      ret_errors=True, ret_prin_comp=True)
    
    hdr_results = outlier_detection(X, num_outliers, method='hdr',
                      normalize=normalize, center=center, scale=scale, 
                      robust=robust, robust_tol=robust_tol, robust_max_step=robust_max_step)
    
    prin_comp = alh_results['prin_comp']
    errors = alh_results['errors']
    alh_outliers = alh_results['outliers']
    hdr_outliers = hdr_results['outliers']

    alh_pc2 = np.array([prin_comp[i] for i in alh_outliers])
    hdr_pc2 = np.array([prin_comp[i] for i in hdr_outliers])
    
    if find_df_index:
        alh_outliers = [df_index[i] for i in alh_outliers]
        hdr_outliers = [df_index[i] for i in hdr_outliers]
        
    union_outliers = list(set(alh_outliers).union(hdr_outliers))
    errors_df = pd.DataFrame(errors, columns=df_cols, index=df_index)
    
    if plot:
        
        hover_list = list()
        for i in range(len(df_index)):
            hover_text = "%s : %.4f" % (df_index[i], isf_scores[i])
            if df_index[i] in union_outliers:
                error_row = errors_df.loc[df_index[i]].sort_values(ascending=False)[:3]
                for i, v in zip(error_row.index, error_row.values):
                    hover_text += " | %s : %.4f" % (i, v)
            hover_list.append(hover_text)
        
        trace_pca = go.Scatter(
            x=prin_comp[:, 0],
            y=prin_comp[:, 1],
            mode='markers',
            name='Isolation Forest',
            hoverinfo='text',
            text=hover_list,
            marker=dict(
                size=6,
                color=isf_scores,
                colorscale='Portland', 
                colorbar=dict(
                    title='isf-scores',
                    lenmode='fraction',
                    len=0.70
                )
            )
        )
                    
        trace_alh = go.Scatter(
            x=alh_pc2[:, 0],
            y=alh_pc2[:, 1],
            mode='markers',
            name='AlphaHull',
            hoverinfo='none',
            marker=dict(
                color='red',
                symbol='circle-open', 
                size=10
            )
        )
                
        trace_hdr = go.Scatter(
            x=hdr_pc2[:, 0],
            y=hdr_pc2[:, 1],
            mode='markers',
            name='HDR',
            hoverinfo='none',
            marker=dict(
                color='blue',
                symbol='x-open', 
                size=11
            )
        )
        
        trace_list = [trace_pca, trace_alh, trace_hdr]
        
        if not plot_filename:
            plot_filename = "isensing_anomalies"
            
        if ipynb:
            plotly.offline.init_notebook_mode()
            plotly.offline.iplot({
                'data': trace_list,
                'layout': go.Layout(title="Isensing Anomalies")})
        else:
            plotly.offline.plot({
                'data': trace_list,
                'layout': go.Layout(title="Isensing Anomalies")}, 
                filename=plot_filename+".html")
    
    intersect_outliers = list(set(alh_outliers).intersection(hdr_outliers))
    print("Isolation Forest:\n%s\n" % (isf_outliers))
    print("AlphaHull:\n%s\n" % (alh_outliers))
    print("High Density Regions:\n%s\n" % (hdr_outliers))
#    print("Intersect:\n%s\n" % (intersect_outliers))
    
    results['outliers'] = list(set(intersect_outliers).intersection(isf_outliers))
    print("All 3:\n%s\n" % (results['outliers']))
    
    if ret_errors:
        results['errors'] = errors_df
    
    return results

