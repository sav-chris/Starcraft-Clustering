import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from Player import Player
import spawningtool.parser
import TestConstants
from TestConstants import TEST_REPLAY_HAS
import Constants

class TestPlayer(unittest.TestCase):
    
    def test_initialise(self):
        
        filename: str = os.path.join(TestConstants.TEST_DATA_DIR, TestConstants.TEST_REPLAY_HAS)
        has_replay = spawningtool.parser.parse_replay(filename)

        player1: Player = Player(has_replay, 1, Constants.CUTOFF_TIME)
        player2: Player = Player(has_replay, 2, Constants.CUTOFF_TIME)

        self.assertEqual(player1.Name, 'Cyan')
        self.assertEqual(player1.Race, Constants.Race.Protoss)
        self.assertEqual(player1.IsWinner, False)

        self.assertEqual(player2.Name, 'Has')
        self.assertEqual(player2.Race, Constants.Race.Protoss)
        self.assertEqual(player2.IsWinner, True)

if __name__ == '__main__':
    unittest.main()        




        



