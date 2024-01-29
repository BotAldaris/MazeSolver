from tkinter import Tk, BOTH, Canvas
from line import Line

class Window:
    def __init__(self,width:int, heigth:int) -> None:
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(width=width,height=heigth)
        self.__canvas.pack()
        self.__running = True

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        while self.__running:
            self.redraw()
    
    def close(self):
        self.__running = False      

    def draw_line(self,line:Line,fill_color:str = "black"):
        line.draw(self.__canvas,fill_color)  
    