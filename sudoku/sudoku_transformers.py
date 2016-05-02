import random

from norvig_sudoku import squares as SQUARES
from norvig_sudoku import rows as ROWS, cols as COLS
from sudoku_utils import *

def index_to_row(index):
	return ROWS[index]

def index_to_col(index):
	return COLS[index]

def index_to_square(index):
	return index_to_row(index) + index_to_col(index)

def square_to_index(square):
	r = ROWS.index(square[0])
	c = COLS.index(square[1])
	return r*(GROUP_SIZE**2) + c

def random_square():
	return random.choice(SQUARES)

def random_row():
	return random.choice(ROWS)

def random_col():
	return random.choice(COLS)

def grid_to_2d(grid):
	return [list(grid[i:i+BOARD_SIZE]) for i in xrange(0, BOARD_SIZE**2, BOARD_SIZE)]

def list_to_grid(grid2):
	return ''.join([''.join(row) for row in grid2])

def swap_columns(grid, col1, col2):
	grid2 = grid_to_2d(grid)
	for row in xrange(BOARD_SIZE):
		grid2[row][col1], grid2[row][col2] = grid2[row][col2], grid2[row][col1]
	return grid2

def swap_rows(grid, row1, row2):
	grid2 = grid_to_2d(grid)
	grid2[row2], grid2[row1] = grid2[row1], grid2[row2]
	return grid2

def swap_values(values, s1, s2):
	v1 = values[s1]
	v2 = values[s2]
	values[s2] = v1
	values[s1] = v2

def swap_rows_in_group(grid):
	group = random.randint(0, GROUP_SIZE-1)
	row_1 = random.randint(0, GROUP_SIZE-1)
	row_2 = row_1

	while row_1 == row_2:
		row_2 = random.randint(0, GROUP_SIZE-1)

	# add group offset to row indexes
	row_1 += group*GROUP_SIZE
	row_2 += group*GROUP_SIZE

	# print "Swapping row %d with row %d\n" % (row_1, row_2)

	row_1 = row_1*(BOARD_SIZE)
	row_2 = row_2*(BOARD_SIZE)

	row_1_values = grid[row_1: row_1 + BOARD_SIZE]
	row_2_values = grid[row_2: row_2 + BOARD_SIZE]

	grid = grid[:row_1] + row_2_values + grid[row_1+BOARD_SIZE:]
	grid = grid[:row_2] + row_1_values + grid[row_2+BOARD_SIZE:]

	return grid

def swap_cols_in_group(grid):
	group = random.randint(0, GROUP_SIZE-1)
	col_1 = random.randint(0, GROUP_SIZE-1)
	col_2 = col_1

	while col_1 == col_2:
		col_2 = random.randint(0, GROUP_SIZE-1)

	# add group offset to col indexes
	col_1 += group*GROUP_SIZE
	col_2 += group*GROUP_SIZE

	# print "Swapping col %d with col %d\n" % (col_1, col_2)

	grid = swap_columns(grid, col_1, col_2)
	return list_to_grid(grid)

def swap_row_groups(grid):
	group1 = random.randint(0, GROUP_SIZE-1)
	group2 = group1

	while group2 == group1:
		group2 = random.randint(0, GROUP_SIZE-1)

	# print "Swapping rows of group %d with group %d\n" % (group1, group2)

	for i in xrange(0, GROUP_SIZE):
		grid = list_to_grid(swap_rows(grid, group1*GROUP_SIZE+i, group2*GROUP_SIZE+i))

	return list_to_grid(grid)

def swap_col_groups(grid):
	group1 = random.randint(0, GROUP_SIZE-1)
	group2 = group1

	while group2 == group1:
		group2 = random.randint(0, GROUP_SIZE-1)

	# print "Swapping columns of group %d with group %d\n" % (group1, group2)

	for i in xrange(0, GROUP_SIZE):
		grid = list_to_grid(swap_columns(grid, group1*GROUP_SIZE+i, group2*GROUP_SIZE+i))

	return list_to_grid(grid)

def transpose(grid):
	grid2 = grid_to_2d(grid)
	transposed = map(list, zip(*grid2))
	return list_to_grid(transposed)

def unassign_random(grid):
	index = square_to_index( random_square() )
	while grid[index] in '.0':
		index = square_to_index( random_square() )
	return unassign_index(grid, index)

def unassign_index(grid, index):
	gridlist = list(grid)
	gridlist[index] = '.'
	return ''.join(gridlist)
