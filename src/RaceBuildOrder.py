from typing import List
from typing import Type
import numpy as np
import numpy.typing as npt
from numpy import array
from LabelEncoder import LabelEncoder
from Constants import BUILD_ORDER
from Constants import BUILD_ORDER_STR
from Constants import Race
from Constants import levenshtein_distance_metric
import Constants 
import os
from sklearn.cluster import OPTICS
import json
from dendrogram import Dendrogram

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


    def add_build_order(self, bo : BUILD_ORDER_STR, bos: List[BUILD_ORDER_STR]):
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

    def decode_labels(self, build_order: BUILD_ORDER)->BUILD_ORDER_STR:
        return self.Label_Encoder.inverse_transform(build_order)

    def construct_paths(self, directory: str):
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

    def load_build_order_file(self, filename: str, data: List[BUILD_ORDER])->None:
        with open(filename, 'r') as the_file:
            lines = the_file.readlines()
            for line in lines:
                build_line = [int(x) for x in line.split(',')]
                data.append(np.array(build_line))

    def save_build_order_file(self, filename: str, data: List[BUILD_ORDER])->None:
        with open(filename, 'a') as the_file:
            for build_event in data:
                the_file.write(', '.join(str(x) for x in build_event))
                the_file.write('\n')

    def save_build_orders(self, directory: str)->None:
        VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        self.save_build_order_file(VT_NPY, self.VersusTerran)
        self.save_build_order_file(VZ_NPY, self.VersusZerg)
        self.save_build_order_file(VP_NPY, self.VersusProtoss)
        # Save Labels
        match self.Race:
            case Race.Terran:
                self.Label_Encoder.save_to_file(os.path.join(directory, Constants.LabelEncoderTerran))
            case Race.Zerg:
                self.Label_Encoder.save_to_file(os.path.join(directory, Constants.LabelEncoderZerg))
            case Race.Protoss:
                self.Label_Encoder.save_to_file(os.path.join(directory, Constants.LabelEncoderProtoss))

    def load_build_orders(self, directory:str)->None:
        VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        self.load_build_order_file(VT_NPY, self.VersusTerran)
        self.load_build_order_file(VZ_NPY, self.VersusZerg)
        self.load_build_order_file(VP_NPY, self.VersusProtoss)
        # load Labels
        match self.Race:
            case Race.Terran:
                self.Label_Encoder.load_from_file(os.path.join(directory, Constants.LabelEncoderTerran))
            case Race.Zerg:
                self.Label_Encoder.load_from_file(os.path.join(directory, Constants.LabelEncoderZerg))
            case Race.Protoss:
                self.Label_Encoder.load_from_file(os.path.join(directory, Constants.LabelEncoderProtoss))


    def save_levenshtein_matricies(self, directory: str)->None:
        VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        np.save(VT_NPY, self.TerranLevenshteinMatrix)
        np.save(VZ_NPY, self.ZergLevenshteinMatrix)
        np.save(VP_NPY, self.ProtossLevenshteinMatrix)

    def load_levenshtein_matricies(self, directory:str)->None:
        VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        self.TerranLevenshteinMatrix  = np.load( VT_NPY)
        self.ZergLevenshteinMatrix    = np.load( VZ_NPY)
        self.ProtossLevenshteinMatrix = np.load( VP_NPY)

    def OPTICS_clustering(self):
        self.clustering_vT = OPTICS(eps=30, min_samples=5, metric='precomputed').fit(self.TerranLevenshteinMatrix)
        self.clustering_vZ = OPTICS(eps=30, min_samples=5, metric='precomputed').fit(self.ZergLevenshteinMatrix)
        self.clustering_vP = OPTICS(eps=30, min_samples=5, metric='precomputed').fit(self.ProtossLevenshteinMatrix)

        return self.clustering_vT, self.clustering_vZ, self.clustering_vP


    #def format_as_string(self, labeled_build_order: List[str], interval: int)->str:
    #    new_lines = list(','.join(l + '\n' * (n % interval == (interval-1))) for n, l in enumerate(labeled_build_order)))


    def draw_dendrogram(self, dendrogram: Dendrogram, clustering: OPTICS, build_orders: List[BUILD_ORDER]):
        labels = clustering.labels_
        for i in range(0, len(labels)):
            build_order = build_orders[i]
            labeled_build_order = self.Label_Encoder.inverse_transform(build_order)
            if labels[i] != -1:
                #new_lines = list(','.join(l + '\n' * (n % 4 == 3) for n, l in enumerate(labeled_build_order)))
                new_lines = [l + '\n' * (n % 4 == 3) for n, l in enumerate(labeled_build_order)]
                build_order_string: str = ','.join(new_lines)
                dendrogram.add_node(labels[i], build_order_string)
        
        dendrogram.draw_graph()
    
    def draw_clustering(self):

        match self.Race:
            case Race.Terran:
                filename_vT = Constants.TERRAN_VT_GV
                filename_vZ = Constants.TERRAN_VZ_GV
                filename_vP = Constants.TERRAN_VP_GV
            case Race.Zerg:
                filename_vT = Constants.ZERG_VT_GV
                filename_vZ = Constants.ZERG_VZ_GV
                filename_vP = Constants.ZERG_VP_GV
            case Race.Protoss:
                filename_vT = Constants.PROTOSS_VT_GV
                filename_vZ = Constants.PROTOSS_VZ_GV
                filename_vP = Constants.PROTOSS_VP_GV
 
        filename_vT = os.path.join(Constants.DENDROGRAMS_DIR, filename_vT)
        filename_vZ = os.path.join(Constants.DENDROGRAMS_DIR, filename_vZ)
        filename_vP = os.path.join(Constants.DENDROGRAMS_DIR, filename_vP)
        
        dendrogram_vT: Dendrogram = Dendrogram("Dendrogram", filename_vT)
        dendrogram_vZ: Dendrogram = Dendrogram("Dendrogram", filename_vZ)
        dendrogram_vP: Dendrogram = Dendrogram("Dendrogram", filename_vP)

        self.draw_dendrogram(dendrogram_vT, self.clustering_vT, self.VersusTerran)
        self.draw_dendrogram(dendrogram_vZ, self.clustering_vZ, self.VersusZerg)
        self.draw_dendrogram(dendrogram_vP, self.clustering_vP, self.VersusProtoss)


        
        

