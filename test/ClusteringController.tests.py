import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import ClusteringController

TEST_DATA_DIR:str = os.path.join(os.path.dirname(__file__), '..', 'test.data')

class TestClusteringController(unittest.TestCase):

    def test_extract_build_order(self):
        controller: ClusteringController = ClusteringController()

        result_replay = spawningtool.parser.parse_replay(data_file)

        controller.extract_build_order()

