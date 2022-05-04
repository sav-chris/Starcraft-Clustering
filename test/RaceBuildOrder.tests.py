import sys
import os
from pathlib import Path
import unittest
#from ..src.RaceBuildOrder import RaceBuildOrder

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR : str = Path(SCRIPT_DIR).parent.absolute()
SRC_DIR  : str = os.path.join(ROOT_DIR, 'src')

print(SCRIPT_DIR)
print(ROOT_DIR)
print(SRC_DIR)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import RaceBuildOrder
#sys.path.append(os.path.dirname(SRC_DIR))

#from RaceBuildOrder import RaceBuildOrder


class TestRaceBuildOrder(unittest.TestCase):

    def test_set_race(self):
        race_build_order : RaceBuildOrder.RaceBuildOrder = RaceBuildOrder.RaceBuildOrder(RaceBuildOrder.Race.Terran)
        self.assertEqual(race_build_order.Race, race_build_order.Race.Terran)

if __name__ == '__main__':
    unittest.main()