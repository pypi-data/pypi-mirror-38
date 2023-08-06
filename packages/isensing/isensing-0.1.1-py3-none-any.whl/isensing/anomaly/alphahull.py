# -*- coding: utf-8 -*-
"""
This module contains the AlphaHull class-object which does the computation of
the alpha-shape of a given set of 2-dimensional points and identify the outliers
that their distance are far away from the alpha-shape. The computation of the 
alpha-shape is based on Delaunay triangulation.

Libraries used:
    math
    numpy
    scipy.spatial (computation of Delaunay triangulation)
    shapely (plotting of the alpha-shape / alpha-convex hull)
    
References:
    http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/

"""
import math
import numpy as np
from scipy.spatial import Delaunay, distance
from shapely.geometry import MultiPoint, MultiLineString, Point, Polygon
from shapely.ops import cascaded_union, polygonize
import matplotlib.pyplot as plt

class AlphaHull:
    """
    Perform outlier detections using AlphaHull from a given set of 2-dimensional data points.
    
    AlphaHull - Computation of alpha-shape based on the delaunay triangulation. Outliers are detected where their distance are faraway from the alpha-shape.
    
    Parameters
    ----------
    n : int, optional
        The number of outliers to be identify
        
    alpha : float, optional
         The alpha value that controls the level of details or how tightly the
         boundary fits around the 2-dimensional data points. Varying the alpha 
         radius from 0 to inf produces a set of different alpha shapes unique
         for that point set.
         
    Attributes
    ----------
    X : array, shape = (n_samples, 2)
        Input data X
        
    edges : set
        A set of edges (point_i, point_j) added during the computation of the 
        alpha-shape.
        
    edge_points : list
        A list of coordinates points added during the computation of the alpha-
        shape that will be used to compute the concave hull.
        
    concave_hull : polygonize triangles
        The computed alpha-shape hull based on the delaunay triangulation.
        
    outliers : arrary, shape = (n, 2)
        The list of n outliers with its x,y coordinates.
        
    outliers_scores : array, shape = (n, 1)
        The distances metric associated with the identified outliers and the
        alpha-shape.
        
    References:
        http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/        
    """
    
    def __init__(self, n=10, alpha=0.8):
        
        self.n = n
        self.alpha = alpha
        
    def __get_alpha_shape(self):
        
        from descartes import PolygonPatch
        
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        margin = .3
        x_min, y_min, x_max, y_max = self.concave_hull.bounds
        ax.set_xlim([x_min-margin, x_max+margin])
        ax.set_ylim([y_min-margin, y_max+margin])
        patch = PolygonPatch(self.concave_hull,
                             fc='#999999',
                             ec='#000000',
                             fill=True,
                             zorder=-1)
        ax.add_patch(patch)
        return fig
    
    def plot_alpha_shape(self):
        """Plot the computed alpha-shape on the 2D plane.
        """
        import pylab as pl
        try:
            self.concave_hull
        except AttributeError:
            print("ERROR: Please fit your data before plotting alpha shape")
        else:
            self.__get_alpha_shape()
            pl.plot(self.X[:, 0], self.X[:, 1], 'o', color='#f16824')
            pl.title("alpha : %s" % self.alpha)
        
    def __plot_outliers(self):
        """Plot all data points with outliers on the 2D plane.
        """
        plt.scatter(self.X[:, 0], self.X[:, 1], marker='.', c='blue')
        plt.scatter(self.outliers[:, 0], self.outliers[:, 1], marker='x', c='red')
        plt.title("AlphaHull")
        plt.show()        

    def __add_edge(self, coords, i, j):
        """Add a line between the i-th and j-th points, if not in the list already.
        """
        
        if (i, j) in self.edges or (j, i) in self.edges:
            return # already added
        self.edges.add((i, j))
        self.edge_points.append(coords[[i, j]])
        
    def __compute_concave_hull(self, X):
        """Computes the alpha-shape / alpha-convex hull based on based on 
        Delaunay triangulation.
        """
        
        if len(X) < 4:
            # When you have a triangle, there is no sense
            # in computing an alpha shape.
            return MultiPoint(list(X)).convex_hull
        
        tri = Delaunay(X)
        
        for ia, ib, ic in tri.vertices:
            
            pa = X[ia]
            pb = X[ib]
            pc = X[ic]
            
            # Lengths of sides of triangle
            a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
            b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
            c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
            
            # Semiperimeter of triangle
            s = (a + b + c)/2.0
            
            # Area of triangle by Heron's formula
            area = math.sqrt(s*(s-a)*(s-b)*(s-c))
            circum_r = a*b*c/(4.0*area)
            
            # Here's the radius filter.
            #print circum_r
            if circum_r < 1.0/self.alpha:
                self.__add_edge(X, ia, ib)
                self.__add_edge(X, ib, ic)
                self.__add_edge(X, ic, ia)
                
        m = MultiLineString(self.edge_points)
        triangles = list(polygonize(m))
        concave_hull = cascaded_union(triangles)
        return concave_hull
    
    def fit(self, X, plot_outliers=False):
        """Perform outlier detections using AlphaHull computation from the 
        2-dimensional data points.

        Parameters
        ----------
        X : array of shape (n_samples, 2)
            A feature array or 2D array of samples.

        plot_outliers : boolean (default False)
            True if plotting of the outliers is required.
            
        Returns
        -------
        outliers : ndarray, shape (n_samples, 2)
            A n_samples of outliers.  

        """        
        assert X.ndim == 2, "Input data must be 2-dimensional data."
        assert X.shape[1] == 2, "Input data must be 2-dimensional data."
        
        self.X = X
        self.edges = set()
        self.edge_points = []
        
        concave_hull = self.__compute_concave_hull(X)
        self.concave_hull = concave_hull
        
        points_in = []
        points_out = []
        
        for i in X:
            p = Point(i)
            if concave_hull.contains(p):
                points_in.append(i)
            else:
                points_out.append(i)

        points_out = np.array(points_out)
        points_in = np.array(points_in)
        
        polygon_in = Polygon(points_in)
        out_scores = [polygon_in.exterior.distance(Point(p)) for p in points_out]
        
        outliers = np.concatenate((points_out, np.expand_dims(out_scores, axis=1)), axis=1)
        outliers = outliers[outliers[:, 2].argsort()[::-1][:self.n]]
        self.outliers = outliers[:, 0:2]
        self.outliers_scores = outliers[:, -1]
        
        if plot_outliers:
            self.__plot_outliers()
        return self.outliers