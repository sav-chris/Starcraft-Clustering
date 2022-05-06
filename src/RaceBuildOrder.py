from typing import List
from typing import Type
import numpy as np
from numpy import array
from sklearn.preprocessing import LabelEncoder
from Constants import BUILD_ORDER
from Constants import BUILD_ORDER_STR
from Constants import Race
from Constants import levenshtein_distance_metric
import Constants
import os
from sklearn.cluster import OPTICS

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

    def compute_levenshtein_matrices(self, verbose:bool = False)->None:

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


    def build_labels(self, build_order: BUILD_ORDER_STR)->None:
        self.Label_Encoder.fit(np.append(self.Label_Encoder.classes_, array(build_order)))

    def decode_labels(self, build_order: BUILD_ORDER)->BUILD_ORDER_STR:
        return self.Label_Encoder.inverse_transform(build_order)

    def levenshtein_paths(self, directory: str):
        VT_NPY: str = ''
        VZ_NPY: str = ''
        VP_NPY: str = ''
        match self.Race:
            case Race.Zerg:
                VT_NPY = Constants.ZERG_VT
                VZ_NPY = Constants.ZERG_VZ
                VP_NPY = Constants.ZERG_VP
            case Race.Protoss:
                VT_NPY = Constants.PROTOSS_VT
                VZ_NPY = Constants.PROTOSS_VZ
                VP_NPY = Constants.PROTOSS_VP
            case Race.Terran:
                VT_NPY = Constants.TERRAN_VT
                VZ_NPY = Constants.TERRAN_VZ
                VP_NPY = Constants.TERRAN_VP

        VT_NPY = os.path.join(directory, VT_NPY)
        VZ_NPY = os.path.join(directory, VZ_NPY)
        VP_NPY = os.path.join(directory, VP_NPY)
        return VT_NPY, VZ_NPY, VP_NPY

    def save_levenshtein_matricies(self, directory: str)->None:
        VT_NPY, VZ_NPY, VP_NPY = self.levenshtein_paths(directory)
        np.save(VT_NPY, self.TerranLevenshteinMatrix)
        np.save(VZ_NPY, self.ZergLevenshteinMatrix)
        np.save(VP_NPY, self.ProtossLevenshteinMatrix)

    def load_levenshtein_matricies(self, directory:str)->None:
        VT_NPY, VZ_NPY, VP_NPY = self.levenshtein_paths(directory)
        self.TerranLevenshteinMatrix  = np.load( VT_NPY)
        self.ZergLevenshteinMatrix    = np.load( VZ_NPY)
        self.ProtossLevenshteinMatrix = np.load( VP_NPY)

    def OPTICS_clustering(self):
        clustering_vT = OPTICS(eps=30, min_samples=5).fit(self.TerranLevenshteinMatrix)
        clustering_vZ = OPTICS(eps=30, min_samples=5).fit(self.ZergLevenshteinMatrix)
        clustering_vP = OPTICS(eps=30, min_samples=5).fit(self.ProtossLevenshteinMatrix)

        return clustering_vT, clustering_vZ, clustering_vP


        

