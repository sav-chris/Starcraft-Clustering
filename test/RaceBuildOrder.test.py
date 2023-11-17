import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
#from ..src.RaceBuildOrder import RaceBuildOrder
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
import RaceBuildOrder
import numpy.testing
import numpy as np
#from ..src.Constants import Constants
import Constants
import TestConstants
import glob
from typing import List
from typing import Type
import Hyperparameters
from typing import Dict


class TestRaceBuildOrder(unittest.TestCase):

    def test_set_race(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        self.assertEqual(race_build_order.Race, race_build_order.Race.Zerg)

    def test_add_terran_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusTerran), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Hatchery', 'Drone']
        #race_build_order.add_terran_build_order(test_build_order) 
        race_build_order.add_race_build_order(Constants.Race.Terran, test_build_order) 
        self.assertEqual(len(race_build_order.VersusTerran), 1)

    def test_add_zerg_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusZerg), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Hatchery', 'Drone']
        #race_build_order.add_zerg_build_order(test_build_order) 
        race_build_order.add_race_build_order(Constants.Race.Zerg, test_build_order) 
        self.assertEqual(len(race_build_order.VersusZerg), 1)

    def test_add_protoss_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.BuildOrdersVersusRace[Constants.Race.Protoss]), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Hatchery', 'Drone']
        #race_build_order.add_protoss_build_order(test_build_order) 
        race_build_order.add_race_build_order(Constants.Race.Protoss, test_build_order) 
        self.assertEqual(len(race_build_order.BuildOrdersVersusRace[Constants.Race.Protoss]), 1)
    
    def test_build_labels(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        test_lables1 : RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Drone', 'Spawning Pool', 'Zergling']
        test_lables2 : RaceBuildOrder.BUILD_ORDER_STR = ['Drone', 'Extractor', 'Hatchery', 'Zergling']
        race_build_order.Label_Encoder.learn_words(test_lables1)
        race_build_order.Label_Encoder.learn_words(test_lables2)
        test_lables3 : RaceBuildOrder.BUILD_ORDER_STR = ['Spawning Pool', 'Drone', 'Extractor']
        test_build_order: RaceBuildOrder.BUILD_ORDER = race_build_order.Label_Encoder.transform(test_lables3)
        numpy.testing.assert_array_equal(race_build_order.decode_labels(test_build_order), np.array(test_lables3))

    def test_compute_levenshtein_matrices(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Protoss)
        
        test_lables1 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Gateway', 'Nexus', 'Cybernetics Core', 'Assimilator']
        test_lables2 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Gateway', 'Gateway', 'Cybernetics Core', 'Assimilator', 'Pylon']
        test_lables3 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Forge', 'Pylon', 'Probe', 'Photon Cannon', 'Pylon']
        
        race_build_order.add_race_build_order(Constants.Race.Protoss, test_lables1)
        race_build_order.add_race_build_order(Constants.Race.Protoss, test_lables2)
        race_build_order.add_race_build_order(Constants.Race.Protoss, test_lables3)

        pLength = len(race_build_order.BuildOrdersVersusRace[Constants.Race.Protoss])
        race_build_order.RaceDistanceMatrix[Constants.Race.Protoss] = np.zeros((pLength, pLength))
        
        race_build_order.compute_distance_matrix(race_build_order.RaceDistanceMatrix[Constants.Race.Protoss], race_build_order.BuildOrdersVersusRace[Constants.Race.Protoss])

        #check symmetry 
        self.assertTrue(np.allclose(race_build_order.RaceDistanceMatrix[Constants.Race.Protoss], race_build_order.RaceDistanceMatrix[Constants.Race.Protoss].T))

        #Check 3 x 3
        self.assertTrue((race_build_order.RaceDistanceMatrix[Constants.Race.Protoss].shape == np.array([3,3])).all())

        #Check diagonal is all zeros 
        self.assertFalse(race_build_order.RaceDistanceMatrix[Constants.Race.Protoss].diagonal().any())

    def test_levenshtein_paths(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Protoss)

        paths : Dict[int, str] = race_build_order.construct_paths(Constants.LEVENSHTEIN_DIR)
        # VT_NPY, VZ_NPY, VP_NPY = race_build_order.construct_paths(Constants.LEVENSHTEIN_DIR)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.PROTOSS_VT ), paths[Constants.Race.Terran])
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.PROTOSS_VZ ), paths[Constants.Race.Zerg])
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.PROTOSS_VP ), paths[Constants.Race.Protoss])

        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        #VT_NPY, VZ_NPY, VP_NPY = race_build_order.construct_paths(Constants.LEVENSHTEIN_DIR)
        paths : Dict[int, str] = race_build_order.construct_paths(Constants.LEVENSHTEIN_DIR)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.ZERG_VT ), paths[Constants.Race.Terran])
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.ZERG_VZ ), paths[Constants.Race.Zerg])
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.ZERG_VP ), paths[Constants.Race.Protoss])

        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Terran)
        #VT_NPY, VZ_NPY, VP_NPY = race_build_order.construct_paths(Constants.LEVENSHTEIN_DIR)
        paths : Dict[int, str] = race_build_order.construct_paths(Constants.LEVENSHTEIN_DIR)
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.TERRAN_VT ), paths[Constants.Race.Terran])
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.TERRAN_VZ ), paths[Constants.Race.Zerg])
        self.assertEqual(os.path.join(Constants.LEVENSHTEIN_DIR, Constants.TERRAN_VP ), paths[Constants.Race.Protoss])

    def test_OPTICS_clustering(self):
        hyperparameters: Hyperparameters = Hyperparameters.Hyperparameters()

        race_build_order_t : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Terran)
        race_build_order_z : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Zerg)
        race_build_order_p : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Protoss)

        race_build_order_t.load_distance_matricies(TestConstants.TEST_LEVENSHTEIN_DIR)
        race_build_order_z.load_distance_matricies(TestConstants.TEST_LEVENSHTEIN_DIR)
        race_build_order_p.load_distance_matricies(TestConstants.TEST_LEVENSHTEIN_DIR)
        
        race_build_order_t.OPTICS_clustering(hyperparameters)
        race_build_order_t.OPTICS_clustering(hyperparameters)
        race_build_order_t.OPTICS_clustering(hyperparameters)

        print('')

    def find_files(self, directory: str, pattern: str)->List[str]:
        filepattern: str = os.path.join(directory, pattern)
        matching_files: List[str] = glob.glob(filepattern,  recursive=True)
        return matching_files

    def test_save_build_orders(self):
        build_order_files: List[str] = self.find_files(TestConstants.TEST_BUILD_ORDER_DIR, Constants.BUILD_ORDER_DIR_FILTER)
        #clear the old build orders
        for file in build_order_files:
            os.remove(file)

        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Protoss)

        test_lables1 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Gateway', 'Nexus', 'Cybernetics Core', 'Assimilator']
        test_lables2 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Gateway', 'Gateway', 'Cybernetics Core', 'Assimilator', 'Pylon']
        test_lables3 : RaceBuildOrder.BUILD_ORDER_STR = ['Probe', 'Probe', 'Pylon', 'Forge', 'Pylon', 'Probe', 'Photon Cannon', 'Pylon']

        race_build_order.add_race_build_order(Constants.Race.Protoss, test_lables1)
        race_build_order.add_race_build_order(Constants.Race.Protoss, test_lables2)
        race_build_order.add_race_build_order(Constants.Race.Protoss, test_lables3)

        race_build_order.save_build_orders(TestConstants.TEST_BUILD_ORDER_DIR)

        build_order_files: List[str] = self.find_files(TestConstants.TEST_BUILD_ORDER_DIR, Constants.BUILD_ORDER_DIR_FILTER)
        self.assertGreater(len(build_order_files), 0)

        race_build_order_loaded : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Protoss)
        race_build_order_loaded.load_build_orders(TestConstants.TEST_BUILD_ORDER_DIR)

        self.assertEqual(len(race_build_order_loaded.BuildOrdersVersusRace[Constants.Race.Protoss]), 3)

    def test_construct_paths(self):
        directory:str = ''
        race_build_order_t : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Terran)
        paths : Dict[int, str] = race_build_order_t.construct_paths(directory)
        #VT_NPY, VZ_NPY, VP_NPY = race_build_order_t.construct_paths(directory)
        self.assertEqual( paths[Constants.Race.Terran], 'TERRAN_VT.npy' )
        self.assertEqual( paths[Constants.Race.Zerg], 'TERRAN_VZ.npy' )
        self.assertEqual( paths[Constants.Race.Protoss], 'TERRAN_VP.npy' )

        race_build_order_z : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Zerg)
        #VT_NPY, VZ_NPY, VP_NPY = race_build_order_z.construct_paths(directory)
        paths : Dict[int, str] = race_build_order_t.construct_paths(directory)
        self.assertEqual( paths[Constants.Race.Terran], 'ZERG_VT.npy' )
        self.assertEqual( paths[Constants.Race.Zerg], 'ZERG_VZ.npy' )
        self.assertEqual( paths[Constants.Race.Protoss], 'ZERG_VP.npy' )

        race_build_order_p : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(Constants.Race.Protoss)
        #VT_NPY, VZ_NPY, VP_NPY = race_build_order_p.construct_paths(directory)
        paths : Dict[int, str] = race_build_order_t.construct_paths(directory)
        self.assertEqual( paths[Constants.Race.Terran], 'PROTOSS_VT.npy' )
        self.assertEqual( paths[Constants.Race.Zerg], 'PROTOSS_VZ.npy' )
        self.assertEqual( paths[Constants.Race.Protoss], 'PROTOSS_VP.npy' )

if __name__ == '__main__':
    unittest.main()

    