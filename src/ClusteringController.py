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
from datetime import datetime
import Hyperparameters
import json

class ClusteringController:
    
    def __init__(self, hyperparameters: Hyperparameters=Hyperparameters.Hyperparameters()):
        self.TerranBuildOrders : RaceBuildOrder = RaceBuildOrder(Race.Terran)
        self.ZergBuildOrders   : RaceBuildOrder = RaceBuildOrder(Race.Zerg)
        self.ProtossBuildOrders: RaceBuildOrder = RaceBuildOrder(Race.Protoss)
        self.Hyperparameters = hyperparameters

    def save_hyperparameters(self, filename: str):
        paramsJsonStr = json.dumps(self.Hyperparameters, default=lambda obj: obj.__dict__)

        with open(filename, "w") as text_file:
            text_file.write(paramsJsonStr)
        
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
            replay: Replay = Replay(result_replay, self.Hyperparameters.CutOffTime, self.Hyperparameters.filter_cheap_units)
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

    def compute_distance_matrices(self, verbose:bool = False, distance_metric: Constants.DistanceMetric = Hyperparameters.distance_metric)->None:
        self.TerranBuildOrders.compute_distance_matrices(verbose, distance_metric)
        self.ZergBuildOrders.compute_distance_matrices(verbose, distance_metric)
        self.ProtossBuildOrders.compute_distance_matrices(verbose, distance_metric)

    def save_distance_matricies(self, directory: str)->None:
        self.TerranBuildOrders.save_distance_matricies(directory)
        self.ZergBuildOrders.save_distance_matricies(directory)
        self.ProtossBuildOrders.save_distance_matricies(directory)

    def load_distance_matricies(self, directory: str)->None:
        self.TerranBuildOrders.load_distance_matricies(directory)
        self.ZergBuildOrders.load_distance_matricies(directory)
        self.ProtossBuildOrders.load_distance_matricies(directory)

    def count_npy_files_in_dir(self, directory: str)->int:
        filepattern: str = os.path.join(directory, Constants.LEVENSHTEIN_DIR_FILTER)
        data_files: List[str] = glob.glob(filepattern,  recursive=True)
        return len(data_files)
    

    def count_files_in_dir(self, directory: str, pattern: str)->int:
        filepattern: str = os.path.join(directory, pattern)
        data_files: List[str] = glob.glob(filepattern,  recursive=True)
        return len(data_files)


    def optics_clustering(self):
        Terran_vT, Terran_vZ, Terran_vP = self.TerranBuildOrders.OPTICS_clustering(self.Hyperparameters)
        Zerg_vT, Zerg_vZ, Zerg_vP = self.ZergBuildOrders.OPTICS_clustering(self.Hyperparameters)
        Protoss_vT, Protoss_vZ, Protoss_vP = self.ProtossBuildOrders.OPTICS_clustering(self.Hyperparameters)

        return Terran_vT, Terran_vZ, Terran_vP, Zerg_vT, Zerg_vZ, Zerg_vP, Protoss_vT, Protoss_vZ, Protoss_vP
    
    def generate_svg(self, folder):
        filepattern: str = os.path.join(folder, Constants.GRAPHVIZ_DIR_FILTER)
        data_files: List[str] = glob.glob(filepattern)
        for file in data_files:
            dot_command:str = 'dot -T svg "{}" -O'.format(file)
            os.system(dot_command)

    def make_timestamp_folder(self, root_dir:str)->str:
        timestamp:str = datetime.today().isoformat()
        timestamp = timestamp.replace(":", "-") 
        timestamp_folder: str = os.path.join(root_dir, timestamp)
        os.makedirs(timestamp_folder, exist_ok=True)
        return timestamp_folder


    def draw_dendrograms(self):
        timestamp_folder:str = self.make_timestamp_folder(Constants.DENDROGRAMS_DIR) 
        
        self.TerranBuildOrders.draw_clustering(timestamp_folder)
        self.ZergBuildOrders.draw_clustering(timestamp_folder)
        self.ProtossBuildOrders.draw_clustering(timestamp_folder)
        self.generate_svg(timestamp_folder)

        self.save_hyperparameters(os.path.join(timestamp_folder, Constants.HyperparametersFilename))


    def draw_histograms(self):
        timestamp_folder:str = self.make_timestamp_folder(Constants.HIST_DIR)

        self.TerranBuildOrders.draw_histograms(timestamp_folder)
        self.ZergBuildOrders.draw_histograms(timestamp_folder)
        self.ProtossBuildOrders.draw_histograms(timestamp_folder)

        self.save_hyperparameters(os.path.join(timestamp_folder, Constants.HyperparametersFilename))

        







        

        
        

        
        
        