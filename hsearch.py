import sys
import os.path
from grid import Grid
from gridui import GridUI
from astarbase import AStarBase
import time
import copy


def main(args):
    # TODO: make input flags to make these parameters mutable
    #change back to 120
    numrows = 120
    #changebackto 160
    numcols = 160
    numhardcenters = 8
    numhighways = 4
    percentofblocked = 20
    maps = []
    # check for filename input
    if len(args) > 0:
        #changing for input
        # filename = "bin/" + args[0]
        filename = args[0]
        # file exists
        if filename == "deliverable":
        # need to make 'deliverable' for now...
        # if os.path.isfile(filename):
            # attempt to build grid from input
            try:
                for i in range(5):
                    grid = Grid(numrows , numcols , numhardcenters, numhighways, percentofblocked, 'bin/gridLog'+str(i)+'.txt')
                    for j in range(10):
                        maps.append(grid)
                        grid = copy.deepcopy(grid)
                for m in maps:
                    m.selectStartGoal()
            except:
                print "Error Occurred when reading from file\nMake sure file format is correct"
        # file does not exist
        else:
            print "Error Occurred in trying to read file\nMake sure file is under 'bin' directory."
            return
    # no file argumaent given
    else:
        for i in range(5):
            grid = Grid(numrows , numcols , numhardcenters, numhighways, percentofblocked, None)
            grid.outputToFile('bin/gridLog'+str(i+1)+'.txt')
            for j in range(10):
                maps.append(grid)
                grid = copy.deepcopy(grid)
        for m in maps:
            m.selectStartGoal()



    # draw
    GridUI(maps).mainloop()


if __name__ == "__main__":
    main(sys.argv[1:])
