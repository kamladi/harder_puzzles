from random import randint

# Pipe object to connect End Points
class Pipe(object):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return "Pipe:" + str(self.color)

# End Points set at beginning of game
class EndPoint(object):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return "End:" + str(self.color)

# solve a flow board
class FlowSolver(object):

    def solve(self, board):
        pass

# Flow board and moves
class FlowPuzzle(object):
    def __init__(self, size):
        self.size = size
        # map of starting boards (from last level of game)
        self.starting_boards = {
        5: {0: [(0,0),(3,2)], 1: [(0,4),(4,2)], 2: [(2,1),(4,1)], 3: [(4,0),(2,2)]},
        6: {0: [(1,0),(3,5)], 1: [(1,1),(4,5)], 2: [(1,3),(4,4)], 3: [(2,1),(4,1)], 4: [(5,0),(3,1)]},
        7: {},
        8: {},
        9: {}
        }
        self.board = self.make_init_board()

    # create an initial board based on size
    def make_init_board(self):
        board = [[None for _ in xrange(self.size)] for _ in xrange(self.size)]
        # randomly place end points
        for i in self.starting_boards[self.size]:
            for (r,c) in self.starting_boards[self.size][i]:
                board[r][c] = EndPoint(i)
        return board

    def is_valid_move(self, move):
        pass

    def apply_move(self, move):
        pass

    def get_valid_moves(self):
        pass

    def get_random_move(self):
        pass

    def is_solved(self):
        # check that entire grid is not None
        for r in xrange(self.size):
            for c in xrange(self.size):
                if self.board[r][c] is None:
                    return False
        # check that all end points are connected
        start_points = self.starting_boards[self.size]
        for color in start_points:
            start_coord, end_coord = start_points[color]
            cur_row, cur_col = start_coord
            connecting = True
            while connecting:
                cur_row, cur_col = self.has_neighbor(color, cur_row, cur_col)
                if cur_row < 0 and cur_col < 0:
                    return False
                if (cur_row, cur_col) == end_coord:
                    connecting = False
        return True

    # see if a neighbor is the same color
    def has_neighbor(self, color, row, col):
        possibilities = [(1,0), (-1,0), (0,1), (0,-1)]
        for p in possibilities:
            r = row - p[0]
            c = col - p[1]
            if self.is_in_bounds(r, c) and self.board[r][c] is not None and self.board[r][c].color == color:
                return r, c
        return -1, -1

    # see if coordinates are in bounds on the board
    def is_in_bounds(self, r, c):
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            return False
        return True

    # print out a game board
    def print_board(self):
        for row in self.board:
            for col in row:
                print str(col).ljust(7),
            print

# generate a puzzle
class FlowGenerator(object):

    def generate_puzzles(self, puzzle, solver, branching_factor, step, iterations):
        return

n = 5
P = FlowPuzzle(n)
P.print_board()
print P.is_solved()
S = FlowSolver()
G = FlowGenerator()
