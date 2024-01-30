from window import Window
from cell import Cell
from time import sleep
from random import seed,choice
class Maze:
    def __init__(self,x:int,y:int,num_rows:int,num_cols:int,cell_size_x:int,cell_size_y:int,win:Window = None,seeds=None) -> None:
        self.__x1 = x
        self.__y1 = y
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self._cells = []
        if seeds:
            seed(seeds)
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0,0)
        self._reset_cells_visted()
        self.solve_maze()
        print("end")

    def __create_cells(self):
        for _ in range(self.__num_cols):
            col = []
            for _ in range(self.__num_rows):
                col.append(Cell(self.__win))
            self._cells.append(col)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i,j)

    def __draw_cell(self,i:int,j:int):
        if self.__win is None:
            return
        cell:Cell = self._cells[i][j]
        x = self.__x1 + self.__cell_size_x*i
        y = self.__y1 + self.__cell_size_y*j
        x1 = x + self.__cell_size_x
        y1 = y + self.__cell_size_y
        cell.draw(x,y,x1,y1)
        self.__animate()
    
    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        sleep(0.03)
    
    def __break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self._cells[self.__num_cols-1][self.__num_rows-1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols-1,self.__num_rows-1)
    
    def __break_walls_r(self,i:int,j:int):
        self._cells[i][j].visited = True
        while True:
            ij = self.__check_adjacent_wall(i,j)
            if not ij:
                self.__draw_cell(i,j)
                return
            chosen = choice(ij)
            next_cell = self.__break_walls((i,j),chosen)
            self.__break_walls_r(next_cell[0],next_cell[1])

    def __check_adjacent_wall(self,col:int,row:int):
        res = []
        if self.__num_cols-1 > col and not self._cells[col+1][row].visited:
            res.append("right")
        if  col > 0 and not self._cells[col-1][row].visited:
            res.append("left")
        if self.__num_rows -1 > row and not self._cells[col][row+1].visited:
            res.append("bottom")
        if  row > 0 and not self._cells[col][row-1].visited:
            res.append("top")
        return res
    
    def __break_walls(self,cell:tuple,direction: str):
        if direction == "top":
            self._cells[cell[0]][cell[1]].has_top_wall = False
            self._cells[cell[0]][cell[1]-1].has_bottom_wall = False
            return cell[0],cell[1]-1
        elif direction == "bottom":
            self._cells[cell[0]][cell[1]].has_bottom_wall = False
            self._cells[cell[0]][cell[1]+1].has_top_wall = False
            return cell[0],cell[1]+1
        elif direction == "left":
            self._cells[cell[0]][cell[1]].has_left_wall = False
            self._cells[cell[0]-1][cell[1]].has_right_wall = False
            return cell[0]-1,cell[1]
        self._cells[cell[0]][cell[1]].has_right_wall = False
        self._cells[cell[0]+1][cell[1]].has_left_wall = False
        return cell[0]+1,cell[1]
    
    def _reset_cells_visted(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve_maze(self,bfs:bool = True):
        if bfs:
            result = self.solve_maze_bfs()
            if not result:
                return
            for i in range(len(result)-1):
                result[i].draw_move(result[i+1])
                self.__animate()
    
    def solve_maze_dfs(self,i:int,j:int):
        self.__animate()
        cell:Cell = self._cells[i][j]
        if cell.visited:
            return []
        
        if i == self.__num_cols-1 and j == self.__num_rows-1:
            return [cell]
        cell.visited = True
        to_visit = cell.check_wall()
        if  i == 0 and j == 0:
            to_visit.remove("top") 
        for direction in to_visit:
            value = self.__break_walls((i,j),direction)
            if self._cells[value[0]][value[1]].visited:
                pass
            cell.draw_move(self._cells[value[0]][value[1]])
            result = self.solve_maze_dfs(value[0],value[1])
            if result:
                result.append(cell)
                cell.draw_move(self._cells[value[0]][value[1]])
                return result
            else:
                cell.draw_move(self._cells[value[0]][value[1]],True)
        return []
    def solve_maze_bfs(self,begin_i=0,begin_j=0):
        path = {(begin_i,begin_j):None}
        to_visit = [(begin_i,begin_j)]
        while to_visit:
            cell_position = to_visit.pop()
            cell:Cell = self._cells[cell_position[0]][cell_position[1]]
            cell.visited = True
            directions = cell.check_wall()
            if cell_position[0] == 0 and cell_position[1] == 0:
                directions.remove("top")
            for direction in directions:
                value = self.__break_walls(cell_position,direction)
                next_cell = self._cells[value[0]][value[1]]
                if value[0] == self.__num_cols-1 and value[1] == self.__num_rows-1:
                    current = cell_position
                    res_path = [self._cells[-1][-1]]
                    while current:
                        res_path.append(self._cells[current[0]][current[1]])
                        current = path[current]
                    return res_path
                if not next_cell.visited:
                    next_cell.visited = True
                    to_visit.insert(0,value)
                    path[value] = cell_position
                    cell.draw_move(next_cell,True)
                    self.__animate()