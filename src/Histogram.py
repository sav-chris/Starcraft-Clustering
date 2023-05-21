import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from typing import Type
from Constants import BUILD_ORDER
from LabelEncoder import LabelEncoder
from typing import Tuple
from matplotlib.ticker import MaxNLocator


def calculate_histogram(label_encoder: LabelEncoder, build_order: Type[BUILD_ORDER])-> Tuple[List[str], List[int]]:
    words: List[str] = label_encoder.KnownWords
    word_indexes = label_encoder.transform(words)

    unit_names: List[int] = []
    
    frequencies: List[int] = []
    for index in word_indexes:
        unit_count: int = np.count_nonzero( build_order == index )
        if unit_count != 0:
            frequencies.append( unit_count )
            unit_names.append(index)

    return label_encoder.inverse_transform(unit_names), frequencies


def plot_histogram(filename:str, title:str, label_encoder: LabelEncoder, build_order: Type[BUILD_ORDER]):

    unit_names, frequencies = calculate_histogram(label_encoder, build_order)

    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.barh(unit_names, frequencies)
    plt.subplots_adjust(left=0.30)

    plt.xlabel('No. Produced')
    plt.ylabel('Unit type')
    plt.title(title)

    plt.savefig(filename)
    plt.close('all')

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.jensenshannon.html
# https://github.com/LucaCappelletti94/dictances
# https://en.wikipedia.org/wiki/Total_variation_distance_of_probability_measures
