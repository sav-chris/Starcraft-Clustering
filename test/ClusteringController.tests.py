import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from ClusteringController import ClusteringController
import TestConstants


class TestClusteringController(unittest.TestCase):
    #def test_load_directory(self):
    #    controller: ClusteringController = ClusteringController()

    #    controller.load_directory(TestConstants.TEST_DATA_DIR)
        
    #    self.assertGreater(len(controller.TerranBuildOrders.VersusProtoss), 0)
    #    self.assertGreater(len(controller.ProtossBuildOrders.VersusTerran), 0)

    def test_clustering(self):
        controller: ClusteringController = ClusteringController()
        controller.load_build_orders(TestConstants.TEST_BUILD_ORDER_EXAMPLE_DIR)
        controller.load_levenshtein_matricies(TestConstants.TEST_LEVENSHTEIN_DIR )

        clustering_TvT, clustering_TvZ, clustering_TvP = controller.TerranBuildOrders.OPTICS_clustering()
        
        

        print('')


if __name__ == '__main__':
    unittest.main()        



