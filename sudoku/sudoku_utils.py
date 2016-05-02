import math
from norvig_sudoku import display, grid_values
from norvig_sudoku import cols as COLS

BOARD_SIZE = len(COLS)
GROUP_SIZE = int(math.sqrt(BOARD_SIZE))

def display_grid(grid):
	display(grid_values(grid))
