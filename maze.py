from cell import Cell
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    def _create_cells(self):
        for col in range(self._num_cols):
            list = []
            for row in range(self._num_rows):
                list.append(Cell(self._win))
            self._cells.append(list)
        
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + self._cell_size_x * i
        x2 = self._x1 + self._cell_size_x * (i+1)
        y1 = self._y1 + self._cell_size_y * j
        y2 = self._y1 + self._cell_size_y * (j + 1)
        self._cells[i][j].draw(x1, x2, y1, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        top_left_cell.has_top_wall = False
        self._draw_cell(0, 0)

        bottom_right_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        bottom_right_cell.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
    
    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            points = []
            #left
            if i > 0 and not self._cells[i - 1][j]._visited:
                points.append((i-1,j))
            #right
            if i < self._num_cols - 1 and not self._cells[i + 1][j]._visited:
                points.append((i+1,j))
            #up
            if j > 0 and not self._cells[i][j - 1]._visited:
                points.append((i,j-1))
            #down
            if j < self._num_rows - 1 and not self._cells[i][j + 1]._visited:
                points.append((i,j+1))

            if len(points) == 0:
                self._draw_cell(i,j)
                return
            
            chosen = random.randrange(len(points))
            chosen_direction = points[chosen]
            
            #left
            if chosen_direction[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            #right
            if chosen_direction[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            #up
            if chosen_direction[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            #down
            if chosen_direction[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            self._break_walls_r(chosen_direction[0], chosen_direction[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j]._visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j]._visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
    
        #right
        if i < self._num_cols - 1 and not self._cells[i + 1][j]._visited and self._cells[i][j].has_right_wall == False:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        #down
        if j < self._num_rows - 1 and not self._cells[i][j + 1]._visited and self._cells[i][j].has_bottom_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)
                
        #left
        if i > 0 and not self._cells[i - 1][j]._visited and self._cells[i][j].has_left_wall == False:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        #up
        if j > 0 and not self._cells[i][j - 1]._visited and self._cells[i][j].has_top_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        return False