from graphics import Line, Point

class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._visited = False
        self._win = win
    
    def draw(self, x1, x2, y1, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        self._win.draw_line(left_wall, "black" if self.has_left_wall else "white")
        
        right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        self._win.draw_line(right_wall, "black" if self.has_right_wall else "white")

        top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self._win.draw_line(top_wall, "black" if self.has_top_wall else "white")

        bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        self._win.draw_line(bottom_wall, "black" if self.has_bottom_wall else "white")
        
    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        fill_color = "red" if undo == False else "gray"
        c1 = Point((self._x1+self._x2)/2, (self._y1+self._y2)/2)
        c2 = Point((to_cell._x1+to_cell._x2)/2, (to_cell._y1+to_cell._y2)/2)
        self._win.draw_line(Line(c1, c2), fill_color)
