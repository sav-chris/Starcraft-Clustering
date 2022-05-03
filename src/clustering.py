import glob
from typing import List
from typing import Type
import spawningtool.parser
import datetime
from sklearn.preprocessing import LabelEncoder
from numpy import array
import numpy.typing as npt
from abc import ABC, abstractmethod
from enum import Enum

from leven import levenshtein
import numpy as np
from sklearn.cluster import dbscan
from sklearn.cluster import OPTICS
from rapidfuzz.distance import Levenshtein

NDArrayInt = npt.NDArray[np.int_]

END_TIME_MINUTES: int = 4
END_TIME_SECONDS: int = 0

data_dir_filter: str = "../Data/**/*.SC2Replay"

data_files = glob.glob(data_dir_filter,  recursive=True)

zerg_label_encoder = LabelEncoder()
zerg_label_encoder.fit(array([])) # initialise label encoder

terran_label_encoder = LabelEncoder()
terran_label_encoder.fit(array([]))

protoss_label_encoder = LabelEncoder()
protoss_label_encoder.fit(array([]))

BUILD_ORDER: Type[List[str]] = List[str] 

class Matchup(Enum):
    TvT = 1
    TvZ = 2
    TvP = 3
    ZvT = 4
    ZvP = 5
    ZvZ = 6
    PvT = 7
    PvP = 8
    PvZ = 9


class BuildOrder():
    VersusTerran  : List[BUILD_ORDER] = []
    VersusZerg    : List[BUILD_ORDER] = []
    VersusProtoss : List[BUILD_ORDER] = []
    def add_build_order(bo : BUILD_ORDER, bos: List[BUILD_ORDER]):
        bos.append(bo)

    def add_terran_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.VersusTerran)

    def add_zerg_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.VersusZerg)

    def add_protoss_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.VersusProtoss)


# Terran Matchups
# TVT
# TVP
# TVZ
class TerranBuildOrders(BuildOrder):
    TVT : List[BUILD_ORDER] = []
    TVP : List[BUILD_ORDER] = []
    TVZ : List[BUILD_ORDER] = []

    def add_tvt_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.TVT)

    def add_tvp_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.TVP)

    def add_tvz_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.TVZ)

# Zerg Matchups
# ZVT
# ZVP
# ZVZ
class ZergBuildOrders(BuildOrder):
    ZVT : List[BUILD_ORDER] = []
    ZVP : List[BUILD_ORDER] = []
    ZVZ : List[BUILD_ORDER] = []

    def add_zvt_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.ZVT)

    def add_zvp_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.ZVP)

    def add_zvz_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.ZVZ)

# Protoss Matchups
# PVT
# PVP
# PVZ 
class ProtossBuildOrders(BuildOrder):
    PVT : List[BUILD_ORDER] = []
    PVP : List[BUILD_ORDER] = []
    PVZ : List[BUILD_ORDER] = []

    def add_pvt_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.PVT)

    def add_pvp_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.PVP)

    def add_pvz_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.PVZ)


terran_build_orders  : BuildOrder = BuildOrder()
zerg_build_orders    : BuildOrder = BuildOrder()
protoss_build_orders : BuildOrder = BuildOrder()

#result_replay['players'][1]['is_winner']

class BuildEvent:
    Minutes: int = 0
    Seconds: int = 0
    Name: str

    def __init__(self, minutes, seconds, name):
        self.Minutes = minutes
        self.Seconds = seconds
        self.Name = name


def extract_build_order(build_order):
    minutes = 0
    seconds = 0
    i: int = 0
    name: str = ''
    build_length = len(build_order)
    buildOrder = []
    while (not ((minutes >= END_TIME_MINUTES) and (seconds >= END_TIME_SECONDS))) and (i < build_length):
        build_event = build_order[i]
        time = datetime.datetime.strptime(build_event["time"], "%M:%S")
        minutes = time.minute
        seconds = time.second
        name = build_event['name']
        print(", ".join([build_event['time'], build_event['name']]))
        buildOrder.append(BuildEvent(minutes, seconds, name))
        i = i + 1
    return buildOrder


for data_file in data_files:


    result_replay = spawningtool.parser.parse_replay(data_file)

    p1_label_enoder: LabelEncoder = zerg_label_encoder
    p2_label_enoder: LabelEncoder = zerg_label_encoder
    
    p1_race = result_replay['players'][1]['race']
    p2_race = result_replay['players'][2]['race']

    if p1_race == 'Terran':
        p1_label_enoder = terran_label_encoder
    if p1_race == 'Protoss':
        p1_label_enoder = protoss_label_encoder
    
    if p2_race == 'Terran':
        p2_label_enoder = terran_label_encoder
    if p2_race == 'Protoss':
        p2_label_enoder = protoss_label_encoder

    p1_build_order = extract_build_order(result_replay['players'][1]['buildOrder'])
    p2_build_order = extract_build_order(result_replay['players'][2]['buildOrder'])
    #p1_build_order = [event['name'] for event in p1_build_order]
    #p2_build_order = [event['name'] for event in p2_build_order]
    p1_build_order = [event.Name for event in p1_build_order]
    p2_build_order = [event.Name for event in p2_build_order]

    # TO DO: make test cases for this!
    #Build Labels
    p1_label_enoder.fit(np.append(p1_label_enoder.classes_, array(p1_build_order)))
    p2_label_enoder.fit(np.append(p2_label_enoder.classes_, array(p2_build_order)))

    p1_build_order_symbols = p1_label_enoder.transform(array(p1_build_order))
    p2_build_order_symbols = p2_label_enoder.transform(array(p2_build_order))

    #Convert to char
    p1_build_order_symbols : BUILD_ORDER = [chr(letter) for letter in p1_build_order_symbols]
    p2_build_order_symbols : BUILD_ORDER = [chr(letter) for letter in p2_build_order_symbols]
    

    if p1_race == 'Terran' and p2_race == 'Terran':
        terran_build_orders.add_terran_build_order (p1_build_order_symbols)
        terran_build_orders.add_terran_build_order(p2_build_order_symbols)

    if p1_race == 'Terran' and p2_race == 'Zerg':
        terran_build_orders.add_zerg_build_order(p1_build_order_symbols)
        zerg_build_orders.add_terran_build_order(p2_build_order_symbols)

    if p1_race == 'Terran' and p2_race == 'Protoss':
        terran_build_orders.add_protoss_build_order(p1_build_order_symbols)
        protoss_build_orders.add_terran_build_order(p2_build_order_symbols)

    if p1_race == 'Zerg' and p2_race == 'Terran':
        zerg_build_orders.add_terran_build_order(p1_build_order_symbols)
        terran_build_orders.add_zerg_build_order(p2_build_order_symbols)

    if p1_race == 'Zerg' and p2_race == 'Zerg':
        zerg_build_orders.add_zerg_build_order(p1_build_order_symbols)
        zerg_build_orders.add_zerg_build_order(p2_build_order_symbols)

    if p1_race == 'Zerg' and p2_race == 'Protoss':
        zerg_build_orders.add_protoss_build_order(p1_build_order_symbols)
        protoss_build_orders.add_zerg_build_order(p2_build_order_symbols)
    
    if p1_race == 'Protoss' and p2_race == 'Terran':
        protoss_build_orders.add_terran_build_order(p1_build_order_symbols)
        terran_build_orders.add_protoss_build_order(p2_build_order_symbols)

    if p1_race == 'Protoss' and p2_race == 'Zerg':
        protoss_build_orders.add_zerg_build_order(p1_build_order_symbols)
        zerg_build_orders.add_protoss_build_order(p2_build_order_symbols)

    if p1_race == 'Protoss' and p2_race == 'Protoss':
        protoss_build_orders.add_protoss_build_order(p1_build_order_symbols)
        protoss_build_orders.add_protoss_build_order(p2_build_order_symbols)
    
    #reduced_dataset = OPTICS(metric=similarity).fit(dataset)
    #clustering = dbscan(X, metric=lev_metric, eps=5, min_samples=2, algorithm='brute')
    
    #dist = ld(p1_build_order_numeric, p2_build_order_numeric)
    
    reduced_dataset = OPTICS(metric=similarity).fit(dataset)
    
    dist = Levenshtein.distance(p1_build_order_symbols, p2_build_order_symbols)

    #dist = levenshtein(p1_build_order_symbols, p2_build_order_symbols)
    print('')
    



    