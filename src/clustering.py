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

#from leven import levenshtein
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
#BUILD_ORDER: Type[np.chararray] = np.chararray
#np.chararray(

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

def levenshtein_distance_metric(left: BUILD_ORDER, right: BUILD_ORDER)->int:
    return Levenshtein.distance(left, right)
    #return Levenshtein.distance(left.tolist(), right.tolist())

class BuildOrder():
    #VersusTerran   = np.zeros(0) #Type[np.array[BUILD_ORDER]]
    #VersusZerg     = np.zeros(0)
    #VersusProtoss  = np.zeros(0)
    VersusTerran  : Type[List[BUILD_ORDER]] = [] #Type[np.array[BUILD_ORDER]]
    VersusZerg    : Type[List[BUILD_ORDER]] = []
    VersusProtoss : Type[List[BUILD_ORDER]] = []

    TerranLevenshteinMatrix  : np.array = np.zeros(0)
    ZergLevenshteinMatrix    : np.array = np.zeros(0)
    ProtossLevenshteinMatrix : np.array = np.zeros(0)

    def add_build_order(self, bo : BUILD_ORDER, bos: List[BUILD_ORDER]):
        bos.append(bo)

    def add_terran_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.VersusTerran)

    def add_zerg_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.VersusZerg)

    def add_protoss_build_order(self, bo : BUILD_ORDER):
        self.add_build_order(bo, self.VersusProtoss)

    def compute_levenshtein_matrix(self, levenshtein_matrix: np.array, build_orders : Type[List[BUILD_ORDER]]):
        length = len(build_orders)
        #TO DO: Maybe do ascii conversion in here?

        # Populate Upper triangular and mirror on lower triangular, diagonal stays zero
        for i in range(0, length):
            for j in range(i+1, length):
                print('%d, %d' % (i,j))
                left = build_orders[i]
                right = build_orders[j]
                levenshtein_matrix[i,j] = levenshtein_distance_metric(left, right)
                levenshtein_matrix[j,i] = levenshtein_matrix[i,j]

    def compute_levenshtein_matrices(self):

        tLength = len(self.VersusTerran)
        zLength = len(self.VersusZerg)
        pLength = len(self.VersusTerran)
        self.TerranLevenshteinMatrix = np.zeros((tLength, tLength)) 
        self.ZergLevenshteinMatrix   = np.zeros((zLength, zLength)) 
        self.ZergLevenshteinMatrix   = np.zeros((pLength, pLength)) 

        self.compute_levenshtein_matrix(self.TerranLevenshteinMatrix, self.VersusTerran)
        self.compute_levenshtein_matrix(self.ZergLevenshteinMatrix, self.VersusZerg)
        self.compute_levenshtein_matrix(self.ProtossLevenshteinMatrix, self.VersusProtoss)


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
        #print(", ".join([build_event['time'], build_event['name']]))
        buildOrder.append(BuildEvent(minutes, seconds, name))
        i = i + 1
    return buildOrder

# Load Data
for data_file in data_files[1:20]:
    print('Loading: ' + data_file)
    result_replay = spawningtool.parser.parse_replay(data_file)

    p1_label_encoder: LabelEncoder = zerg_label_encoder
    p2_label_encoder: LabelEncoder = zerg_label_encoder
    
    p1_race = result_replay['players'][1]['race']
    p2_race = result_replay['players'][2]['race']

    if p1_race == 'Terran':
        p1_label_encoder = terran_label_encoder
    if p1_race == 'Protoss':
        p1_label_encoder = protoss_label_encoder
    
    if p2_race == 'Terran':
        p2_label_encoder = terran_label_encoder
    if p2_race == 'Protoss':
        p2_label_encoder = protoss_label_encoder

    p1_build_order = extract_build_order(result_replay['players'][1]['buildOrder'])
    p2_build_order = extract_build_order(result_replay['players'][2]['buildOrder'])
    #p1_build_order = [event['name'] for event in p1_build_order]
    #p2_build_order = [event['name'] for event in p2_build_order]
    p1_build_order = [event.Name for event in p1_build_order]
    p2_build_order = [event.Name for event in p2_build_order]

    # TO DO: make test cases for this!
    #Build Labels
    p1_label_encoder.fit(np.append(p1_label_encoder.classes_, array(p1_build_order)))
    p2_label_encoder.fit(np.append(p2_label_encoder.classes_, array(p2_build_order)))

    p1_build_order_symbols = p1_label_encoder.transform(array(p1_build_order))
    p2_build_order_symbols = p2_label_encoder.transform(array(p2_build_order))

    #Convert to char
    p1_build_order_symbols : BUILD_ORDER = [chr(letter) for letter in p1_build_order_symbols]
    p2_build_order_symbols : BUILD_ORDER = [chr(letter) for letter in p2_build_order_symbols]
    
    #p1_build_order_symbols : BUILD_ORDER = np.asarray( [chr(letter) for letter in p1_build_order_symbols])
    #p2_build_order_symbols : BUILD_ORDER = np.asarray( [chr(letter) for letter in p2_build_order_symbols])
    

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
    
    # TO DO: Save build order data to file/db?

    #reduced_dataset = OPTICS(metric=similarity).fit(dataset)
    #clustering = dbscan(X, metric=lev_metric, eps=5, min_samples=2, algorithm='brute')
    
    #dist = ld(p1_build_order_numeric, p2_build_order_numeric)
    
    #reduced_dataset = OPTICS(metric=similarity).fit(dataset)
    
    #dist = Levenshtein.distance(p1_build_order_symbols.tolist(), p2_build_order_symbols.tolist())
    dist = Levenshtein.distance(p1_build_order_symbols, p2_build_order_symbols)

    #dist = levenshtein(p1_build_order_symbols, p2_build_order_symbols)
    #print('')


# TO DO: decide how to compute eps=???, min_samples=???

#Compute Levenshtein Matricies 
zerg_build_orders.compute_levenshtein_matrices()


clustering_ZvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(np.array(zerg_build_orders.VersusZerg))


#print('Computing TvT ...')
#clustering_TvT = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(np.array(terran_build_orders.VersusTerran))

#print('Computing TvZ ...')
#clustering_TvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(terran_build_orders.VersusZerg)

#print('Computing TvP ...')
#clustering_TvP = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(terran_build_orders.VersusProtoss)

#print('Computing ZvT ...')
#clustering_ZvT = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(zerg_build_orders.VersusTerran)

#print('Computing ZvZ ...')
#clustering_ZvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(zerg_build_orders.VersusZerg)

#print('Computing ZvP ...')
#clustering_ZvP = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(zerg_build_orders.VersusProtoss)

#print('Computing PvT ...')
#clustering_PvT = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(protoss_build_orders.VersusTerran)

#print('Computing PvZ ...')
#clustering_PvZ = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(protoss_build_orders.VersusZerg)

#print('Computing PvP ...')
#clustering_PvP = OPTICS(metric=levenshtein_distance_metric, eps=30, min_samples=5).fit(protoss_build_orders.VersusProtoss)





    