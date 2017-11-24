from abc import ABCMeta
from cell import Cell
from coordinate import Coordinate
import math
import random

class Grid:
    # grid objects will be abstract for different A* algorithms
    __metaclass__ = ABCMeta

    def __init__(self,numrows,numcols,numhardcenters,numhighways,percentofblocked,filename):
        # num of rows
        self.numrows = numrows
        # num of columns
        self.numcols = numcols
        #keeps track of centers being used
        self.hardCenterList = []
        #keeps track of Start Coordinate
        self.startCoordinate = None
        # keeps track of Goal Coordinate
        self.goalCoordinate = None
        # file name is given
        # TODO: make this constructor loop take in flags and gather data about grid
        if filename is not None:
            with open(filename) as f:
                #parse start coordinate
                temp = f.readline().split(" ")
                self.startCoordinate = Coordinate(int(temp[0]),int(temp[1]))

                #parse goal coordinate
                temp = f.readline().split(" ")
                self.goalCoordinate = Coordinate(int(temp[0]),int(temp[1]))

                # parse and collect hard center coordinates
                for i in range(numhardcenters):
                    temp = f.readline().split(" ")
                    self.hardCenterList.append(Coordinate(int(temp[0]),int(temp[1])))

                # initiize the grid with cell objects
                self.cells = [[Cell(i,j) for j in range(numcols)] for i in range(numrows)]
                # iterate through rows
                for row in range(0,numrows):
                    # get entire row as string
                    rowstring = f.readline()
                    # iterate trough 'columns' of rownstring
                    for col in range(0,numcols):
                        # assign terrains
                        self.cells[row][col].setTerrain(rowstring[col])
            # close file
            f.closed
        # no file name is given
        else:
            # all cells given in clean
            self.cells = [[Cell(i,j) for j in range(numcols)] for i in range(numrows)]
            # set hard cells
            self.setHardTerrain(numhardcenters)
            # set highway and river paths
            self.setHighways(numhighways)
            # set blocked cells
            self.setBlockedTerrain(percentofblocked)
            # set start and goal cells
            self.selectStartGoal()
        #assign proper colors to START and GOAL Cells
        self.setStartGoalColors()


    # randomly place START and GOAL cells in random regions
    def selectStartGoal(self):
        while True:
            startCoordinate = self.getRandomKeyCoordinate()
            goalCoordinate = self.getRandomKeyCoordinate()

            # calculate Euclidean distance given (x1, y1),(x2, y2) using formula:
            # sqrt((x2 - x1)^2 + (y2 - y1)^2)
            eDistance = math.sqrt(math.pow((goalCoordinate.row - startCoordinate.row),2)+math.pow((goalCoordinate.col - startCoordinate.col),2))

            # TODO: fix scalability of this first if statement
            # checks to see if cells are within 100 cells of each other using absolute value of Euclidean distance
            if math.fabs(eDistance) >= 100:
                # check to make sure cells are not  blocked cells
                if self.cells[startCoordinate.row][startCoordinate.col].terrain != "0":
                    if self.cells[goalCoordinate.row][goalCoordinate.col].terrain != "0":
                        break
        self.startCoordinate = startCoordinate
        self.goalCoordinate = goalCoordinate

    def setStartGoalColors(self):
        self.cells[self.startCoordinate.row][self.startCoordinate.col].color = "green"
        self.cells[self.goalCoordinate.row][self.goalCoordinate.col].color = "red"


    # helper function to get start and goal coordinates
    def getRandomKeyCoordinate(self):
        rowCoord = 0
        colCoord = 0
        # randomly decide if top or bottom 20 rows
        if random.random() > 0.5:   # do top if true
            # hardcoding leaves no room for scalability, 20 obtained in a scalable way
            # works as long as numrows >= 6
            rowCoord = random.randint(0, (self.numrows / 6) - 1)
        else:   #bottom 20 rows
            rowCoord = random.randint(((self.numrows / 6) * 5), self.numrows - 1)

        #randomly decide if left-most or right-most columns
        if random.random() > 0.5:    # do left-most
            # works as long as numrows >= 8
            colCoord = random.randint(0, (self.numcols / 8) - 1)
        else:   # right-most 20 columns
            colCoord = random.randint((self.numcols / 8) * 7, self.numcols - 1)
        return Coordinate(rowCoord, colCoord)

    #randomly assigns areas with difficult terrain
    def setHardTerrain(self, numhardcenters):
        #keeps track of centers being used
        hardTerrainList = []    #holds terrain to be changed to HARD
        #iterate to find 8 center cells
        for i in range(numhardcenters):
            #get center cell coordinate
            while True:
                centerCoord = self.getRandomCoord()
                #breaks loop if center coordinate is not already being used
                if centerCoord not in self.hardCenterList:
                    #add to list as being used
                    self.hardCenterList.append(centerCoord)
                    break

            #iterate through 31 x 31 block of cells around center
            #start at row 15 up from center, end 15 below center
            for irow in range(centerCoord.row - 15 , centerCoord.row + 15):
                #start at col 15 left of center, end 15 right of center
                for icol in range(centerCoord.col - 15 , centerCoord.col + 15):
                    #verify that given coordinate is legal
                    if self.verifyCoordInBounds(Coordinate(irow,icol)):
                        #randomly set cell at coordinate to 'hard to pass'
                        if random.random() > 0.5:
                            hardTerrainList.append(Coordinate(irow,icol))

        #update terrain
        self.changeTerrain(hardTerrainList, "2")

    #randomly assigns 20% of the grid with blocked cells
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

    # sets highway terrain
    def setHighways(self, numhighways):
        # these directions and sides will start at the top, and run clockwise
        # 0 = UP
        # 1 = RIGHT
        # 2 = DOWN
        # 3 = LEFT
        # these enumerations will  serve as the current directions of the path

        #         0^
        #      <3 # 1>
        #         2v

        restart = True      #restart is originally set to true in order to start new highway path
        overlapCount = 0    #overlap counter to use in case process needs to be restarted
        completeCount = 0   #complete count keeps track of amound of completed highways


        allHighwayCoordinates = []      # used to hold all highway coordinates
        currentHighwayCoordinates = []  # used to hold current highway coordinates

        # loop until 4 highways are complete
        while completeCount != numhighways:
            #if highways overlap or a highway gets completed, start again
            if restart:
                # loop is to get starting cell that is not already a highway
                while True:
                    # get random start side using direction enumerations
                    startSide = random.randint(0, 3)
                    # get starting Coordinate using the current startSide
                    currentCoord = self.getStartHighwayCoordinate(startSide)
                    #check to make sure starting coordinate is not already a highway
                    if currentCoord not in allHighwayCoordinates:
                        break

                #makes sure highway will be at least 100 cells long
                highwayLength = 0
                #gets opposite direction of startSide
                direction = self.getOpposideDirection(startSide)

                # paths keep hitting each other, restart entire process
                if overlapCount > 1000:
                    allHighwayCoordinates = []
                    completeCount = 0
                    overlapCount = 0
                #clean current highway
                currentHighwayCoordinates = []
                #mark this process as complete
                restart = False

            # logic for moving through grid; better to have 4 checks with 20 iterations each
            # as opposed to one 20 iteraion loop with 4 direction checks each
            if direction == 0:      #direction is UP
                for i in range(20): #iterator
                    #restartChecks will check if cell is complete, or overlapping another highway
                    restart, overlapCount, completeCount = self.restartChecks(currentCoord, allHighwayCoordinates, currentHighwayCoordinates, highwayLength, completeCount, overlapCount)
                    if restart:
                        break
                    # add previous to list of coordinates
                    currentHighwayCoordinates.append(Coordinate(currentCoord.row , currentCoord.col))
                    #increment highway length
                    highwayLength += 1
                    #move to new coordinate
                    currentCoord.row -= 1

            elif direction == 1:    #direction is RIGHT
                for i in range(20):
                    restart, overlapCount, completeCount = self.restartChecks(currentCoord, allHighwayCoordinates, currentHighwayCoordinates, highwayLength, completeCount, overlapCount)
                    if restart:
                        break
                    currentHighwayCoordinates.append(Coordinate(currentCoord.row , currentCoord.col))
                    highwayLength += 1
                    currentCoord.col += 1

            elif direction == 2:    #direction is DOWN
                for i in range(20):
                    restart, overlapCount, completeCount = self.restartChecks(currentCoord, allHighwayCoordinates, currentHighwayCoordinates, highwayLength, completeCount, overlapCount)
                    if restart:
                        break
                    currentHighwayCoordinates.append(Coordinate(currentCoord.row , currentCoord.col))
                    highwayLength += 1
                    currentCoord.row += 1

            elif direction == 3:    #direction is left
                for i in range(20):
                    restart, overlapCount, completeCount = self.restartChecks(currentCoord, allHighwayCoordinates, currentHighwayCoordinates, highwayLength, completeCount, overlapCount)
                    if restart:
                        break
                    currentHighwayCoordinates.append(Coordinate(currentCoord.row , currentCoord.col))
                    highwayLength += 1
                    currentCoord.col -= 1

            #randomly change direction after 20 iterations
            if random.random() > 0.6:
                direction = self.getPerpendicularDirection(direction)
        #completeCount Loop End

        #change terrain of completed Highways
        self.changeTerrain(allHighwayCoordinates, "highway")

    # setHighways helper functions start
    def restartChecks(self, currentCoord, allHighwayCoordinates, currentHighwayCoordinates,  highwayLength, completeCount, overlapCount):
        restart = False
        if Coordinate(currentCoord.row,currentCoord.col) in allHighwayCoordinates or Coordinate(currentCoord.row,currentCoord.col) in currentHighwayCoordinates:
            restart = True
            overlapCount += 1
        if not self.verifyCoordInBounds(Coordinate(currentCoord.row , currentCoord.col)):
            restart = True
            if highwayLength >= 100:
                allHighwayCoordinates.extend(currentHighwayCoordinates)
                completeCount += 1
        return restart, overlapCount, completeCount

    # returns the opposite of the current direction
    def getOpposideDirection(self,direction):
        return{
            0 : 2,      #UP to DOWN
            1 : 3,      #RIGHT to LEFT
            2 : 0,      #DOWN to UP
            3 : 1,      #LEFT to RIGHT
        }[direction]

    # randomly returns a direction perpendicular to the current direction
    def getPerpendicularDirection(self, direction):
        newDirection = direction
        #current durrection is UP or DOWN
        if direction == 0 or direction == 2:
            if random.random() > 0.5:
                #new direction is now RIGHT
                newDirection = 1
            else:
                #new direction is now LEFT
                newDirection = 3
        #current direction is RIGHT or LEFT
        elif direction == 1 or direction == 3:
            if random.random() > 0.5:
                #new direction is now UP
                newDirection = 0
            else:
                #new direction is now DOWN
                newDirection = 2
        return newDirection

    # coordinate helper functions start
    # returns random coordinate on grid
    def getRandomCoord(self):
        #random legal row
        randrow = random.randint(0, self.numrows - 1)
        #random legal col
        randcol = random.randint(0, self.numcols - 1)
        return Coordinate(randrow, randcol)

    # returns a random start for a border
    def getStartHighwayCoordinate(self,startSide):
        #start with random Coordinate
        randCoord = self.getRandomCoord()

        if startSide == 0:      #starting on TOP side
            randCoord.row = 0
        elif startSide == 1:    #starting on RIGHT side
            randCoord.col = self.numcols - 1
        elif startSide == 2:    #starting on BOTTOM side
            randCoord.row = self.numrows - 1
        elif startSide == 3:    #starting on LEFT side
            randCoord.col = 0
        return randCoord
    # setHighways helper functions end

    # check that Coordinate is not out of bounds
    def verifyCoordInBounds(self, coord):
        #set base to false in case of logic failure
        inBounds = False
        #check bounds
        if coord.row >= 0 and coord.row < self.numrows and coord.col >= 0 and coord.col < self.numcols:
            inBounds = True
        return inBounds

    # takes in a list of coordinates and updates those cells with given terrain
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
    # coordinate helper functions end

    # gets Cell color
    def getCColor(self,row,col):
        return self.cells[row][col].color

    # outputs grid object to given path
    def outputToFile(self,fileName):
        f = open(fileName , 'w')
        # print Start Coordinate
        f.write(repr(self.startCoordinate) + "\n")
        # print Goal Coordinate
        f.write(repr(self.goalCoordinate) +"\n")
        # print center cell locations
        for coord in self.hardCenterList:
            f.write(repr(coord)+"\n")
        for row in range(0, self.numrows):
            for col in range(0, self.numcols):
                f.write(str(self.cells[row][col].terrain))
            f.write("\n")
        f.close()
