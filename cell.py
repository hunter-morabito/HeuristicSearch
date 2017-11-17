from coordinate import Coordinate

class Cell:

    def __init__(self, row, col):
        self.color = "white"
        #difficulty
        self.diff = 1
        self.coordinate = Coordinate(row, col)

    #change difficulty also requires an update in color
    def setDiff(self, diff):
        self.diff = diff
        if self.diff == 0:
            self.color = "black"
        elif self.diff == 1:
            self.color = "white"
        elif self.diff == 2:
            #color is bronze gold
            self.color = "#C9AE5D"
