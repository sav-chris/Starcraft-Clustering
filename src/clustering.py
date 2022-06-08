import numpy as np
from numpy import array
import numpy.typing as npt
from sklearn.cluster import OPTICS
from ClusteringController import ClusteringController
import Constants
import Hyperparameters

hyperparameters: Hyperparameters = Hyperparameters.Hyperparameters(Constants.CUTOFF_TIME, Constants.CLUST_PARAMS, True)
clustering_controller: ClusteringController = ClusteringController(hyperparameters)

if clustering_controller.count_npy_files_in_dir(Constants.BUILD_ORDER_DIR) == 0:
    print('Loading Replay Files ... ')
    clustering_controller.load_directory(Constants.DATA_DIR, True)
    clustering_controller.save_build_orders(Constants.BUILD_ORDER_DIR)
else:
    print('Loading Cached Build Orders ... ')
    clustering_controller.load_build_orders(Constants.BUILD_ORDER_DIR)

if clustering_controller.count_npy_files_in_dir(Constants.LEVENSHTEIN_DIR) == 0:
    print('Computing Levenshtein Matricies ... ')
    
    clustering_controller.compute_levenshtein_matrices(True)
    clustering_controller.save_levenshtein_matricies(Constants.LEVENSHTEIN_DIR)
else:
    print('Precomputed Levenshtein Matricies Loading ...')
    clustering_controller.load_levenshtein_matricies(Constants.LEVENSHTEIN_DIR)

print('Clustering ...')
clustering_controller.optics_clustering()
clustering_controller.draw_dendrograms()



# TO DO: decide how to compute eps=???, min_samples=???
