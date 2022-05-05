from typing import List
from typing import Type
import numpy as np
from numpy import array
from sklearn.preprocessing import LabelEncoder
from Constants import BUILD_ORDER
from Constants import BUILD_ORDER_STR
from Constants import Race
from Constants import levenshtein_distance_metric


class RaceBuildOrder:

    def __init__(self, Race: Race):
        self.VersusTerran: Type[List[BUILD_ORDER]] = []
        self.VersusZerg: Type[List[BUILD_ORDER]] = []
        self.VersusProtoss: Type[List[BUILD_ORDER]] = []

        self.Label_Encoder: LabelEncoder = LabelEncoder()

        self.TerranLevenshteinMatrix: np.array = np.zeros(0)
        self.ZergLevenshteinMatrix: np.array = np.zeros(0)
        self.ProtossLevenshteinMatrix: np.array = np.zeros(0)

        self.Race = Race
        self.Label_Encoder.fit([])

    def add_build_order(self, bo : BUILD_ORDER_STR, bos: List[BUILD_ORDER_STR]):
        self.build_labels(bo)
        bos.append(self.Label_Encoder.transform(bo))

    def add_terran_build_order(self, bo : BUILD_ORDER_STR):
        self.add_build_order(bo, self.VersusTerran)

    def add_zerg_build_order(self, bo : BUILD_ORDER_STR):
        self.add_build_order(bo, self.VersusZerg)

    def add_protoss_build_order(self, bo : BUILD_ORDER_STR):
        self.add_build_order(bo, self.VersusProtoss)


    def compute_levenshtein_matrix(self, levenshtein_matrix: np.array, build_orders : Type[List[BUILD_ORDER]]):
        length = len(build_orders)
        # Populate Upper triangular and mirror on lower triangular, diagonal stays zero
        for i in range(0, length):
            for j in range(i+1, length):
                #TO DO: Possible optimisation here? 
                left = [chr(letter) for letter in build_orders[i]] 
                right = [chr(letter) for letter in build_orders[j]]
                levenshtein_matrix[i,j] = levenshtein_distance_metric(left, right)
                levenshtein_matrix[j,i] = levenshtein_matrix[i,j]

    def compute_levenshtein_matrices(self, verbose:bool = False):

        tLength = len(self.VersusTerran)
        zLength = len(self.VersusZerg)
        pLength = len(self.VersusProtoss)
        self.TerranLevenshteinMatrix  = np.zeros((tLength, tLength)) 
        self.ZergLevenshteinMatrix    = np.zeros((zLength, zLength)) 
        self.ProtossLevenshteinMatrix = np.zeros((pLength, pLength)) 

        self.compute_levenshtein_matrix(self.TerranLevenshteinMatrix,  self.VersusTerran)
        self.compute_levenshtein_matrix(self.ZergLevenshteinMatrix,    self.VersusZerg)
        self.compute_levenshtein_matrix(self.ProtossLevenshteinMatrix, self.VersusProtoss)

        if verbose:
            print(self.Race)
            print('Versus Terran: ')
            print(self.TerranLevenshteinMatrix)
            print('Versus Zerg: ')
            print(self.ZergLevenshteinMatrix)
            print('Versus Protoss: ')
            print(self.ProtossLevenshteinMatrix)


    def build_labels(self, build_order: BUILD_ORDER_STR):
        self.Label_Encoder.fit(np.append(self.Label_Encoder.classes_, array(build_order)))

    def decode_labels(self, build_order: BUILD_ORDER)->BUILD_ORDER_STR:
        return self.Label_Encoder.inverse_transform(build_order)

    



