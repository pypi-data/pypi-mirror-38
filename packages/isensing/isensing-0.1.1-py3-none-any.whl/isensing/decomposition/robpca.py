# -*- coding: utf-8 -*-
"""
This module contains the RobustPCA class-object which does the computation of
the robust principal components analysis using the algorithm of Croux and 
Ruiz-Gazen (JMVA, 2005). A Fast Algorithm for Robust Principal Components based
on Projection Pursuit

Libraries used:
    numpy
    statsmodels
    
References:
    https://feb.kuleuven.be/public/u0017833/Programs/pca/robpca.txt
    
"""

import numpy as np
from statsmodels import robust
import pandas as pd

class RobustPCA:
    """Performs RobustPCA and computes a desired number of robust principal 
    components using the algorithm of Croux and Ruiz-Gazen (JMVA, 2005).
    
    Parameters
    ----------
    tol : float, optional (default 1e-8)
        Tolerance value that is used internally for checking convergence.
        
    max_steps : int, optional (default 200)
        The maximum number of iterations to compute the principal components.
    
    n_components : int, optional (default 2)
        The number of principal components to be computed.
         
    Attributes
    ----------
    X : array, shape = (n_samples, n_features)
        Input data X.
        
    components_ : array, shape = (n_samples, n_components)
        Principal components computed from the robustPCA algorithms. 
        
        
    """    
    def __init__(self, tol=1e-8, max_step=200, n_components=2):
        
        self.tol = tol
        self.max_step = max_step
        self.n_components = n_components
        
    def __r_mad(self, Z):
        return robust.mad(Z)
    
    @staticmethod
    def norme(x):
        return np.linalg.norm(x, axis=1, keepdims=True)
    
    def __mrobj(self, m):
        X = self.X
        t1 = np.matlib.repmat(m, X.shape[0], 1)
        t2 = X - t1
        xm = self.norme(t2)
        t1 = np.sum(xm, axis=0)
        s = t1.T
        return s
    
    def __L1_Median(self):
        
        X = self.X        
        n, p = X.shape
        
        m = np.median(X, axis=0)
        k = 1
    
        while (k <= self.max_step):
            
            mold = m
            t1 = np.matlib.repmat(m, n, 1)
            t2 = X-t1
            t3 = self.norme(t2)
            t4 = np.concatenate((t3, X), axis=1)
            Xext = t4[t4[:, 0].argsort()]
            dx = Xext[:, [0]]
            X = Xext[:, 1:]
            
            if (np.all(dx)):
                w = 1 / dx
            else:
                # untested
                ww = dx(np.all(dx, axis=1))
                w = 1 / ww
                t1 = np.zeros((len(dx) - len(w), 1))
                w = np.concat((t1, w))
            
            t1 = np.matlib.repmat(m, n, 1)
            t2 = X - t1
            t3 = np.matlib.repmat(w, 1, p)
            t4 = t2 * t3
            t5 = np.sum(t4, axis=0, keepdims=True)
            t6 = np.sum(w)
            delta = t5 / t6
            nd = np.linalg.norm(delta)
            
            if (np.all(nd < self.tol)):
                # untested
                maxhalf = 0
            else:
                maxhalf = np.log2(nd / self.tol)
            
            m = mold+delta
            nstep = 0
            
            while (np.all(self.__mrobj(m) >= self.__mrobj(mold) and nstep <= maxhalf)):
                # untested
                nstep += 1
                m = mold + delta / np.power(2, nstep)
            
            if (nstep > maxhalf):
                mX = mold #check with CH
                break
            
            k += 1
            
        if (k > self.max_step):
            print('Iteration failed')
        return m
    
    def fit_transform(self, X):
        """Fit the model with X and apply robustPCA reduction on X.

        Parameters
        ----------
        X : array, shape = (n_samples, n_features)
            Input data X.
            
        Returns
        -------
        X_new : array-like, shape (n_samples, n_components)

        """
        # convert pandas Dataframe into numpy array
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        self.X = X
        n, p = X.shape
    
        if (self.n_components > np.min([n, p])):
            raise AssertionError('pp too large')
    
        if (p > n):
            v, d, u = np.linalg.svd(X.t)
            X = np.matmul(u, d)
            pold = p
            p = n
        else:
            pold = p
    
        m = self.__L1_Median()
        
        y = X - np.matlib.repmat(m, n, 1)
        
        X_new = np.zeros((n, self.n_components))
    
        veig = []
        Lambda = []
    
        for k in range(self.n_components):
            if (k < p):
                
                pcol = np.zeros((n, 1))
                
                for i in range(n):
                    pyi = y[[i], :]
                    pyi = pyi.T
                    npyi = np.linalg.norm(pyi)
                    if (npyi == 0):
                        pcol[i] = 0
                    else:
                        pyi = pyi / npyi
                        t1 = np.matmul(y, pyi)
                        pcol[i] = self.__r_mad(t1)
                        
                istar = np.argmax(pcol)
                lambdastar = pcol[istar]
                Lambda.append(lambdastar)
                vhelp = y[[istar], :].T
                vhelp = vhelp / np.linalg.norm(vhelp)
                scores = np.matmul(y, vhelp)
                y = y - np.matmul(scores, vhelp.T)
                
            else:
                
                i = 0
                
                while (np.linalg.norm(y[i,:]) == 0):
                    i += 1
                
                vhelp = y[[i],:].T
                vhelp = vhelp / np.linalg.norm(vhelp)
                scores = np.matmul(v,vhelp)
                Lambda.append(self.__r_mad(scores))
                
            veig.append(vhelp)
            X_new[:, [k]] = scores
    
        if (pold > n):
            # untested
            veig = np.matmul(v, veig)
    
        self.lmbda_ = np.power(Lambda, 2)
        self.components_ = np.squeeze(veig)
        
        return X_new