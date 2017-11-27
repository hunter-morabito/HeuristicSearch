import Tkinter as tk
from grid import Grid
from astarbase import AStarBase
from astarclasses import AStarEuclidean, AStarManhattan,AStarOctile,AStarUniform,AStarTieBreak
import copy
import pdb

#in charge of grawing grid
class GridUI(tk.Tk):
    def __init__(self, maps):
        tk.Tk.__init__(self)
        #list of the 50 possible maps
        self.maps = maps
        self.initLabels()
        self.initMapButtons()
        self.initGoalSwitchButtons()
        self.initAStarOptions()

        self.mapNum = 1
        self.goalNum = 1
        # done initializing labels
        #keeps track of how long A*'s take
        self.runTime = 0
        # run and draw the first A* algorithm to start
        self.runAStar(1,1)

        # draw the first grid
        # self.redraw(self.aStar.grid)

        # put buttons at top of grid
        self.mapButtonsGroup.grid(row = 0, column = 0)
        # put goal switch buttons on grid
        self.goalButtonsGroup.grid(row = 1,column = 0)
        # put labels on grid
        self.groupCellBio.grid(row = 2, column = 1)
        self.astarGroup.grid(row = 3,column = 0)


    def redraw(self,grid):
        self.timelabel.configure(text = "Time: " + str(self.aStar.runtime))
        self.distlabel.configure(text = "Total distance: "+str(self.aStar.grid.cells[self.aStar.grid.goalCoordinate.row][self.aStar.grid.goalCoordinate.col].g))
        self.nodeslabel.configure(text = "Nodes Expanded: " + str(self.aStar.nodesExpanded))
        #cell height and width in pixels
        #CHANGE THIS BACK TO 6 PIXELS
        cellwidth = 6
        cellheight = 6
        #initialize Canvas
        self.canvas = tk.Canvas(self, height = (grid.numrows * cellheight), width = (grid.numcols * cellwidth), borderwidth=0, highlightthickness=0)

        self.canvas.pack(side="top", fill="both", expand="true")

        self.rect = {}
        self.oval = {}

        for row in range(grid.numrows):
            for col in range(grid.numcols):
                #set cell coordinates
                x1 = col * cellwidth
                y1 = row * cellheight
                x2 = x1 + cellwidth
                y2 = y1 + cellheight

                #print cell
                self.rect[row,col] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=grid.getCell(row,col).color, tags=(row,col))
                self.canvas.tag_bind(self.rect[row,col],"<Button-1>", self.update_cell_bio)
                #will use for showing path:
                if grid.getCell(row,col).partOfPath:
                    self.oval[row,col] = self.canvas.create_oval(x1+0.5,y1+0.5,x2-0.5,y2-0.5, fill="green", tags=(row,col))
                    self.canvas.tag_bind(self.oval[row,col],"<Button-1>", self.update_cell_bio)
        self.canvas.grid(row = 2,column=0)

    def initLabels(self):
        # labels
        self.groupCellBio = tk.LabelFrame(self,text = "Cell Info",padx = 5,pady = 5)
        self.cellCoordLabel = tk.Label(self.groupCellBio,text = "Cell Bio")
        self.glabel = tk.Label(self.groupCellBio,text = "Cell G")
        self.hlabel = tk.Label(self.groupCellBio,text = "Cell H")
        self.flabel = tk.Label(self.groupCellBio,text = "Cell F")
        self.timelabel = tk.Label(self.groupCellBio,text = "Time: ")
        self.distlabel = tk.Label(self.groupCellBio,text = "Distance: ")
        self.nodeslabel = tk.Label(self.groupCellBio,text = "Nodes Expanded: ")
        # pack labels into group
        self.cellCoordLabel.pack()
        self.glabel.pack()
        self.hlabel.pack()
        self.flabel.pack()
        self.timelabel.pack()
        self.distlabel.pack()
        self.nodeslabel.pack()

    def initMapButtons(self):
        self.mapButtonsGroup = tk.LabelFrame(self,text = "Map Options",padx = 5,pady = 5)
        for i in range(1, 6):
            m1 = tk.Button(self.mapButtonsGroup,text = str(i))
            m1.pack(side="left")
            m1.bind("<Button-1>", self.newMap)

    def initGoalSwitchButtons(self):
        self.goalButtonsGroup = tk.LabelFrame(self,text = "Goal Options",padx = 5,pady = 5)
        for i in range(1, 11):
            b1 = tk.Button(self.goalButtonsGroup,text = str(i))
            b1.pack(side="left")
            b1.bind("<Button-1>", self.newGoal)

    # TODO: clean this up to make the buttons pull from a list
    def initAStarOptions(self):
        self.selection = "Euclidean"
        self.astarGroup = tk.LabelFrame(self,text = "A* Options",padx = 5,pady = 5)
        weightLabel = tk.Label(self.astarGroup,text = "Weight: ")
        self.weightedEnter = tk.Entry(self.astarGroup)
        weightLabel.pack(side="left")
        self.weightedEnter.pack(side="left")
        self.weightedEnter.insert(0,"1")
        heuristics = ['Euclidean','Manhattan','Octal','Uniform Cost','Tie Break']
        for h in heuristics:
            b1 = tk.Button(self.astarGroup,text = h)
            b1.bind("<Button-1>", self.selectAStar)
            b1.pack(side="left")


    def selectAStar(self,event):
        self.selection = event.widget['text']
        self.runAStar(self.mapNum,self.goalNum)


    def newMap(self,event):
        self.mapNum = int(event.widget['text'])
        self.runAStar(self.mapNum,self.goalNum)

    def newGoal(self,event):
        self.goalNum = int(event.widget['text'])
        self.runAStar(self.mapNum,self.goalNum)

    def runAStar(self, mapNum, goalNum):
        mapNum = (mapNum - 1) * 10
        mapNum = mapNum + (goalNum - 1)
        temp = copy.deepcopy(self.maps[mapNum])
        if self.selection == "Euclidean":
            self.aStar = AStarEuclidean(self.maps[mapNum], float(self.weightedEnter.get()))
        elif self.selection == "Manhattan":
            self.aStar = AStarManhattan(self.maps[mapNum],float(self.weightedEnter.get()))
        elif self.selection == "Octal":
            self.aStar = AStarOctile(self.maps[mapNum],float(self.weightedEnter.get()))
        elif self.selection == "Uniform Cost":
            self.aStar = AStarUniform(self.maps[mapNum],float(self.weightedEnter.get()))
        elif self.selection == "Tie Break":
            self.aStar = AStarTieBreak(self.maps[mapNum],float(self.weightedEnter.get()))

        self.aStar.run()
        self.redraw(self.aStar.grid)
        self.maps[mapNum] = temp

    def update_cell_bio(self,event):
        cellWidget = event.widget.find_closest(event.x,event.y)
        tags = event.widget.gettags(cellWidget)
        cell = self.aStar.grid.getCell(int(tags[0]),int(tags[1]))

        self.cellCoordLabel.configure(text = cell.coordinate)
        self.glabel.configure(text = "G: "+str(cell.g))
        self.hlabel.configure(text = "H: " + str(cell.h))
        self.flabel.configure(text = "F: " + str(cell.f))
