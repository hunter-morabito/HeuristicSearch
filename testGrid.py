import math
from cell import Cell
from coordinate import Coordinate
from gridui import GridUI
from astarbase import AStarBase
import random

class TESTGRID:
    def __init__(self):
        self.numrows = 100
        self.numcols = 100
        self.startCoordinate = Coordinate(0,self.numcols - 1)
        self.goalCoordinate = Coordinate(self.numrows - 1,self.numcols - 1)
        self.cells = [[Cell(i,j) for j in range(self.numcols)] for i in range(self.numrows)]
        self.setBlockedTerrain(30)

    def setBlockedTerrain(self, percentofblocked):
        #get 20% of total cells
        blockedTotal = int((self.numrows * self.numcols) * (percentofblocked/100.0))
        #blocked cells counter
        blocked = 0
        #holds blocked coordinates
        blockedList = []
        #iterate until 20% of cells are blocked
        while blocked != blockedTotal:
            randCoord = self.getRandomCoord()
            #check to verify cell is not a highway already
            if self.cells[randCoord.row][randCoord.col].terrain != "a" and self.cells[randCoord.row][randCoord.col].terrain != "b":
                #add to list and increment counter
                blockedList.append(randCoord)
                blocked += 1
        #change cell terrain at collected coordinates
        self.changeTerrain(blockedList, "0")

    def changeTerrain(self, coordinateList, terrain):
        for coord in coordinateList:
            cell = self.cells[coord.row][coord.col]
            if terrain == "0":
                cell.setTerrain("0")
            elif terrain == "1":
                cell.setTerrain("1")
            elif terrain == "2":
                cell.setTerrain("2")
            elif terrain == "highway":
                if cell.terrain == "1":
                    cell.setTerrain("a")
                elif cell.terrain == "2":
                    cell.setTerrain("b")

    def getRandomCoord(self):
        #random legal row
        randrow = random.randint(0, self.numrows - 1)
        #random legal col
        randcol = random.randint(0, self.numcols - 1)
        return Coordinate(randrow, randcol)

    # check that Coordinate is not out of bounds
    def verifyCoordInBounds(self, coord):
        #set base to false in case of logic failure
        inBounds = False
        #check bounds
        if coord.row >= 0 and coord.row < self.numrows and coord.col >= 0 and coord.col < self.numcols:
            inBounds = True
        return inBounds

    # gets Cell color
    def getCColor(self,row,col):
        return self.cells[row][col].color

def main():
    grid = AStarBase(TESTGRID())

    GridUI(grid.grid).mainloop()


if __name__ == "__main__":
    main()
