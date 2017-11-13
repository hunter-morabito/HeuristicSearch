import Tkinter as tk

class GridUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #use 600 by 800 for 5 px
        self.canvas = tk.Canvas(self, width=960, height=720, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 120
        self.columns = 160
        self.cellwidth = 6
        self.cellheight = 6
        switch = False;
        self.rect = {}
        for row in range(120):
            switch = not switch
            for col in range(160):
                switch = not switch
                x1 = col * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight

                #used for testing
                if switch:
                    self.rect[row,col] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#E1E1E1", tags="rect")
                else:
                    self.rect[row,col] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="#ffffff", tags="rect")
                #will use for showing path:
                #self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval")



if __name__ == "__main__":
    gridui = GridUI()
    gridui.mainloop()
