import Tkinter as tk
from grid import Grid


#safe keeping: , *args, **kwargs

#in charge of grawing grid
class GridUI(tk.Tk):
    def __init__(self, grid):
        tk.Tk.__init__(self)
        #cell height and width in pixels
        cellwidth = 6
        cellheight = 6
        #initialize Canvas
        self.canvas = tk.Canvas(self, height = (grid.numrows * cellheight), width = (grid.numcols * cellwidth), borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        self.rect = {}

        for row in range(grid.numrows):
            for col in range(grid.numcols):
                #set cell coordinates
                x1 = col * cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight

                #print cell
                self.rect[row,col] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=grid.getCColor(row,col), tags="rect")

                #will use for showing path:
                #self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval")
