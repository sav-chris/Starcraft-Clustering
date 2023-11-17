import Constants
from Constants import GameTime, ClusteringParams


class Hyperparameters:
    CutOffTime: GameTime = Constants.CUTOFF_TIME
    ClusteringParams: ClusteringParams = Constants.CLUST_PARAMS
    filter_cheap_units = True
    distance_metric = Constants.DistanceMetric.Levenshtien
    ComputeHistogram = False
    
    def __init__(
            self, 
            cutOffTime: GameTime=Constants.CUTOFF_TIME, 
            clusteringParams= Constants.CLUST_PARAMS, 
            filter_cheap_units:bool = True, 
            distance_metric: Constants.DistanceMetric = Constants.DistanceMetric.Levenshtien,
            ComputeHistogram: bool = False
            ):
        self.CutOffTime: GameTime = cutOffTime
        self.ClusteringParams: ClusteringParams = clusteringParams
        self.filter_cheap_units = filter_cheap_units
        self.distance_metric = distance_metric
        self.ComputeHistogram = ComputeHistogram



    


