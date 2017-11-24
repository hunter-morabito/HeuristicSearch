import sys
import os.path
from grid import Grid
from gridui import GridUI
import time

def main(args):
    # TODO: make input flags to make these scalable
    numrows = 120
    numcols = 160
    numhardcenters = 8
    numhighways = 4
    percentofblocked = 20
    # check for filename input
    if len(args) > 0:
        filename = "bin/" + args[0]
        # file exists
        if os.path.isfile(filename):
            # attempt to build grid from input
            try:
                grid = Grid(numrows, numcols, numhardcenters, numhighways, percentofblocked, filename)
            except:
                print "Error Occurred when reading from file\nMake sure file format is correct"
        # file does not exist
        else:
            print "Error Occurred in trying to read file\nMake sure file is under 'bin' directory."
            return
    # no file argumaent given
    else:
        grid = Grid(numrows , numcols , numhardcenters, numhighways, percentofblocked, None)

    # output to file
    grid.outputToFile('bin/gridLog.txt')
    # draw
    GridUI(grid).mainloop()


if __name__ == "__main__":
    main(sys.argv[1:])
