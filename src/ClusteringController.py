from RaceBuildOrder import RaceBuildOrder
from typing import TypedDict
from typing import List
from typing import Dict
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
from Hyperparameters import Hyperparameters as hyperparams
import json
from sklearn.cluster import OPTICS


class ClusteringController:

    Hyperparameters : hyperparams = hyperparams()
    
    def __init__(self, hyperparameters: hyperparams=hyperparams()):
        self.RaceBuildOrders : Dict[int, RaceBuildOrder] = {}

        for race in Race:
            self.RaceBuildOrders[race] = RaceBuildOrder(race)

        self.Hyperparameters = hyperparameters

    def save_hyperparameters(self, filename: str):
        paramsJsonStr = json.dumps(self.Hyperparameters, default=lambda obj: obj.__dict__)

        with open(filename, "w") as text_file:
            text_file.write(paramsJsonStr)
        
    def select_race_build_order(self, player: Player)->RaceBuildOrder:
        
        if not player.Race in self.RaceBuildOrders:
            self.RaceBuildOrders[player.Race] = RaceBuildOrder(player.Race)
        return self.RaceBuildOrders[player.Race]


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
            
            race_build_order_p1.add_race_build_order(replay.Player2.Race, replay.Player1.BuildOrder)
            race_build_order_p2.add_race_build_order(replay.Player1.Race, replay.Player2.BuildOrder)

    
    def save_build_orders(self, directory: str)->None:
        for race in self.RaceBuildOrders:
            self.RaceBuildOrders[race].save_build_orders(directory)

    def load_build_orders(self, directory: str)->None:
        for race in self.RaceBuildOrders:
            self.RaceBuildOrders[race].load_build_orders(directory)

    def compute_distance_matrices(self, verbose:bool = False, distance_metric: Constants.DistanceMetric = Hyperparameters.distance_metric)->None:
        for race in self.RaceBuildOrders:
            self.RaceBuildOrders[race].compute_distance_matrices(verbose, distance_metric)
        

    def save_distance_matricies(self, directory: str)->None:
        for race in self.RaceBuildOrders:
            self.RaceBuildOrders[race].save_distance_matricies(directory)


    def load_distance_matricies(self, directory: str)->None:
        for race in self.RaceBuildOrders:
            self.RaceBuildOrders[race].load_distance_matricies(directory)
            

    def count_npy_files_in_dir(self, directory: str)->int:
        filepattern: str = os.path.join(directory, Constants.LEVENSHTEIN_DIR_FILTER)
        data_files: List[str] = glob.glob(filepattern,  recursive=True)
        return len(data_files)
    

    def count_files_in_dir(self, directory: str, pattern: str)->int:
        filepattern: str = os.path.join(directory, pattern)
        data_files: List[str] = glob.glob(filepattern,  recursive=True)
        return len(data_files)


    def optics_clustering(self):
        opticsClustering : Dict[int, Dict[int, OPTICS]] = {}
        for race in self.RaceBuildOrders: 
            opticsClustering[race] : Dict[int, OPTICS] = self.RaceBuildOrders[race].OPTICS_clustering(self.Hyperparameters)

        return opticsClustering
    
    
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

        for race in self.RaceBuildOrders:
            self.RaceBuildOrders[race].draw_clustering(timestamp_folder)
        
        self.generate_svg(timestamp_folder)

        self.save_hyperparameters(os.path.join(timestamp_folder, Constants.HyperparametersFilename))


    def draw_histograms(self):
        timestamp_folder:str = self.make_timestamp_folder(Constants.HIST_DIR)

        for race in self.RaceBuildOrders:
            self.RaceBuildOrders[race].draw_histograms(timestamp_folder)

        self.save_hyperparameters(os.path.join(timestamp_folder, Constants.HyperparametersFilename))

        







        

        
        

        
        
        