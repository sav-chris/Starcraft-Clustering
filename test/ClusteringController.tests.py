import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from ClusteringController import ClusteringController
import spawningtool.parser
import TestConstants
from Constants import DATA_DIR_FILTER

class TestClusteringController(unittest.TestCase):
    def test_load_directory(self):
        controller: ClusteringController = ClusteringController()

        controller.load_directory(TestConstants.TEST_DATA_DIR)
        
        self.assertGreater(len(controller.TerranBuildOrders.VersusProtoss), 0)
        self.assertGreater(len(controller.ProtossBuildOrders.VersusTerran), 0)

if __name__ == '__main__':
    unittest.main()        



