import Constants
from Constants import GameTime, ClusteringParams


class Hyperparameters:
    
    def __init__(
            self, 
            cutOffTime: GameTime=Constants.CUTOFF_TIME, 
            clusteringParams= Constants.CLUST_PARAMS, 
            filter_cheap_units:bool = True, 
            distance_metric: Constants.DistanceMetric = Constants.DistanceMetric.Levenshtien
            ):
        self.CutOffTime: GameTime = cutOffTime
        self.ClusteringParams: ClusteringParams = clusteringParams
        self.filter_cheap_units = filter_cheap_units
        self.distance_metric = distance_metric



    


