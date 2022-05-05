from typing import TypedDict
from Constants import GameTime
from Player import Player

class Replay:
    def __init__(self, replay: TypedDict, cut_off_time: GameTime):
        self.Player1: Player = Player(replay, 1, cut_off_time)
        self.Player2: Player = Player(replay, 2, cut_off_time)