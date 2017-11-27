from grid import Grid
from astarclasses import AStarEuclidean, AStarManhattan,AStarOctile,AStarUniform,AStarTieBreak
import time
import copy

def main():
    maps = []
    numrows = 120
    numcols = 160
    numhardcenters = 8
    numhighways = 4
    percentofblocked = 20
    for i in range(5):
        grid = Grid(numrows , numcols , numhardcenters, numhighways, percentofblocked, 'bin/gridLog'+str(i)+'.txt')
        for j in range(10):
            maps.append(grid)
            grid = copy.deepcopy(grid)
    for m in maps:
        m.selectStartGoal()

    avgEucDist = 0
    avgEucTime = 0
    avgEucNodes = 0
    avgManDist = 0
    avgManTime = 0
    avgManNodes = 0
    avgTieDist = 0
    avgTieTime = 0
    avgTieNodes = 0
    avgUSDist = 0
    avgUSTime = 0
    avgUSNodes = 0
    avgOctDist = 0
    avgOctTime = 0
    avgOctNodes = 0

    for m in maps:
        #EUC
        temp = copy.deepcopy(m)
        aStar = AStarEuclidean(m, 1.5)
        starttime = time.time()
        aStar.run()
        avgEucTime = (avgEucTime+(time.time() - starttime)) / 2.0
        avgEucDist = (avgEucDist + aStar.grid.cells[aStar.grid.goalCoordinate.row][aStar.grid.goalCoordinate.col].g) / 2.0
        avgEucNodes = (avgEucNodes + aStar.nodesExpanded)/2.0
        m = temp
        #Man
        temp = copy.deepcopy(m)
        aStar = AStarManhattan(m, 1.5)
        starttime = time.time()
        aStar.run()
        avgManTime = (avgManTime+(time.time() - starttime)) / 2.0
        avgManDist = (avgManDist + aStar.grid.cells[aStar.grid.goalCoordinate.row][aStar.grid.goalCoordinate.col].g) / 2.0
        avgManNodes = (avgManNodes + aStar.nodesExpanded)/2.0
        m = temp
        #Tie
        temp = copy.deepcopy(m)
        aStar = AStarTieBreak(m, 1.5)
        starttime = time.time()
        aStar.run()
        avgTieTime = (avgTieTime+(time.time() - starttime)) / 2.0
        avgTieDist = (avgTieDist + aStar.grid.cells[aStar.grid.goalCoordinate.row][aStar.grid.goalCoordinate.col].g) / 2.0
        avgTieNodes = (avgTieNodes + aStar.nodesExpanded)/2.0
        m = temp
        #US
        temp = copy.deepcopy(m)
        aStar = AStarUniform(m, 1.5)
        starttime = time.time()
        aStar.run()
        avgUSTime = (avgUSTime+(time.time() - starttime)) / 2.0
        avgUSDist = (avgUSDist + aStar.grid.cells[aStar.grid.goalCoordinate.row][aStar.grid.goalCoordinate.col].g) / 2.0
        avgUSNodes = (avgUSNodes + aStar.nodesExpanded)/2.0
        m = temp
        #Octal
        temp = copy.deepcopy(m)
        aStar = AStarOctile(m, 1.5)
        starttime = time.time()
        aStar.run()
        avgOctTime = (avgOctTime+(time.time() - starttime)) / 2.0
        avgOctDist = (avgOctDist + aStar.grid.cells[aStar.grid.goalCoordinate.row][aStar.grid.goalCoordinate.col].g) / 2.0
        avgOctNodes = (avgOctNodes + aStar.nodesExpanded)/2.0
        m = temp


    print "E"
    print avgEucTime,avgEucDist,avgEucNodes
    print "M"
    print avgManTime,avgManDist,avgManNodes
    print "T"
    print avgTieTime,avgTieDist,avgTieNodes
    print "U"
    print avgUSTime,avgUSDist,avgUSNodes
    print "O"
    print avgOctTime,avgOctDist,avgOctNodes




if __name__ == "__main__":
    main()
