class Coordinate:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    # returns a string giving row and col; used for file output
    def __repr__(self):
        return "%d %d" % (self.row , self.col)

    # returns a more detailed string about Coordinates
    def __str__(self):
        return "Row: %d,  Col: %d" % (self.row , self.col)

    # overrides equals comparison in order to compare coordinates
    def __eq__(self, other):
        if isinstance(self , other.__class__):
            return self.__dict__ == other.__dict__
        return False

    # this __ne__ function is required in Python 2.7, but not in Python 3
    # overrides not equals comparison in order to compare coordinates
    def __ne__(self, other):
        return not self.__eq__(other)
