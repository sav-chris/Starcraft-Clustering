from typing import List
from typing import Type
from typing import Callable
from typing import Dict
from typing import Tuple
import numpy as np
import numpy.typing as npt
from numpy import array
from LabelEncoder import LabelEncoder
from Constants import BUILD_ORDER
from Constants import BUILD_ORDER_STR
from Constants import Race
from Constants import DistanceMetric
import distance_metrics
import Constants 
import os
from sklearn.cluster import OPTICS
import json
from dendrogram import Dendrogram
from Hyperparameters import Hyperparameters
import collections
import Histogram as hist

class RaceBuildOrder:

    def __init__(self, Race: Race):
        self.BuildOrdersVersusRace: Dict[int, List[BUILD_ORDER]] = {}

        self.Label_Encoder: LabelEncoder = LabelEncoder()

        self.RaceDistanceMatrix: Dict[int, np.array] = {}

        self.Race = Race

        self.clustering_vRace : Dict[int, OPTICS] = {}

        for race in Constants.Race:
            self.BuildOrdersVersusRace[race] = []


    def count_uncategorised(self, optics: OPTICS)->int:
        counts:collections.Counter = collections.Counter(optics.labels_)
        return counts[-1]

    def save_uncategorised(self, filepath:str):
        print(self.Race)
        Race_Uncategorised : Dict[int, int] = {}
        for race in self.clustering_vRace.keys():
            race_str: str = Race.as_string(race)
            Race_Uncategorised[race] = self.count_uncategorised(self.clustering_vRace[self.Race])
            print(f'Uncategorised { race_str } Builds: {Race_Uncategorised[race]}')
        
        txt_uncategorised:str = f'Race: {self.Race} \n'
        for race in self.clustering_vRace.keys():
            txt_uncategorised = txt_uncategorised + f'Uncategorised { Race.as_string(race) } Builds: {Race_Uncategorised[race]} \n'

        with open(filepath, "w") as text_file:
            text_file.write(txt_uncategorised)

    def add_build_order(self, bo : BUILD_ORDER_STR, bos: List[BUILD_ORDER_STR]):
        bos.append(self.Label_Encoder.transform(bo))


    def add_race_build_order(self, race: Race, bo : BUILD_ORDER_STR):
        self.add_build_order(bo, self.BuildOrdersVersusRace[race])
    

    def compute_distance_matrix(
            self, 
            distance_matrix: np.array, 
            build_orders : Type[List[BUILD_ORDER]], 
            distance_metric: DistanceMetric = Hyperparameters.distance_metric
        ):
        length = len(build_orders)

        distance: distance_metrics.DistMetric = distance_metrics.levenshtein_distance_metric
        match distance_metric:
            case DistanceMetric.Levenshtien:
                distance = distance_metrics.levenshtein_distance_metric
            case DistanceMetric.Histogram_Jensen_Shannon:
                distance = distance_metrics.create_histogram_jensen_shannon_distance_metric(self.Label_Encoder)
            case DistanceMetric.Histogram_Kullback_Leibler:
                distance = distance_metrics.create_histogram_kullback_leibler_distance_metric(self.Label_Encoder)
            case _:
                distance = distance_metrics.levenshtein_distance_metric

        # Populate Upper triangular and mirror on lower triangular, diagonal stays zero
        for i in range(0, length):
            for j in range(i+1, length):
                distance_matrix[i,j] = distance(build_orders[i], build_orders[j])
                distance_matrix[j,i] = distance_matrix[i,j]

    def compute_distance_matrices(self, verbose:bool = False, distance_metric: Constants.DistanceMetric = Hyperparameters.distance_metric)->None:
        
        for race in self.BuildOrdersVersusRace.keys():
            raceLength: int = len(self.BuildOrdersVersusRace[race])
            self.RaceDistanceMatrix[race] = np.zeros((raceLength, raceLength))
            self.compute_distance_matrix(self.RaceDistanceMatrix[race], self.BuildOrdersVersusRace[race], distance_metric)

        if verbose:
            print(self.Race)
            for race in self.RaceDistanceMatrix.keys():
                print(f'Versus { Race.as_string(race) }: ')
                print(self.RaceDistanceMatrix[race])
            

    def decode_labels(self, build_order: BUILD_ORDER)->BUILD_ORDER_STR:
        return self.Label_Encoder.inverse_transform(build_order)
    
    def format_RvR(self, this_race : Race, vs_race: Race)->str:
        # TO DO: Does this belong somewhere else?
        return Constants.RACE_V_RACE.format(Race.as_string(this_race).upper(), Race.as_string(vs_race)[0]) 

    def construct_paths(self, directory: str)->Dict[int, str]:
        paths: Dict[int, str] = {}
        for race in self.BuildOrdersVersusRace.keys():
            filename: str = self.format_RvR(self.Race, race) 
            path: str = os.path.join(directory, filename)
            paths[race] = path

        return paths
       

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
        paths: Dict[int, str] = self.construct_paths(directory)
        for race in paths.keys():
            self.save_build_order_file(paths[race], self.BuildOrdersVersusRace[race])

        self.Label_Encoder.save_to_file
        (
            os.path.join
            (
                directory, 
                Constants.LabelEncoderRace.format
                (
                    Race.as_string(self.Race)
                )
            )
        )

    def load_build_orders(self, directory:str)->None:
        paths: Dict[int, str] = self.construct_paths(directory)
        for race in paths.keys():
            if os.path.exists(paths[race]):
                self.load_build_order_file(paths[race], self.BuildOrdersVersusRace[race])

        label_encoder: str = os.path.join(directory, Constants.LabelEncoderRace.format(Race.as_string(self.Race)))
        if os.path.exists(label_encoder):
            self.Label_Encoder.load_from_file(label_encoder)


    def save_distance_matricies(self, directory: str)->None:
        paths: Dict[int, str] = self.construct_paths(directory)
        for race in paths.keys():
            np.save(paths[race], self.RaceDistanceMatrix[race])

    def load_distance_matricies(self, directory:str)->None:
        paths: Dict[int, str] = self.construct_paths(directory)
        for race in paths.keys():
            if os.path.exists(paths[race]):
                self.RaceDistanceMatrix[race] = np.load(paths[race])


    def OPTICS_clustering(self, hyperparameters: Hyperparameters):
        
        for race in Race:
            if race in self.RaceDistanceMatrix:
                if len(self.RaceDistanceMatrix[race]) > 0:
                    self.clustering_vRace[race] = OPTICS(eps=hyperparameters.ClusteringParams.epsilon, min_samples=hyperparameters.ClusteringParams.min_samples, metric='precomputed').fit(self.RaceDistanceMatrix[race])

        return self.clustering_vRace
        
    def draw_dendrogram(self, dendrogram: Dendrogram, clustering: OPTICS, build_orders: List[BUILD_ORDER]):
        labels = clustering.labels_
        for i in range(0, len(labels)):
            build_order = build_orders[i]
            labeled_build_order = self.Label_Encoder.inverse_transform(build_order)
            if labels[i] != -1:
                # insert newlines every 4 items
                new_lines = [l + '\n' * (n % 4 == 3) for n, l in enumerate(labeled_build_order)]
                build_order_string: str = ','.join(new_lines)
                dendrogram.add_node(labels[i], build_order_string)
        
        dendrogram.draw_graph()
    
    def format_graphviz_filename(self, race1: Race, race2: Race)->str:

        race1_str: str = Race.as_string(race1)
        race2_str: str = Race.as_string(race2)
        return Constants.RACE_VR_GV.format(race1_str, race1_str[0], race2_str[0])
    
    def format_histogram_filename(self, race1: Race, race2: Race)->str:

        race1_str: str = Race.as_string(race1)
        race2_str: str = Race.as_string(race2)
        return Constants.RACE_VR_HIST.format(race1_str, race1_str[0], race2_str[0]) + Constants.HIST_EXT
            

    def draw_clustering(self, folder):
        
        dendrogram_vRace: Dict[int, Dendrogram] =  {}
        race_filenames: Dict[int, str] = { } 
        
        for race in Race:
            if len(self.BuildOrdersVersusRace[race]) > 0:
                race_filenames[race] = os.path.join(folder, self.format_graphviz_filename(self.Race, race))
                dendrogram_vRace[race] = Dendrogram("Dendrogram", race_filenames[race])

                self.draw_dendrogram(dendrogram_vRace[race], self.clustering_vRace[race], self.BuildOrdersVersusRace[race])

        uncategorised_filepath: str = os.path.join(folder,  f'{self.Race}.{Constants.UNCATEGORISED_FILE}')
        self.save_uncategorised(uncategorised_filepath)
        

    def plot_hist(self, filename, title, build_order):  
        i: int = 0
        for build_order in build_order:
            i +=1
            hist.plot_histogram(filename.format(i), title, self.Label_Encoder, build_order)
            

    def draw_histograms(self, folder):
        
        race_filenames: Dict[int, str] = { } 
        race_titles: Dict[int, str] = { }
        
        for race in Race:
            race_filenames[race] = os.path.join(folder, self.format_histogram_filename(self.Race, race))
            race_titles[race] = "{0}v{1}".format(Race.as_string(self.Race)[0], Race.as_string(race)[0])
            
            self.plot_hist(race_filenames[race], race_titles[race], self.BuildOrdersVersusRace)
            