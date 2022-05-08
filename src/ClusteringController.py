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
                race_build_order_p1.add_protoss_build_order(replay.Player1.BuildOrder)
            if replay.Player2.Race == Constants.Race.Terran:
                race_build_order_p1.add_terran_build_order(replay.Player1.BuildOrder)
            if replay.Player2.Race == Constants.Race.Zerg:
                race_build_order_p1.add_zerg_build_order(replay.Player1.BuildOrder)

            if replay.Player1.Race == Constants.Race.Protoss:
                race_build_order_p2.add_protoss_build_order(replay.Player2.BuildOrder)
            if replay.Player1.Race == Constants.Race.Terran:
                race_build_order_p2.add_terran_build_order(replay.Player2.BuildOrder)
            if replay.Player1.Race == Constants.Race.Zerg:
                race_build_order_p2.add_zerg_build_order(replay.Player2.BuildOrder)
    
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
    
    def generate_svg(self):
        filepattern: str = os.path.join(Constants.DENDROGRAMS_DIR, Constants.GRAPHVIZ_DIR_FILTER)
        data_files: List[str] = glob.glob(filepattern)
        for file in data_files:
            dot_command:str = 'dot -T svg "{}" -O'.format(file)
            os.system(dot_command)

    def draw_dendrograms(self):
        self.TerranBuildOrders.draw_clustering()
        self.ZergBuildOrders.draw_clustering()
        self.ProtossBuildOrders.draw_clustering()
        self.generate_svg()




