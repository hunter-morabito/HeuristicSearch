from cell import Cell
from coordinate import Coordinate
import random

class Grid:
    def __init__(self,numrows,numcols):
        #num of rows
        self.numrows = numrows
        #num of columns
        self.numcols = numcols
        #all cells given in clean
        self.cells = [[Cell(i,j) for j in range(numcols)] for i in range(numrows)]

    def setHardCells(self):
        #iterate to find 8 center cells
        for i in range(8):
            #get center cell coordinate
            centerCoord = self.getRandomCoord()
            #iterate through 31 x 31 block of cells around center
            #start at row 15 up from center, end 15 below center
            for irow in range (centerCoord.row - 15 , centerCoord.row + 15):
                #start at col 15 left of center, end 15 right of center
                for icol in range(centerCoord.col - 15 , centerCoord.col + 15):
                    #verify that given coordinate is legal
                    if self.verifyLegalCoord(Coordinate(irow,icol)):
                        #randomly set cell at coordinate to 'hard to pass'
                        if random.random() >= 0.5:
                            self.cells[irow][icol].setDiff(2)


    def getRandomCoord(self):
        #random legal row
        randrow = random.randint(0, self.numrows - 1)
        #random legal col
        randcol = random.randint(0, self.numcols - 1)
        return Coordinate(randrow, randcol)


    def verifyLegalCoord(self, coord):
        #set base to false in case of logic failure
        legal = False
        #check bounds
        if coord.row >= 0 and coord.row < self.numrows and coord.col >= 0 and coord.col < self.numcols:
            legal = True
        return legal

    #gets Cell color
    def getCColor(self,row,col):
        return self.cells[row][col].color
