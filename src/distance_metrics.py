from typing import List
from typing import Type
from typing import Callable
from rapidfuzz.distance import Levenshtein
import numpy.typing as npt
from scipy.spatial import distance
import numpy as np
from Constants import BUILD_ORDER
from typing import Tuple
from LabelEncoder import LabelEncoder
from scipy.stats import entropy

DistMetric = Callable[[Type[BUILD_ORDER], Type[BUILD_ORDER]], int]


def levenshtein_distance_metric(left:  Type[BUILD_ORDER], right:  Type[BUILD_ORDER])->int:
    left_chars = [chr(letter) for letter in left] 
    right_chars = [chr(letter) for letter in right]
    return Levenshtein.distance(left_chars, right_chars)


def create_histogram_jensen_shannon_distance_metric(label_encoder: LabelEncoder)->DistMetric:
    def dist_metric(left: Type[BUILD_ORDER], right: Type[BUILD_ORDER])->int:
        left_hist : List[int] = calculate_histogram(label_encoder, left) 
        right_hist: List[int] = calculate_histogram(label_encoder, right) 
        return distance.jensenshannon(left_hist, right_hist)

    return dist_metric


def create_histogram_kullback_leibler_distance_metric(label_encoder: LabelEncoder)->DistMetric:
    def dist_metric(left: Type[BUILD_ORDER], right: Type[BUILD_ORDER])->int:
        left_hist : List[int] = calculate_histogram(label_encoder, left) 
        right_hist: List[int] = calculate_histogram(label_encoder, right) 
        return entropy(left_hist, right_hist)

    return dist_metric

def calculate_histogram(label_encoder: LabelEncoder, build_order: Type[BUILD_ORDER])-> List[int]:
    words: List[str] = label_encoder.KnownWords
    word_indexes = label_encoder.transform(words)
    
    bo = np.array(build_order)
    frequencies: List[int] = []
    for index in word_indexes:
        unit_count: int = np.count_nonzero( bo == index )
        frequencies.append( unit_count )
    
    return frequencies


