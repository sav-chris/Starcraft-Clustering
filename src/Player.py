import datetime
from typing import TypedDict
from typing import List
import Constants
from Constants import GameTime, Race

class Player:

    def is_race_string_valid(self, race_string: str):
        return (race_string == 'Protoss') or (race_string == 'Zerg') or (race_string == 'Terran')

    def  __init__(self, replay: TypedDict, player_index: int, cut_off_time: GameTime, filter_cheap_units: bool = False):

        race_str:str = replay['players'][player_index]['race']
        if (not self.is_race_string_valid(race_str)):
            #if the race is not in english, try using 'pick_race'
            race_str:str = replay['players'][player_index]['pick_race']
        self.Name: str = replay['players'][player_index]['name']
        self.Race: Constants.Race = Race[race_str] 
        self.IsWinner: bool = replay['players'][player_index]['is_winner']
        self.BuildOrder: Constants.BUILD_ORDER_STR = self.extract_build_order(replay['players'][player_index]['buildOrder'], cut_off_time, filter_cheap_units)
        
    def is_worker_or_cheap_unit(self, name:str)->bool:
        cheap_units = ['SCV', 'PROBE', 'DRONE', 'MARINE', 'ZERGLING']
        if name.upper() in cheap_units:
            return True
        return False

    def extract_build_order(self, build_order: TypedDict, cut_off_time: GameTime, filter_cheap_units: bool = False)->Constants.BUILD_ORDER_STR:
        minutes = 0
        seconds = 0
        i: int = 0
        name: str = ''
        build_length = len(build_order)
        buildOrder = []
        while (not ((minutes >= cut_off_time.Minutes) and (seconds >= cut_off_time.Seconds))) and (i < build_length):
            build_event = build_order[i]
            time = datetime.datetime.strptime(build_event["time"], "%M:%S")
            minutes = time.minute
            seconds = time.second
            name = build_event['name']
            if (not self.is_worker_or_cheap_unit(name)) or (not filter_cheap_units):
                buildOrder.append(name)
            i = i + 1
        return buildOrder