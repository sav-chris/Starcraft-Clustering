import glob
import spawningtool.parser
import datetime
from sklearn.preprocessing import LabelEncoder
from numpy import array
import numpy.typing as npt

#import textdistance
#from leven import levenshtein       
import numpy as np
from sklearn.cluster import dbscan
from sklearn.cluster import OPTICS

NDArrayInt = npt.NDArray[np.int_]

END_TIME_MINUTES: int = 4
END_TIME_SECONDS: int = 0

data_dir_filter: str = "../Data/**/*.SC2Replay"

data_files = glob.glob(data_dir_filter,  recursive=True)

zerg_label_encoder = LabelEncoder()
zerg_label_encoder.fit(array([])) # initialise label encoder

terran_label_encoder = LabelEncoder()
terran_label_encoder.fit(array([]))

protoss_label_encoder = LabelEncoder()
protoss_label_encoder.fit(array([]))


#result_replay['players'][1]['race']
#result_replay['players'][1]['is_winner']

#result_replay = spawningtool.parser.parse_replay(data_files[0])
#p1_build_order = result_replay['players'][1]['buildOrder']
#p2_build_order = result_replay['players'][2]['buildOrder']


class BuildEvent:
    Minutes: int = 0
    Seconds: int = 0
    Name: str

    def __init__(self, minutes, seconds, name):
        self.Minutes = minutes
        self.Seconds = seconds
        self.Name = name


def extract_build_order(build_order):
    minutes = 0
    seconds = 0
    i: int = 0
    name: str = ''
    build_length = len(build_order)
    buildOrder = []
    while (not ((minutes >= END_TIME_MINUTES) and (seconds >= END_TIME_SECONDS))) and (i < build_length):
        build_event = build_order[i]
        time = datetime.datetime.strptime(build_event["time"], "%M:%S")
        minutes = time.minute
        seconds = time.second
        name = build_event['name']
        print(", ".join([build_event['time'], build_event['name']]))
        buildOrder.append(BuildEvent(minutes, seconds, name))
        i = i + 1
    return buildOrder


#print(result_replay['players'][1]['race'])
#print(result_replay['players'][1]['is_winner'])
#p1_vector = extract_build_order(p1_build_order)
#p2_vector = extract_build_order(p2_build_order)
#print('')

def levenshtein_distance(x:NDArrayInt, y: NDArrayInt)->int:
    if (x.size == 0):
        return y.size

    if (y.size == 0):
        return x.size

    if(x[0] == y[0]):
        return levenshtein_distance(x[1:], y[1:])

    #Deletion Insertion Substitution
    d = min(levenshtein_distance(x[1:], y), levenshtein_distance(x, y[1:]) )
    d = min(d, levenshtein_distance(x[1:], y[1:]))
    return 1 + d



def similarity(x, y):
    pass



for data_file in data_files:


    result_replay = spawningtool.parser.parse_replay(data_file)

    p1_label_enoder: LabelEncoder = zerg_label_encoder
    p2_label_enoder: LabelEncoder = zerg_label_encoder
    
    p1_race = result_replay['players'][1]['race']
    p2_race = result_replay['players'][2]['race']

    if p1_race == 'Terran':
        p1_label_enoder = terran_label_encoder
    if p1_race == 'Protoss':
        p1_label_enoder = protoss_label_encoder
    
    if p2_race == 'Terran':
        p2_label_enoder = terran_label_encoder
    if p2_race == 'Protoss':
        p2_label_enoder = protoss_label_encoder

    p1_build_order = result_replay['players'][1]['buildOrder']
    p2_build_order = result_replay['players'][2]['buildOrder']

     


    p1_build_order = [event['name'] for event in p1_build_order]
    p2_build_order = [event['name'] for event in p2_build_order]

        
    #Build Labels
    p1_label_enoder.fit(np.append(p1_label_enoder.classes_, array(p1_build_order)))
    p2_label_enoder.fit(np.append(p2_label_enoder.classes_, array(p2_build_order)))



    p1_build_order_numeric = label_encoder.transform(array(p1_build_order))
    p2_build_order_numeric = label_encoder.transform(array(p2_build_order))

    reduced_dataset = OPTICS(metric=similarity).fit(dataset)
    
    dist = ld(p1_build_order_numeric, p2_build_order_numeric)

    
    
    #dist = levenshtein(p1_build_order_numeric, p2_build_order_numeric)
    print('')
    



    




