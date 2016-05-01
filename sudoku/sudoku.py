import sys
from norvig_sudoku import parse_grid, from_file
from norvig_sudoku import assign as assign_norvig, squares as SQUARES
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


if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit("Must include filename as an argument")

	grids = from_file(sys.argv[1])
	solver = SudokuSolver()

	for i,g in enumerate(grids):
		print "%d: %d steps" % (i, solver.solve(g)[1])
