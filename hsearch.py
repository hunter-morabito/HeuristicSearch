from grid import Grid
from gridui import GridUI
import time

def main():
    numrows = 120
    numcols = 160
    grid = Grid(numrows , numcols)

    #draw
    GridUI(grid).mainloop()


if __name__ == "__main__":
    main()
