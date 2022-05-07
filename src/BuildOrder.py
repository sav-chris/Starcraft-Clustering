import Constants
from typing import List
from typing import Type
import numpy.typing as npt
import numpy as np

class BuildOrder:

    def __init__(self, build_order: Constants.BUILD_ORDER):
        BuildOrder: Constants.BUILD_ORDER = build_order

    def convert_build_order_to_numpy_array(self, build_order: List[Constants.BUILD_ORDER])->npt.NDArray:
        build_order_array: npt.NDArray = np.array([])
        build_order_array =  [ np.asarray(bo) for bo in build_order]

    def convert_build_order_to_numpy_array(self):
        return self.convert_build_order_to_numpy_array(self.BuildOrder)

        

    
    