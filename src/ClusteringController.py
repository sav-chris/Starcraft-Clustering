from RaceBuildOrder import RaceBuildOrder
from typing import TypedDict
from typing import List
import Constants
from Constants import GameTime, ClusteringParams, Race
import glob
import spawningtool.parser
from Player import Player
from Replay import Replay
import os
import Constants
from dendrogram import Dendrogram
import numpy as np


class ClusteringController:
    
    def __init__(self):
        self.TerranBuildOrders : RaceBuildOrder = RaceBuildOrder(Race.Terran)
        self.ZergBuildOrders   : RaceBuildOrder = RaceBuildOrder(Race.Zerg)
        self.ProtossBuildOrders: RaceBuildOrder = RaceBuildOrder(Race.Protoss)
        self.CutOffTime: GameTime = Constants.CUTOFF_TIME
        self.ClusteringParams: ClusteringParams = Constants.CLUST_PARAMS

    def select_race_build_order(self, player: Player)->RaceBuildOrder:
        race_build_order: RaceBuildOrder = self.ProtossBuildOrders
        if player.Race == Race.Terran:
                race_build_order = self.TerranBuildOrders
        if player.Race == Race.Zerg:
            race_build_order = self.ZergBuildOrders
        return race_build_order

    def load_directory(self, filepath: str, verbose: bool = False):
        filepattern: str = os.path.join(filepath, Constants.DATA_DIR_FILTER)
        data_files: List[str] = glob.glob(filepattern,  recursive=True)
        for data_file in data_files:
            if verbose:
                print("Loading: " + data_file)
            result_replay: TypedDict = spawningtool.parser.parse_replay(data_file)
            replay: Replay = Replay(result_replay, Constants.CUTOFF_TIME)
            race_build_order_p1: RaceBuildOrder = self.select_race_build_order(replay.Player1)
            race_build_order_p2: RaceBuildOrder = self.select_race_build_order(replay.Player2)

            if replay.Player2.Race == Constants.Race.Protoss:
                race_build_order_p1.add_protoss_build_order(replay.Player2.BuildOrder)
            if replay.Player2.Race == Constants.Race.Terran:
                race_build_order_p1.add_terran_build_order(replay.Player2.BuildOrder)
            if replay.Player2.Race == Constants.Race.Zerg:
                race_build_order_p1.add_zerg_build_order(replay.Player2.BuildOrder)

            if replay.Player1.Race == Constants.Race.Protoss:
                race_build_order_p2.add_protoss_build_order(replay.Player1.BuildOrder)
            if replay.Player1.Race == Constants.Race.Terran:
                race_build_order_p2.add_terran_build_order(replay.Player1.BuildOrder)
            if replay.Player1.Race == Constants.Race.Zerg:
                race_build_order_p2.add_zerg_build_order(replay.Player1.BuildOrder)
    
    def save_build_orders(self, directory: str)->None:
        self.TerranBuildOrders.save_build_orders(directory)
        self.ZergBuildOrders.save_build_orders(directory)
        self.ProtossBuildOrders.save_build_orders(directory)

    def load_build_orders(self, directory: str)->None:
        self.TerranBuildOrders.load_build_orders(directory)
        self.ZergBuildOrders.load_build_orders(directory)
        self.ProtossBuildOrders.load_build_orders(directory)

    def compute_levenshtein_matrices(self, verbose:bool = False)->None:
        self.TerranBuildOrders.compute_levenshtein_matrices(verbose)
        self.ZergBuildOrders.compute_levenshtein_matrices(verbose)
        self.ProtossBuildOrders.compute_levenshtein_matrices(verbose)

    def save_levenshtein_matricies(self, directory: str)->None:
        self.TerranBuildOrders.save_levenshtein_matricies(directory)
        self.ZergBuildOrders.save_levenshtein_matricies(directory)
        self.ProtossBuildOrders.save_levenshtein_matricies(directory)

    def load_levenshtein_matricies(self, directory: str)->None:
        self.TerranBuildOrders.load_levenshtein_matricies(directory)
        self.ZergBuildOrders.load_levenshtein_matricies(directory)
        self.ProtossBuildOrders.load_levenshtein_matricies(directory)

    def count_npy_files_in_dir(self, directory: str)->int:
        filepattern: str = os.path.join(directory, Constants.LEVENSHTEIN_DIR_FILTER)
        data_files: List[str] = glob.glob(filepattern,  recursive=True)
        return len(data_files)


    def optics_clustering(self):
        Terran_vT, Terran_vZ, Terran_vP = self.TerranBuildOrders.OPTICS_clustering()
        Zerg_vT, Zerg_vZ, Zerg_vP = self.ZergBuildOrders.OPTICS_clustering()
        Protoss_vT, Protoss_vZ, Protoss_vP = self.ProtossBuildOrders.OPTICS_clustering()

        return Terran_vT, Terran_vZ, Terran_vP, Zerg_vT, Zerg_vZ, Zerg_vP, Protoss_vT, Protoss_vZ, Protoss_vP

    def draw_dendrograms(self):
        self.TerranBuildOrders.draw_clustering()
        self.ZergBuildOrders.draw_clustering()
        self.ProtossBuildOrders.draw_clustering()


    # def draw_dendrogram(self, clustering, race1: Race, race2: Race):
    #     filename: str = ''
    #     race_build_order: RaceBuildOrder = None
    #     build_order: List[Constants.BUILD_ORDER] = []
    #     match race1:
    #         case Race.Terran:
    #             match race2:
    #                 case Race.Terran:
    #                     filename = Constants.TERRAN_VT_GV
    #                     build_order = 
    #                 case Race.Zerg:
    #                     filename = Constants.TERRAN_VZ_GV
    #                 case Race.Protoss:
    #                     filename = Constants.TERRAN_VP_GV
    #         case Race.Zerg:
    #             match race2:
    #                 case Race.Terran:
    #                     filename = Constants.ZERG_VT_GV
    #                 case Race.Zerg:
    #                     filename = Constants.ZERG_VZ_GV
    #                 case Race.Protoss:
    #                     filename = Constants.ZERG_VP_GV
    #         case Race.Protoss:
    #             match race2:
    #                 case Race.Terran:
    #                     filename = Constants.PROTOSS_VT_GV
    #                 case Race.Zerg:
    #                     filename = Constants.PROTOSS_VZ_GV
    #                 case Race.Protoss:
    #                     filename = Constants.PROTOSS_VP_GV

    #     filename = os.path.join(Constants.DENDROGRAMS_DIR, Constants.TERRAN_VT_GV)
    #     dendrogram: Dendrogram = Dendrogram("Dendrogram", filename)
        
    #     labels = clustering.labels_

    #     for i in range(0, len(labels)):
    #         build_order = self.TerranBuildOrders.VersusTerran[i]
    #         labeled_build_order = self.TerranBuildOrders.Label_Encoder.inverse_transform(build_order)
    #         if labels[i] != -1: #check not labeled noise
    #             build_order_string: str = np.array2string(labeled_build_order, separator=',')
    #             dendrogram.add_node(labels[i], build_order_string)

    #     dendrogram.draw_graph()

    # def draw_clustering(self, Terran_vT, Terran_vZ, Terran_vP, Zerg_vT, Zerg_vZ, Zerg_vP, Protoss_vT, Protoss_vZ, Protoss_vP):

    #     filename = os.path.join(Constants.DENDROGRAMS_DIR, Constants.TERRAN_VT_GV)
    #     dend_Terran_vT: Dendrogram = Dendrogram("Terran (TvT)", filename)
        
    #     tvt = Terran_vT.labels_

    #     for i in range(0, len(tvt)):
    #         build_order = self.TerranBuildOrders.VersusTerran[i]
    #         labeled_build_order = self.TerranBuildOrders.Label_Encoder.inverse_transform(build_order)
    #         if tvt[i] != -1:
    #             build_order_string: str = np.array2string(labeled_build_order, separator=',')
    #             dend_Terran_vT.add_node(tvt[i], build_order_string)

    #     dend_Terran_vT.draw_graph()

            








        
        
        
        
