from astarbase import AStarBase
import math

class AStarEuclidean(AStarBase):
    def __init__(self,grid,weight):
        super(AStarEuclidean,self).__init__(grid)
        self.weight = weight

    # this heuristinc is the Euclidean distance of the current and goal cell * given weight
    # calculate Euclidean distance given (x1, y1),(x2, y2) using formula:
    # math.sqrt((x2 - x1)^2 + (y2 - y1)^2)
    def heuristic(self,start,goal):
        h = (math.sqrt( math.pow( (goal.coordinate.row - start.coordinate.row), 2)   \
                      + math.pow( (goal.coordinate.col - start.coordinate.col), 2) ) \
                      *  self.weight)
        f = start.g + h
        return f, h

class AStarManhattan(AStarBase):
    def __init__(self,grid,weight):
        super(AStarManhattan,self).__init__(grid)
        self.weight = weight

    def heuristic(self,start,goal):
        dx = math.fabs(start.coordinate.row - goal.coordinate.row)
        dy = math.fabs(start.coordinate.col - goal.coordinate.col)
        h = ((dx+dy) * self.weight)
        f = start.g + h
        return f, h

class AStarTieBreak(AStarBase):
    def __init__(self,grid,weight):
        super(AStarTieBreak,self).__init__(grid)
        self.weight = weight
        self.scale = 1
    def heuristic(self,start,goal):
        # scale increases as called by .1%
        # i.e min cost of takeing a step/expected max length
        self.scale *= (1.0 + 0.015)
        h = (self.scale * self.weight)
        f = start.g * h
        return f, h

class AStarOctile(AStarBase):
    def __init__(self,grid,weight):
        super(AStarOctile,self).__init__(grid)
        self.weight = weight


    #returns octile heuristic
    def heuristic(self,start,goal):
        dx = math.fabs(start.coordinate.row - goal.coordinate.row)
        dy = math.fabs(start.coordinate.col - goal.coordinate.col)
        maxum = dx
        minum = dy
        if dx < dy:
            maxum = dy
            minum = dx
        h = ((maxum + (math.sqrt(2)-1) * minum ) * self.weight)
        f = start.g + h
        return f, h

class AStarUniform(AStarBase):
    def __init__(self,grid,weight):
        super(AStarUniform,self).__init__(grid)
        self.weight = weight
    def heuristic(self,start,goal):
        return start.g, 0
