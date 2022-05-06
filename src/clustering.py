import numpy as np
from numpy import array
import numpy.typing as npt
from sklearn.cluster import OPTICS
from ClusteringController import ClusteringController
import Constants


clustering_controller: ClusteringController = ClusteringController()

if clustering_controller.count_levenshtein_files_in_dir(Constants.LEVENSHTEIN_DIR) == 0:
    print('Computing Levenshtein Matricies ... ')
    clustering_controller.load_directory(Constants.DATA_DIR, True)
    clustering_controller.compute_levenshtein_matrices(True)
    clustering_controller.save_levenshtein_matricies(Constants.LEVENSHTEIN_DIR)
else:
    print('Precomputed Levenshtein Matricies Loading ...')
    clustering_controller.load_levenshtein_matricies(Constants.LEVENSHTEIN_DIR)

print('Clustering ...')
clustering_TvP = OPTICS(eps=30, min_samples=5).fit(clustering_controller.TerranBuildOrders.ProtossLevenshteinMatrix)


print(clustering_TvP)
# TO DO: decide how to compute eps=???, min_samples=???

#Compute Levenshtein Matricies 
#zerg_build_orders.compute_levenshtein_matrices()


#clustering_ZvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(np.array(zerg_build_orders.VersusZerg))


#print('Computing TvT ...')
#clustering_TvT = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(np.array(terran_build_orders.VersusTerran))

#print('Computing TvZ ...')
#clustering_TvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(terran_build_orders.VersusZerg)

#print('Computing TvP ...')
#clustering_TvP = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(terran_build_orders.VersusProtoss)

#print('Computing ZvT ...')
#clustering_ZvT = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(zerg_build_orders.VersusTerran)

#print('Computing ZvZ ...')
#clustering_ZvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(zerg_build_orders.VersusZerg)

#print('Computing ZvP ...')
#clustering_ZvP = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(zerg_build_orders.VersusProtoss)

#print('Computing PvT ...')
#clustering_PvT = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(protoss_build_orders.VersusTerran)

#print('Computing PvZ ...')
#clustering_PvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(protoss_build_orders.VersusZerg)

#print('Computing PvP ...')
#clustering_PvP = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(protoss_build_orders.VersusProtoss)





    