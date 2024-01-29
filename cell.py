from line import Line
from point import Point
from window import Window

class Cell:
    def __init__(self, win:Window =None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1:int = None
        self.__x2:int = None
        self.__y1:int = None
        self.__y2:int = None
        self.visited = False
        self._win:Window = win

    def get_center_point(self):
            x = ((self.__x2 + self.__x1) * 0.5)
            y = ((self.__y2 + self.__y1) * 0.5)
            return Point(x, y)
    
    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line,"#d9d9d9")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line,"#d9d9d9")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line,"#d9d9d9")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line,"#d9d9d9")

    def draw_move(self, to_cell:"Cell", undo=False):
        if self._win is None:
            return
        color = "red"
        if undo:
            color = "gray"

        self_center = self.get_center_point()
        to_cell_center = to_cell.get_center_point()
        line = Line(self_center, to_cell_center)
        self._win.draw_line(line, color)