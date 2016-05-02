import sys
import copy
import random
import math

from norvig_sudoku import parse_grid, from_file, display, random_puzzle
from norvig_sudoku import assign as assign_norvig, squares as SQUARES
from norvig_sudoku import rows as ROWS, digits as DIGITS, cols as COLS
from norvig_sudoku import units as UNITS, peers as PEERS
from sudoku_utils import *
from sudoku_transformers import swap_rows_in_group, swap_cols_in_group, \
	swap_row_groups, swap_col_groups, transpose, unassign_index, unassign_random

"""
CONSTANTS
=========
squares: list of location names in board, named as 'A1','D3', etc.
					A-F represent row index, 1-9 represent col index

unit: collection of nine squares which together have to contain a
			permutation of digits 1-9
units: dictionary mapping a square to a list of units that include that square.
"""

class SudokuSolver(object):
	def solve(self, grid):
		return self.search(parse_grid(grid), 0)

	def solve_all(self, grid):
		return self.search_all(parse_grid(grid), 0, [])

	# Assign the given digit to the given square, and propogate any other
	# assignments that can be made. Only counts the first asignment
	# to num_assignments (only increments it by one)
	def assign(self, values, square, digit, num_assignments):
		return (assign_norvig(values, square, digit), num_assignments+1)

	# This function is a modified version of Norvig's solve() to count the number
	#		of assignments
	# values: dict mapping a square in the grid to a string of possible digits
	def search(self, values, num_assignments):
		# unable to parse grid / failed earlier
		if values is False:
			return (False, num_assignments)

		# Solved!
		if all(len(values[s]) == 1 for s in SQUARES):
			return (values, num_assignments)

		# Choose unfilled square with the fewest possibilities

		n,s = min((len(values[s]),s) for s in SQUARES if len(values[s]) > 1)

		for d in values[s]:
			# Try assigning digit d to square s
			(values_after_assignment, num_assignments) = self.assign(values.copy(), s, d, num_assignments)
			new_values, new_num_assignments = self.search(values_after_assignment, num_assignments)
			if new_values:
				return (new_values, new_num_assignments)

		# None of the possibilities were valid
		return (False, num_assignments)

	# This function is a modified version of Norvig's solve() to count the number
	#	of assignments, as well as a list of all possible solutions
	# values: dict mapping a square in the grid to a string of possible digits
	def search_all(self, values, num_assignments, solutions):
		# unable to parse grid / failed earlier
		if values is False:
			return (False, num_assignments, solutions)

		# Solved!
		if all(len(values[s]) == 1 for s in SQUARES):
			solutions.append( (values, num_assignments) )
			return (values, num_assignments, solutions)

		# Choose unfilled square with the fewest possibilities
		n,s = min((len(values[s]),s) for s in SQUARES if len(values[s]) > 1)

		for d in values[s]:
			# Try assigning digit d to square s
			(values_after_assignment, num_assignments) = self.assign(values.copy(), s, d, num_assignments)
			new_values, new_num_assignments, solutions = self.search_all(values_after_assignment, num_assignments, solutions)

		# None of the possibilities were valid
		return (False, num_assignments, solutions)


# Wrapper class around two forms of sudoku board generators
class SudokuGenerator(object):
	# Iteratively remove assignments from the grid
	def generate_remove_assignments(self, grid, solver, unique_solution=False, num_iterations=100):
		values, num_assignments = solver.solve(grid)
		cur_grid = grid
		for i,value in enumerate(cur_grid):
			if value not in '.0':
				next_grid = unassign_index(grid, i)
				if unique_solution:
					# If we care about unique solutions (only counts as valid if
					# only one solution exists)
					next_values, next_num_assignments, solutions = solver.solve_all(next_grid)
					if len(solutions) > 1:
						# Too many solutions, pass
						continue
					elif len(solutions) == 0:
						# No solution, pass
						continue
					else:
						# New grid has exactly one solution
						next_values, next_num_assignments = solutions[0]
				else:
					# Don't care about multiple solution
					next_values, next_num_assignments = solver.solve(next_grid)

				# No solution
				if not next_values:
					continue

				# We have found a more difficult sudoku puzzle
				elif next_num_assignments > num_assignments:
					print "Found improvement: %d => %d" % (num_assignments, next_num_assignments)
					cur_grid = next_grid

		return cur_grid

	def generate_random_transformations(self, grid, solver, step_size, iterations):
		TRANSFORMS = [swap_rows_in_group, swap_cols_in_group, swap_row_groups, swap_col_groups, transpose]
		cur_grid = grid
		value, num_assignments = solver.solve(grid)
		for i in xrange(iterations):
			# peform {step_size} transformations to the grid
			next_grid = copy.copy(cur_grid)
			for k in xrange(step_size):
				next_grid = random.choice(TRANSFORMS)(grid)
			new_value, new_num_assignments = solver.solve(grid)
			if new_value:
				if num_assignments < new_num_assignments:
					print "Found improvement: %d => %d\n" % (num_assignments, new_num_assignments)
					cur_grid = next_grid
		return cur_grid

if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit("Must include filename as an argument")

	grids = []
	filename = sys.argv[1]
	separator = '\n'
	if filename == 'random':
		grids = [random_puzzle(random.randint(25, 30)) for i in xrange(50)]
	else:
		if filename == 'easy50.txt':
			separator = '========'
		grids = from_file(filename, separator)

	solver = SudokuSolver()
	generator = SudokuGenerator()

	if len(sys.argv) > 2:
		random.seed()

		random_grid = grids[random.randint(0, len(grids)-1)].replace('\n','')
		display_grid(random_grid)

		values, num_assignments = solver.solve(random_grid)
		print "Initial number of assignments: ", num_assignments

		command = sys.argv[2]

		if command == 'transform':
			new_grid = generator.generate_random_transformations(random_grid, solver, 3, 50)

		elif command == 'remove':
			# Mathematicians currently believe 17 is the minimum number of assignments
			# in a sudoku board for there to be a unique solution
			MIN_NUM_ASSIGNMENTS = 17
			UNIQUE_SOLUTION = False
			num_iterations = 100
			if len(sys.argv) > 3:
				num_iterations = int(sys.argv[3])

			new_grid = random_grid
			for k in xrange(num_iterations):
				# Stop improving when minimum number of assignments has been reached
				nonempty_squares = list(square for square in new_grid if square not in '.0')
				if len(nonempty_squares) <= MIN_NUM_ASSIGNMENTS:
					break
				cur_grid = generator.generate_remove_assignments(new_grid, solver, UNIQUE_SOLUTION)
				if new_grid == cur_grid:
					break
				new_grid = cur_grid

		# Used to test out individual transformations
		elif command == 'unassign':
			new_grid = unassign_random(random_grid)
		elif command == 'swap_rows':
			new_grid = swap_rows_in_group(random_grid)
		elif command == 'swap_cols':
			new_grid = swap_cols_in_group(random_grid)
		elif command == 'swap_row_groups':
			new_grid = swap_row_groups(random_grid)
		elif command == 'swap_col_groups':
			new_grid = swap_col_groups(random_grid)
		elif command == 'transpose':
			new_grid = transpose(random_grid)
		else:
			sys.exit("unknown argument " + sys.argv[2])

		display_grid(new_grid)
		result, result_num_assignments = solver.solve(new_grid)
		print "Result num assignments: %d => %d\n" % (num_assignments, result_num_assignments)
	else:
		# Solve all the puzzles in the given file
		for i,g in enumerate(grids):
			solutions = solver.solve_all(g)[2]
			print "%d: %s" % (i, map(lambda s: s[1], solutions))
