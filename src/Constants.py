from enum import Enum
from typing import List
from typing import Type
from rapidfuzz.distance import Levenshtein

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

DATA_DIR_FILTER: str = "../Data/**/*.SC2Replay"


def levenshtein_distance_metric(left: BUILD_ORDER_CHR, right: BUILD_ORDER_CHR)->int:
    return Levenshtein.distance(left, right)
