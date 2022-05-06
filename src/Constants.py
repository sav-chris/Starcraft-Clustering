from enum import Enum
from typing import List
from typing import Type
from rapidfuzz.distance import Levenshtein
import os

class Race(Enum):
    Terran = 1
    Zerg = 2
    Protoss = 3

class GameTime:
    def __init__(self, minutes: int, seconds:int):
        self.Minutes: int = minutes
        self.Seconds: int = seconds

CUTOFF_TIME: GameTime = GameTime(4, 0)        

class ClusteringParams:
    def __init__(self, epsilon: int, min_samples: int):
        self.epsilon: int = epsilon
        self.min_samples = min_samples

CLUST_PARAMS: ClusteringParams = ClusteringParams(30, 5)        

class BuildEvent:
    def __init__(self, minutes, seconds, name):
        self.Minutes: int = minutes
        self.Seconds: int = seconds
        self.Name: str = name

BUILD_ORDER: Type[List[int]] = List[int] 
BUILD_ORDER_STR: Type[List[str]] = List[str] 
BUILD_ORDER_CHR: Type[List[str]] = List[str] 

DATA_DIR_FILTER: str = "**\*.SC2Replay"
LEVENSHTEIN_DIR_FILTER: str = "**\*.npy"
ROOT_DIR: str = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR: str = os.path.join(ROOT_DIR, 'Data')
LEVENSHTEIN_DIR: str = os.path.join(ROOT_DIR, 'levenshtein')

TERRAN_VT: str = 'TERRAN_VT.npy'
TERRAN_VZ: str = 'TERRAN_VZ.npy'
TERRAN_VP: str = 'TERRAN_VP.npy'
PROTOSS_VT: str = 'PROTOSS_VT.npy'
PROTOSS_VZ: str = 'PROTOSS_VZ.npy'
PROTOSS_VP: str = 'PROTOSS_VP.npy'
ZERG_VT: str = 'ZERG_VT.npy'
ZERG_VZ: str = 'ZERG_VZ.npy'
ZERG_VP: str = 'ZERG_VP.npy'


def levenshtein_distance_metric(left: BUILD_ORDER_CHR, right: BUILD_ORDER_CHR)->int:
    return Levenshtein.distance(left, right)


