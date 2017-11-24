# enumeration not natively supported in Python 2.7
# from enum import Enum
#
# class Terrain(enum):
#     BLOCKED = 0
#     REGULAR = 1
#     HARD = 2
#     HIGHWAY = "a"
#     HARDHIGH = "b"
from coordinate import Coordinate


class Cell:
    def __init__(self, row, col):
        self.color = "white"
        # difficulty
        self.terrain = "1"
        self.coordinate = Coordinate(row, col)

    # change difficulty also requires an update in color
    def setTerrain(self, terrain):
        self.terrain = terrain
        if self.terrain == "0":         # BLOCKED
            self.color = "dark grey"
        elif self.terrain == "1":       # REGULAR
            self.color = "white"
        elif self.terrain == "2":       # HARD
            # color is bronze gold
            self.color = "#C9AE5D"
        elif self.terrain == "a":       # REGULAR HIGHWAY
            # color is a shade of blue
            self.color = "#0059ff"
        elif self.terrain == "b":       # HARD HIGHWAY
            # color is a darker shade of purple
            self.color = "#41008c"
