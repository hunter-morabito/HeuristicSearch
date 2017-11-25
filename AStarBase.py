from abc import ABCMeta
from binHeap import BinaryHeap

class AStarBase:
    __metaclass__ = ABCMeta

    def __init__(self,grid):
        # make grid a global var
        self.grid = grid
        self.startCell = self.grid.cells[self.grid.startCoordinate.row][self.grid.startCoordinate.col]
        self.goalCell = self.grid.cells[self.grid.goalCoordinate.row][self.grid.goalCoordinate.col]
        # current last checked Cell is the start cell
        self.lastCheckedCell = self.startCell
        # set of start to itself
        self.startCell.parent = self.startCell
        # initiize openSet using custom Binary Heap
        # this set will keep track of all the places currently seen, but not visited
        self.openSet = BinaryHeap()
        # insert start cell onto the heap
        self.openSet.insert(self.startCell)
        # initiize closeSet using custom Binary Heap
        self.closedSet = BinaryHeap()
        self.run()


    # TODO: Make this, and class, abstract method to be used in different A* implementation
    def heuristic(self, start, goal):
        # calculate Euclidean distance given (x1, y1),(x2, y2) using formula:
        # sqrt((x2 - x1)^2 + (y2 - y1)^2)
        return math.sqrt( math.pow( (goal.coordinate.row - start.coordinate.row), 2) \
                       +  math.pow( (goal.coordinate.col - start.coordinate.col), 2) )


    # TODO: swap getNeighbors() from grid.py to astarbase.py and use diagonal check
    # returns the speed it takes to get from current cell to another,
    # while taking terrain into account
    def getNeighborHeuristic(self, current, n):
        distance = 0
        #check for horizontal or diagonal move
        if    n.coordinate.row == current.coordinate.row - 1 and  n.coordinate.col == current.coordinate.row - 1 \
           or n.coordinate.row == current.coordinate.row - 1 and  n.coordinate.col == current.coordinate.row + 1 \
           or n.coordinate.row == current.coordinate.row + 1 and  n.coordinate.col == current.coordinate.row - 1 \
           or n.coordinate.row == current.coordinate.row + 1 and  n.coordinate.col == current.coordinate.row + 1:
           print "is diagional"
        return distance

    def run(self):
        # while self.openSet.size > 0:
        for i in range (1):
            # next best option
            current = self.openSet.pop()
            self.lastCheckedCell = current

            # check if goal has been reached
            if current == self.goalCell:
                print "done"
                return 1

            # move current node from open set to 'visited' set
            self.closedSet.insert(current)

            # gather neighbor cells
            for n in self.grid.getNeighbors(current):
                # is the current neighbor valid by not already being visited and
                # not being a blocked cell
                if not self.closedSet.contains(n) and n.terrain != "0":
                    # this is the method call the implements all the different terrain changes
                    tempG = current.g + self.getNeighborHeuristic(current,n)
