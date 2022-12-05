import math as m


class Player:
    def __init__(self, MAP_SIZE, TS):
        self.MAP_SIZE = MAP_SIZE
        self.x, self.y = (self.MAP_SIZE/2)*TS, (self.MAP_SIZE/2)*TS
        self.rotation = m.radians(0)
