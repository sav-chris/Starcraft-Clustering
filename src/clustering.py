import numpy as np
from numpy import array
import numpy.typing as npt
from sklearn.cluster import OPTICS
from ClusteringController import ClusteringController
import Constants
import Hyperparameters

hyperparameters: Hyperparameters = Hyperparameters.Hyperparameters(
    Constants.CUTOFF_TIME, 
    Constants.CLUST_PARAMS, 
    filter_cheap_units=False,
    distance_metric=Constants.DistanceMetric.Histogram_Jensen_Shannon,
    ComputeHistogram = False
    )
clustering_controller: ClusteringController = ClusteringController(hyperparameters)

if clustering_controller.count_npy_files_in_dir(Constants.BUILD_ORDER_DIR) == 0:
    print('Loading Replay Files ... ')
    clustering_controller.load_directory(Constants.DATA_DIR, True)
    clustering_controller.save_build_orders(Constants.BUILD_ORDER_DIR)
else:
    print('Loading Cached Build Orders ... ')
    clustering_controller.load_build_orders(Constants.BUILD_ORDER_DIR)

if clustering_controller.count_npy_files_in_dir(Constants.LEVENSHTEIN_DIR) == 0:
    print('Computing Distance Matricies ... ')
    
    clustering_controller.compute_distance_matrices(verbose=True, distance_metric=hyperparameters.distance_metric)
    clustering_controller.save_distance_matricies(Constants.LEVENSHTEIN_DIR)
else:
    print('Loading Precomputed Distance Matricies ...')
    clustering_controller.load_distance_matricies(Constants.LEVENSHTEIN_DIR)

if clustering_controller.Hyperparameters.ComputeHistogram:
    print('Compute Histograms ...')
    clustering_controller.draw_histograms()

print('OPTICS Clustering ...')
clustering_controller.optics_clustering()
clustering_controller.draw_dendrograms()

print('Histogram Clustering')


# TO DO: decide how to compute eps=???, min_samples=???
