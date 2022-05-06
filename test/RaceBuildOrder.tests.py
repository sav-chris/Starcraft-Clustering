import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import RaceBuildOrder
import numpy.testing
import numpy as np
import Constants
import TestConstants

class TestRaceBuildOrder(unittest.TestCase):

    def test_set_race(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        self.assertEqual(race_build_order.Race, race_build_order.Race.Zerg)

    def test_add_terran_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusTerran), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Hatchery', 'Drone']
        race_build_order.add_terran_build_order(test_build_order) 
        self.assertEqual(len(race_build_order.VersusTerran), 1)

    def test_add_zerg_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusZerg), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Hatchery', 'Drone']
        race_build_order.add_zerg_build_order(test_build_order) 
        self.assertEqual(len(race_build_order.VersusZerg), 1)

    def test_add_protoss_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusProtoss), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Hatchery', 'Drone']
        race_build_order.add_protoss_build_order(test_build_order) 
        self.assertEqual(len(race_build_order.VersusProtoss), 1)
    
    def test_build_labels(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        test_lables1 : RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Spawning Pool', 'Zergling']
        test_lables2 : RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Extractor', 'Hatchery', 'Zergling']
        race_build_order.build_labels(test_lables1)
        race_build_order.build_labels(test_lables2)
        test_lables3 : RaceBuildOrder.BUILD_ORDER_STR = ['Spawning Pool', 'Drone', 'Extractor']
        test_build_order: RaceBuildOrder.BUILD_ORDER = race_build_order.Label_Encoder.transform(test_lables3)
        numpy.testing.assert_array_equal(race_build_order.decode_labels(test_build_order), np.array(test_lables3))

    def test_compute_levenshtein_matrices(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Protoss)

        test_lables1 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Gateway', 'Nexus', 'Cybernetics Core', 'Assimilator']
        test_lables2 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Gateway', 'Gateway', 'Cybernetics Core', 'Assimilator', 'Pylon']
        test_lables3 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Forge', 'Pylon', 'Probe', 'Photon Cannon', 'Pylon']

        race_build_order.add_protoss_build_order(test_lables1)
        race_build_order.add_protoss_build_order(test_lables2)
        race_build_order.add_protoss_build_order(test_lables3)

        pLength = len(race_build_order.VersusProtoss)
        race_build_order.ProtossLevenshteinMatrix = np.zeros((pLength, pLength))
        
        race_build_order.compute_levenshtein_matrix(race_build_order.ProtossLevenshteinMatrix, race_build_order.VersusProtoss)

        #check symmetry 
        self.assertTrue(np.allclose(race_build_order.ProtossLevenshteinMatrix, race_build_order.ProtossLevenshteinMatrix.T))

        #Check 3 x 3
        self.assertTrue((race_build_order.ProtossLevenshteinMatrix.shape == np.array([3,3])).all())

        #Check diagonal is all zeros 
        self.assertFalse(race_build_order.ProtossLevenshteinMatrix.diagonal().any())

    def test_levenshtein_paths(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Protoss)
        VT_NPY, VZ_NPY, VP_NPY = race_build_order.levenshtein_paths(Constants.LEVENSHTEIN_DIR)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.PROTOSS_VT ), VT_NPY)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.PROTOSS_VZ ), VZ_NPY)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.PROTOSS_VP ), VP_NPY)

        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        VT_NPY, VZ_NPY, VP_NPY = race_build_order.levenshtein_paths(Constants.LEVENSHTEIN_DIR)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.ZERG_VT ), VT_NPY)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.ZERG_VZ ), VZ_NPY)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.ZERG_VP ), VP_NPY)

        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Terran)
        VT_NPY, VZ_NPY, VP_NPY = race_build_order.levenshtein_paths(Constants.LEVENSHTEIN_DIR)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.TERRAN_VT ), VT_NPY)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.TERRAN_VZ ), VZ_NPY)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.TERRAN_VP ), VP_NPY)

    def test_OPTICS_clustering(self):
        race_build_order_t : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Terran)
        race_build_order_z : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        race_build_order_p : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Protoss)

        race_build_order_t.load_levenshtein_matricies(TestConstants.TEST_LEVENSHTEIN_DIR)
        race_build_order_z.load_levenshtein_matricies(TestConstants.TEST_LEVENSHTEIN_DIR)
        race_build_order_p.load_levenshtein_matricies(TestConstants.TEST_LEVENSHTEIN_DIR)
        
        Terran_vt, Terran_vz, Terran_vp = race_build_order_t.OPTICS_clustering()
        Zerg_vt, Zerg_vz, Zerg_vp = race_build_order_t.OPTICS_clustering()
        Protoss_vt, Protoss_vz, Protoss_vp = race_build_order_t.OPTICS_clustering()

        print('')


if __name__ == '__main__':
    unittest.main()

    