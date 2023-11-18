from enum import Enum
from enum import IntEnum
from typing import List
from typing import Type
from rapidfuzz.distance import Levenshtein
import os
import numpy.typing as npt


class Race(Enum):
    Terran = 1
    Zerg = 2
    Protoss = 3
    Genetron = 4
    Xayid = 5
    Keiron = 6

    @classmethod
    def as_string(self, race: int):
        return Race(race).name

class DistanceMetric(IntEnum):
    Levenshtien = 1
    Histogram_Jensen_Shannon = 2
    Histogram_Kullback_Leibler = 3

class GameTime:
    def __init__(self, minutes: int, seconds:int):
        self.Minutes: int = minutes
        self.Seconds: int = seconds

CUTOFF_TIME: GameTime = GameTime(4, 0)        

class ClusteringParams:
    def __init__(self, epsilon: int, min_samples: int):
        self.epsilon: int = epsilon
        self.min_samples = min_samples

CLUST_PARAMS: ClusteringParams = ClusteringParams(30, 3)        

class BuildEvent:
    def __init__(self, minutes, seconds, name):
        self.Minutes: int = minutes
        self.Seconds: int = seconds
        self.Name: str = name

#BUILD_ORDER: Type[List[int]] = List[int] 
BUILD_ORDER: Type[npt.NDArray] = npt.NDArray 
BUILD_ORDER_STR: Type[List[str]] = List[str] 
BUILD_ORDER_CHR: Type[List[str]] = List[str] 

DATA_DIR_FILTER: str = "**\*.SC2Replay"
LEVENSHTEIN_DIR_FILTER: str = "**\*.npy"
BUILD_ORDER_DIR_FILTER: str = "**\*.npy"
GRAPHVIZ_DIR_FILTER: str = "*.gv"
HIST_DIR_FILTER: str = "*.png"
ROOT_DIR: str = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR: str = os.path.join(ROOT_DIR, 'Data')
BUILD_ORDER_DIR: str = os.path.join(ROOT_DIR, 'build.orders')
LEVENSHTEIN_DIR: str = os.path.join(ROOT_DIR, 'levenshtein')
DENDROGRAMS_DIR: str = os.path.join(ROOT_DIR, 'dendrograms')
HIST_DIR: str = os.path.join(ROOT_DIR, 'histograms')


RACE_V_RACE: str = '{0}_V{1}.npy'
#TERRAN_VT: str = 'TERRAN_VT.npy'
#TERRAN_VZ: str = 'TERRAN_VZ.npy'
#TERRAN_VP: str = 'TERRAN_VP.npy'
#ZERG_VT: str = 'ZERG_VT.npy'
#ZERG_VZ: str = 'ZERG_VZ.npy'
#ZERG_VP: str = 'ZERG_VP.npy'
#PROTOSS_VT: str = 'PROTOSS_VT.npy'
#PROTOSS_VZ: str = 'PROTOSS_VZ.npy'
#PROTOSS_VP: str = 'PROTOSS_VP.npy'


RACE_VR_GV: str = '{0}({1}v{2}).gv'
#TERRAN_VT_GV: str = 'Terran(TvT).gv'
#TERRAN_VZ_GV: str = 'Terran(TvZ).gv'
#TERRAN_VP_GV: str = 'Terran(TvP).gv'
#ZERG_VT_GV: str = 'Zerg(ZvT).gv'
#ZERG_VZ_GV: str = 'Zerg(ZvZ).gv'
#ZERG_VP_GV: str = 'Zerg(ZvP).gv'
#PROTOSS_VT_GV: str = 'Protoss(PvT).gv'
#PROTOSS_VZ_GV: str = 'Protoss(PvZ).gv'
#PROTOSS_VP_GV: str = 'Protoss(PvP).gv'

RACE_VR_HIST: str = '{0}({1}v{2})'
HIST_EXT: str = '[{}].png'
#TERRAN_VT_HIST: str = 'Terran(TvT)[{}].png'
#TERRAN_VZ_HIST: str = 'Terran(TvZ)[{}].png'
#TERRAN_VP_HIST: str = 'Terran(TvP)[{}].png'
#ZERG_VT_HIST: str = 'Zerg(ZvT)[{}].png'
#ZERG_VZ_HIST: str = 'Zerg(ZvZ)[{}].png'
#ZERG_VP_HIST: str = 'Zerg(ZvP)[{}].png'
#PROTOSS_VT_HIST: str = 'Protoss(ZvT)[{}].png'
#PROTOSS_VZ_HIST: str = 'Protoss(ZvZ)[{}].png'
#PROTOSS_VP_HIST: str = 'Protoss(ZvP)[{}].png'


UNCATEGORISED_FILE: str = 'Uncategorised.txt'

LabelEncoderRace: str = 'LabelEncoder{0}.npy'
#LabelEncoderTerran: str = 'LabelEncoderTerran.npy'
#LabelEncoderZerg: str = 'LabelEncoderZerg.npy'
#LabelEncoderProtoss: str = 'LabelEncoderProtoss.npy'

HyperparametersFilename: str = 'Hyperparameters.json'
