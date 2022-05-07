import numpy as np
from numpy import array
import numpy.typing as npt
from sklearn.cluster import OPTICS
from ClusteringController import ClusteringController
import Constants


clustering_controller: ClusteringController = ClusteringController()

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
#Terran_vT, Terran_vZ, Terran_vP, Zerg_vT, Zerg_vZ, Zerg_vP, Protoss_vT, Protoss_vZ, Protoss_vP = 
clustering_controller.optics_clustering()
#Terran_vT, Terran_vZ, Terran_vP, Zerg_vT, Zerg_vZ, Zerg_vP, Protoss_vT, Protoss_vZ, Protoss_vP
clustering_controller.draw_dendrograms()



# TO DO: decide how to compute eps=???, min_samples=???
