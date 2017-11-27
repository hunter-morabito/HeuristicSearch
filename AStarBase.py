from abc import ABCMeta, abstractmethod
import math
import time
from coordinate import Coordinate
from cell import Cell
from grid import Grid
from binHeap import BinaryHeap
import copy

class AStarBase:
    __metaclass__ = ABCMeta

    def __init__(self,grid):

        self.REGULAR_TO_REGULAR_D = math.sqrt(2.0)
        self.REGULAR_TO_HARD_D = (math.sqrt(2.0)+math.sqrt(8.0))/2.0
        self.HARD_TO_HARD_D = math.sqrt(8.0)
        # make grid a global var
        self.grid = grid
        # holds how many nodes have been expanded
        self.nodesExpanded = 0

        self.startCell = self.grid.cells[self.grid.startCoordinate.row][self.grid.startCoordinate.col]
        self.goalCell = self.grid.cells[self.grid.goalCoordinate.row][self.grid.goalCoordinate.col]
        # current last checked Cell is the start cell
        self.lastCheckedCell = self.startCell
        # set of start to itself
        self.startCell.parent = self.startCell
        # initiize openSet using custom Binary Heap
        # this set will keep track of all the places currently seen, but not visited
        self.openSet = BinaryHeap()
        # initiize closeSet using custom Binary Heap
        self.closedSet = BinaryHeap()
        #tracks the time it takes to run the A* algo
        self.runtime = 0.0

    # TODO: Make this, and class, abstract method to be used in different A* implementation
    @abstractmethod
    def heuristic(self, start, goal):
        # calculate Euclidean distance given (x1, y1),(x2, y2) using formula:
        # math.sqrt((x2 - x1)^2 + (y2 - y1)^2)

        h = (math.sqrt( math.pow( (goal.coordinate.row - start.coordinate.row), 2)   \
                      + math.pow( (goal.coordinate.col - start.coordinate.col), 2) ) \
                      *  self.weight)
        f = start.g + h
        return f, h

    def run(self):
        runRet , self.runtime = self.process()
        # Goal was successfully found
        if runRet == 1:
            self.updatePath()
        # Goal was not successfully found
        else:
            print "Path not found"

    def process(self):
        startTime = time.time()
        self.startCell.g = 0
        self.startCell.f = self.heuristic(self.startCell,self.goalCell)
        self.startCell.h = self.heuristic(self.startCell,self.goalCell)
        self.openSet.insert(self.startCell)
        while self.openSet.size > 0:
        #for i in range (1):
            # next best option
            current = self.openSet.pop()
            self.lastCheckedCell = current

            # check if goal has been reached
            if current.coordinate == self.goalCell.coordinate:
                return 1 , (time.time() - startTime)

            # move current node from open set to 'visited' set
            current.closed = True
            self.closedSet.insert(current)

            # gather neighbor cells
            for n in self.getNeighbors(current):
                # is the current neighbor valid by not already being visited by not being in the closed list
                # and not being a blocked cell
                if n.closed == False and n.terrain != "0":
                    # this is the method call the implements all the different terrain changes
                    tempG = current.g + self.getNeighborG(current,n)
                    #neighbor not in open set if g is never set
                    if n.g != -1:
                        # self.openSet.insert(n)
                        if tempG >= n.g:
                            # not a better path
                            continue
                        else:
                            # neighbor needs to be replaced
                            self.openSet.remove(n)
                            self.nodesExpanded -= 1
                    # can be used to showcase fringe
                    # n.color = "yellow"
                    # update neighbor.g
                    n.g = tempG
                    # update total A* score using given g and heuristic
                    n.f, n.h = self.heuristic(n,self.goalCell)
                    # update neighbors parent to the current node
                    n.parent = current

                    # neighbor has not been seen yet
                    self.openSet.insert(n)
                    self.nodesExpanded += 1

        # goal was never reached
        return -1 , (time.time() - startTime)

    # TODO: consider makeing dictonary instead
    # returns the speed it takes to get from current cell to neighbor,
    # while taking terrain into account
    def getNeighborG(self, current, n):
        distance = 0.0
        # REGULAR to REGULAR
        if (current.terrain == "1" or current.terrain == "a") and (n.terrain == "1" or n.terrain == "a"): \
            # moving diagonally
            if n.diagonal:
                distance = self.REGULAR_TO_REGULAR_D
            # moving horiz/vert
            else:
                distance = 1.0
        # REGULAR to HARD
        elif   ((current.terrain == "1" or current.terrain == "a") and (n.terrain == "2" or n.terrain == "b")) \
            or ((current.terrain == "2" or current.terrain == "b") and (n.terrain == "1" or n.terrain == "a")):
                if n.diagonal:
                    # formula is:
                    #    math.sqrt(2) + math.sqrt(8)
                    #    -----------------
                    #            2
                    distance = self.REGULAR_TO_HARD_D
                else:
                    distance = 1.5
        # HARD to HARD
        elif (current.terrain == "2" or current.terrain == "b") and (n.terrain == "2" or n.terrain == "b"):
            # moving diagonally
            if n.diagonal:
                distance = self.HARD_TO_HARD_D
            else:
                distance = 2.0
        # check to see if cells are moving horiz/vert across highways
        if (current.terrain == "a" or current.terrain == "b") and (n.terrain == "a" or n.terrain=="b"):
            if not n.diagonal:
                distance = distance / 4.0
        return distance

    # A* Helper methods
    def getNeighbors(self,cell):
        neighbors = []
        # neighbors are labeled as the following:
        #         N1 N2 N3
        #         N8 ## N4
        #         N7 N6 N5
        # Add N1 // Diagonal
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row - 1,cell.coordinate.col - 1)):
            n = self.grid.cells[cell.coordinate.row - 1][cell.coordinate.col - 1]
            n.diagonal = True
            neighbors.append(n)
        # Add N2
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row - 1,cell.coordinate.col)):
            n = self.grid.cells[cell.coordinate.row - 1][cell.coordinate.col]
            n.diagonal = False
            neighbors.append(n)
        # Add N3 // Diagonal
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row - 1,cell.coordinate.col + 1)):
            n = self.grid.cells[cell.coordinate.row - 1][cell.coordinate.col + 1]
            n.diagonal = True
            neighbors.append(n)
        # Add N4
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row,cell.coordinate.col + 1)):
             n = self.grid.cells[cell.coordinate.row][cell.coordinate.col + 1]
             n.diagonal = False
             neighbors.append(n)
        # Add N5 // Diagonal
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row + 1,cell.coordinate.col + 1)):
            n = self.grid.cells[cell.coordinate.row + 1][cell.coordinate.col + 1]
            n.diagonal = True
            neighbors.append(n)
        # Add N6
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row + 1,cell.coordinate.col)):
             n = self.grid.cells[cell.coordinate.row + 1][cell.coordinate.col]
             n.diagonal = False
             neighbors.append(n)
        # Add N7 // Diagonal
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row + 1,cell.coordinate.col - 1)):
             n = self.grid.cells[cell.coordinate.row + 1][cell.coordinate.col - 1]
             n.diagonal = True
             neighbors.append(n)
        # Add N8
        if self.grid.verifyCoordInBounds(Coordinate(cell.coordinate.row,cell.coordinate.col - 1)):
             n = self.grid.cells[cell.coordinate.row][cell.coordinate.col - 1]
             n.diagonal = False
             neighbors.append(n)
        return neighbors

    def updatePath(self):
        self.goalCell.color = "red"
        self.startCell.color = "orange"
        current = self.goalCell.parent
        while current.coordinate != self.startCell.coordinate:
            current.partOfPath = True
            #current.color = "green"
            current = current.parent
