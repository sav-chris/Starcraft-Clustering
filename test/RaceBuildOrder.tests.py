import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import RaceBuildOrder
import numpy.testing
import numpy as np


class TestRaceBuildOrder(unittest.TestCase):

    def test_set_race(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)
        self.assertEqual(race_build_order.Race, race_build_order.Race.Zerg)

    def test_add_terran_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusTerran), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER = [1, 2, 3, 4]
        race_build_order.add_terran_build_order(test_build_order) 
        self.assertEqual(len(race_build_order.VersusTerran), 1)

    def test_add_zerg_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusZerg), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER = [1, 2, 3, 4]
        race_build_order.add_zerg_build_order(test_build_order) 
        self.assertEqual(len(race_build_order.VersusZerg), 1)

    def test_add_protoss_build_order(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Zerg)

        self.assertEqual(len(race_build_order.VersusProtoss), 0)
        test_build_order: RaceBuildOrder.BUILD_ORDER = [1, 2, 3, 4]
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
        


if __name__ == '__main__':
    unittest.main()

    