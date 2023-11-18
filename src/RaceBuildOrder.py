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
        # typing.Dict[str, str]
        #Dict[str, List[BUILD_ORDER]]
        self.BuildOrdersVersusRace: Dict[int, List[BUILD_ORDER]] = {}

        #self.VersusTerran : Type[List[BUILD_ORDER]] = []
        #self.VersusZerg   : Type[List[BUILD_ORDER]] = []
        #self.VersusProtoss: Type[List[BUILD_ORDER]] = []

        self.Label_Encoder: LabelEncoder = LabelEncoder()

        self.RaceDistanceMatrix: Dict[int, np.array] = {}

        #self.TerranDistanceMatrix: np.array = np.zeros(0)
        #self.ZergDistanceMatrix: np.array = np.zeros(0)
        #self.ProtossDistanceMatrix: np.array = np.zeros(0)
        
        self.Race = Race

        self.clustering_vRace : Dict[int, OPTICS] = {}
        #self.clustering_vT = None
        #self.clustering_vZ = None
        #self.clustering_vP = None

        for race in Constants.Race:
            self.BuildOrdersVersusRace[race] = []
            #self.RaceDistanceMatrix[race] = np.zeros(0)




    def count_uncategorised(self, optics: OPTICS)->int:
        counts:collections.Counter = collections.Counter(optics.labels_)
        return counts[-1]

    def save_uncategorised(self, filepath:str):
        print(self.Race)
        Race_Uncategorised : Dict[int, int] = {}
        for race in self.clustering_vRace.keys():
            print(f'Uncategorised { Race.as_string(race) } Builds: {Race_Uncategorised[race]}')
            Race_Uncategorised[race] = self.count_uncategorised(self.clustering_vRace[self.Race]) 
        
        #T_Uncategorised:int = self.count_uncategorised(self.clustering_vT)
        #Z_Uncategorised:int = self.count_uncategorised(self.clustering_vZ)
        #P_Uncategorised:int = self.count_uncategorised(self.clustering_vP)
        #print(self.Race)
        #print(f'Uncategorised Terran Builds: {T_Uncategorised}')
        #print(f'Uncategorised Zerg Builds: {Z_Uncategorised}')
        #print(f'Uncategorised Protoss Builds: {P_Uncategorised}')

        txt_uncategorised:str = f'Race: {self.Race} \n'
        for race in self.clustering_vRace.keys():
            txt_uncategorised = txt_uncategorised + f'Uncategorised { Race.as_string(race) } Builds: {Race_Uncategorised[race]} \n'

        #txt_uncategorised = txt_uncategorised + f'Uncategorised Terran Builds: {T_Uncategorised} \n'
        #txt_uncategorised = txt_uncategorised + f'Uncategorised Zerg Builds: {Z_Uncategorised} \n'
        #txt_uncategorised = txt_uncategorised + f'Uncategorised Protoss Builds: {P_Uncategorised}'

        with open(filepath, "w") as text_file:
            text_file.write(txt_uncategorised)

    def add_build_order(self, bo : BUILD_ORDER_STR, bos: List[BUILD_ORDER_STR]):
        bos.append(self.Label_Encoder.transform(bo))


    def add_race_build_order(self, race: Race, bo : BUILD_ORDER_STR):
        self.add_build_order(bo, self.BuildOrdersVersusRace[race])
    

    #def add_terran_build_order(self, bo : BUILD_ORDER_STR):
    #    self.add_build_order(bo, self.VersusTerran)

    #def add_zerg_build_order(self, bo : BUILD_ORDER_STR):
    #    self.add_build_order(bo, self.VersusZerg)

    #def add_protoss_build_order(self, bo : BUILD_ORDER_STR):
    #    self.add_build_order(bo, self.VersusProtoss)


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

        #tLength = len(self.VersusTerran)
        #zLength = len(self.VersusZerg)
        #pLength = len(self.VersusProtoss)
        #self.TerranDistanceMatrix  = np.zeros((tLength, tLength)) 
        #self.ZergDistanceMatrix    = np.zeros((zLength, zLength)) 
        #self.ProtossDistanceMatrix = np.zeros((pLength, pLength)) 
        #self.compute_distance_matrix(self.TerranDistanceMatrix,  self.VersusTerran,  distance_metric)
        #self.compute_distance_matrix(self.ZergDistanceMatrix,    self.VersusZerg,    distance_metric)
        #self.compute_distance_matrix(self.ProtossDistanceMatrix, self.VersusProtoss, distance_metric)

        if verbose:
            print(self.Race)
            for race in self.RaceDistanceMatrix.keys():
                print(f'Versus { Race.as_string(race) }: ')
                print(self.RaceDistanceMatrix[race])
            #print('Versus Terran: ')
            #print(self.TerranDistanceMatrix)
            #print('Versus Zerg: ')
            #print(self.ZergDistanceMatrix)
            #print('Versus Protoss: ')
            #print(self.ProtossDistanceMatrix)


    def decode_labels(self, build_order: BUILD_ORDER)->BUILD_ORDER_STR:
        return self.Label_Encoder.inverse_transform(build_order)
    
    def format_RvR(self, this_race : Race, vs_race: Race)->str:
        # TO DO: Does this belong somewhere else?
        return Constants.RACE_V_RACE.format(Race.as_string(this_race).upper(), Race.as_string(vs_race)[0]) 

    def construct_paths(self, directory: str)->Dict[int, str]:
        paths: Dict[int, str] = {}
        for race in self.BuildOrdersVersusRace.keys():
            #filename: str = Constants.RACE_V_RACE.format(Race.as_string(self.Race).upper(), Race.as_string(race)[0]) 
            filename: str = self.format_RvR(self.Race, race) 
            path: str = os.path.join(directory, filename)
            paths[race] = path

        return paths
        #VT_NPY: str = ''
        #VZ_NPY: str = ''
        #VP_NPY: str = ''
        #match self.Race:
        #    case Race.Zerg:
        #        VT_NPY = Constants.ZERG_VT
        #        VZ_NPY = Constants.ZERG_VZ
        #        VP_NPY = Constants.ZERG_VP
        #    case Race.Protoss:
        #        VT_NPY = Constants.PROTOSS_VT
        #        VZ_NPY = Constants.PROTOSS_VZ
        #        VP_NPY = Constants.PROTOSS_VP
        #    case Race.Terran:
        #        VT_NPY = Constants.TERRAN_VT
        #        VZ_NPY = Constants.TERRAN_VZ
        #        VP_NPY = Constants.TERRAN_VP

        #VT_NPY = os.path.join(directory, VT_NPY)
        #VZ_NPY = os.path.join(directory, VZ_NPY)
        #VP_NPY = os.path.join(directory, VP_NPY)
        #return VT_NPY, VZ_NPY, VP_NPY

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

        #VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        #self.save_build_order_file(VT_NPY, self.VersusTerran)
        #self.save_build_order_file(VZ_NPY, self.VersusZerg)
        #self.save_build_order_file(VP_NPY, self.VersusProtoss)
        # Save Labels
        #match self.Race:
        #    case Race.Terran:
        #        self.Label_Encoder.save_to_file(os.path.join(directory, Constants.LabelEncoderTerran))
        #    case Race.Zerg:
        #        self.Label_Encoder.save_to_file(os.path.join(directory, Constants.LabelEncoderZerg))
        #    case Race.Protoss:
        #        self.Label_Encoder.save_to_file(os.path.join(directory, Constants.LabelEncoderProtoss))

    def load_build_orders(self, directory:str)->None:
        paths: Dict[int, str] = self.construct_paths(directory)
        for race in paths.keys():
            if os.path.exists(paths[race]):
                self.load_build_order_file(paths[race], self.BuildOrdersVersusRace[race])

        label_encoder: str = os.path.join(directory, Constants.LabelEncoderRace.format(Race.as_string(self.Race)))
        if os.path.exists(label_encoder):
            self.Label_Encoder.load_from_file(label_encoder)

        #VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        #self.load_build_order_file(VT_NPY, self.VersusTerran)
        #self.load_build_order_file(VZ_NPY, self.VersusZerg)
        #self.load_build_order_file(VP_NPY, self.VersusProtoss)
        # load Labels
        #match self.Race:
        #    case Race.Terran:
        #        self.Label_Encoder.load_from_file(os.path.join(directory, Constants.LabelEncoderTerran))
        #    case Race.Zerg:
        #        self.Label_Encoder.load_from_file(os.path.join(directory, Constants.LabelEncoderZerg))
        #    case Race.Protoss:
        #        self.Label_Encoder.load_from_file(os.path.join(directory, Constants.LabelEncoderProtoss))


    def save_distance_matricies(self, directory: str)->None:
        paths: Dict[int, str] = self.construct_paths(directory)
        for race in paths.keys():
            np.save(paths[race], self.RaceDistanceMatrix[race])

        #VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        #np.save(VT_NPY, self.TerranDistanceMatrix)
        #np.save(VZ_NPY, self.ZergDistanceMatrix)
        #np.save(VP_NPY, self.ProtossDistanceMatrix)

    def load_distance_matricies(self, directory:str)->None:
        paths: Dict[int, str] = self.construct_paths(directory)
        for race in paths.keys():
            if os.path.exists(paths[race]):
                self.RaceDistanceMatrix[race] = np.load(paths[race])

        #VT_NPY, VZ_NPY, VP_NPY = self.construct_paths(directory)
        #self.TerranDistanceMatrix  = np.load( VT_NPY)
        #self.ZergDistanceMatrix    = np.load( VZ_NPY)
        #self.ProtossDistanceMatrix = np.load( VP_NPY)

    def OPTICS_clustering(self, hyperparameters: Hyperparameters):
        
        for race in Race:
            if race in self.RaceDistanceMatrix:
                self.clustering_vRace[race] = OPTICS(eps=hyperparameters.ClusteringParams.epsilon, min_samples=hyperparameters.ClusteringParams.min_samples, metric='precomputed').fit(self.RaceDistanceMatrix[race])

        return self.clustering_vRace
        
        #self.clustering_vT = OPTICS(eps=hyperparameters.ClusteringParams.epsilon, min_samples=hyperparameters.ClusteringParams.min_samples, metric='precomputed').fit(self.TerranDistanceMatrix)
        #self.clustering_vZ = OPTICS(eps=hyperparameters.ClusteringParams.epsilon, min_samples=hyperparameters.ClusteringParams.min_samples, metric='precomputed').fit(self.ZergDistanceMatrix)
        #self.clustering_vP = OPTICS(eps=hyperparameters.ClusteringParams.epsilon, min_samples=hyperparameters.ClusteringParams.min_samples, metric='precomputed').fit(self.ProtossDistanceMatrix)
        #return self.clustering_vT, self.clustering_vZ, self.clustering_vP


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
        return Constants.RACE_VR_HIST.format(race1_str, race1_str[0], race2_str[0])
            

    def draw_clustering(self, folder):
        
        dendrogram_vRace: Dict[int, Dendrogram] =  {}
        race_filenames: Dict[int, str] = { } 
        
        for race in Race:
            race_filenames[race] = os.path.join(folder, self.format_graphviz_filename(self.race, race))
            dendrogram_vRace[race] = Dendrogram("Dendrogram", race_filenames[race])

            self.draw_dendrogram(dendrogram_vRace[race], self.clustering_vRace[race], self.BuildOrdersVersusRace[race])

        uncategorised_filepath: str = os.path.join(folder,  f'{self.Race}.{Constants.UNCATEGORISED_FILE}')
        self.save_uncategorised(uncategorised_filepath)
        
        #race_to_filenames: Dict[int, Tuple[str, str, str]] = {
        #    Race.Terran:  (Constants.TERRAN_VT_GV,  Constants.TERRAN_VZ_GV,  Constants.TERRAN_VP_GV),
        #    Race.Zerg:    (Constants.ZERG_VT_GV,    Constants.ZERG_VZ_GV,    Constants.ZERG_VP_GV),
        #    Race.Protoss: (Constants.PROTOSS_VT_GV, Constants.PROTOSS_VZ_GV, Constants.PROTOSS_VP_GV)
        #}
        #filename_vT, filename_vZ, filename_vP = race_to_filenames[self.Race]

        

        #match self.Race:
        #    case Race.Terran:
        #        filename_vT = Constants.TERRAN_VT_GV
        #        filename_vZ = Constants.TERRAN_VZ_GV
        #        filename_vP = Constants.TERRAN_VP_GV
        #    case Race.Zerg:
        #        filename_vT = Constants.ZERG_VT_GV
        #        filename_vZ = Constants.ZERG_VZ_GV
        #        filename_vP = Constants.ZERG_VP_GV
        #    case Race.Protoss:
        #        filename_vT = Constants.PROTOSS_VT_GV
        #        filename_vZ = Constants.PROTOSS_VZ_GV
        #        filename_vP = Constants.PROTOSS_VP_GV
 
        #filename_vT = os.path.join(folder, filename_vT)
        #filename_vZ = os.path.join(folder, filename_vZ)
        #filename_vP = os.path.join(folder, filename_vP)
        
        #dendrogram_vT: Dendrogram = Dendrogram("Dendrogram", filename_vT)
        #dendrogram_vZ: Dendrogram = Dendrogram("Dendrogram", filename_vZ)
        #dendrogram_vP: Dendrogram = Dendrogram("Dendrogram", filename_vP)

        #self.draw_dendrogram(dendrogram_vT, self.clustering_vT, self.VersusTerran)
        #self.draw_dendrogram(dendrogram_vZ, self.clustering_vZ, self.VersusZerg)
        #self.draw_dendrogram(dendrogram_vP, self.clustering_vP, self.VersusProtoss)

        #uncategorised_filepath: str = os.path.join(folder,  f'{self.Race}.{Constants.UNCATEGORISED_FILE}')
        #self.save_uncategorised(uncategorised_filepath)

    def plot_hist(self, filename, title, build_order):  
        i: int = 0
        for build_order in build_order:
            i +=1
            hist.plot_histogram(filename.format(i), title, self.Label_Encoder, build_order)
            

    def draw_histograms(self, folder):
        
        race_filenames: Dict[int, str] = { } 
        race_titles: Dict[int, str] = { }
        
        for race in Race:
            race_filenames[race] = os.path.join(folder, self.format_histogram_filename(self.race, race))
            race_titles[race] = "{0}v{1}".format(Race.as_string(self.race)[0], Race.as_string(race)[0])
            
            self.plot_hist(race_filenames[race], race_titles[race], self.BuildOrdersVersusRace)
            
        #titleT:str = ""
        #titleZ:str = ""
        #titleP:str = ""
        #match self.Race:
        #    case Race.Terran:
        #        filename_vT = Constants.TERRAN_VT_HIST
        #        filename_vZ = Constants.TERRAN_VZ_HIST
        #        filename_vP = Constants.TERRAN_VP_HIST
        #        titleT = "TvT"
        #        titleZ = "TvZ"
        #        titleP = "TvP"
        #    case Race.Zerg:
        #        filename_vT = Constants.ZERG_VT_HIST
        #        filename_vZ = Constants.ZERG_VZ_HIST
        #        filename_vP = Constants.ZERG_VP_HIST
        #        titleT = "ZvT"
        #        titleZ = "ZvZ"
        #        titleP = "ZvP"
        #    case Race.Protoss:
        #        filename_vT = Constants.PROTOSS_VT_HIST
        #        filename_vZ = Constants.PROTOSS_VZ_HIST
        #        filename_vP = Constants.PROTOSS_VP_HIST
        #        titleT = "PvT"
        #        titleZ = "PvZ"
        #        titleP = "PvP"
 
        #filename_vT = os.path.join(folder, filename_vT)
        #filename_vZ = os.path.join(folder, filename_vZ)
        #filename_vP = os.path.join(folder, filename_vP)
        
        #self.plot_hist(filename_vT, titleT, self.VersusTerran)
        #self.plot_hist(filename_vZ, titleZ, self.VersusZerg)
        #self.plot_hist(filename_vP, titleP, self.VersusProtoss)

        #uncategorised_filepath: str = os.path.join(folder,  f'{self.Race}.{Constants.UNCATEGORISED_FILE}')


