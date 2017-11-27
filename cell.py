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
        # f = g + h
        self.f = -1
        # g is the distance traveled so far from start
        self.g = -1
        # h is the heurstic value
        # think of this as an educated guess,
        # when a cell is visited, this value gets assigned
        # based on how far the cell is from the goal
        self.h = -1
        # this is used for quickly setting a cells (g)
        self.diagonal = False
        self.coordinate = Coordinate(row, col)
        self.parent = None
        # boolean to save computation time when looking for
        # cell in closed set
        self.closed = False
        # will be updated at the end of A* to allow drawing of
        # shortest path
        self.partOfPath = False

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

    # overrides equals comparison in order to compare coordinates
    def __eq__(self, other):
        if self.coordinate == other.coordinate:
            return True
        return False

    # this __ne__ function is required in Python 2.7, but not in Python 3
    # overrides not equals comparison in order to compare coordinates
    def __ne__(self, other):
        return not self.__eq__(other)
