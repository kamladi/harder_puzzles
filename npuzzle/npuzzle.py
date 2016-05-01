import random
import copy
import heapq

class NPuzzleSolver(object):
    
    def solve(self, puzzle):
        
        def heuristic(puzzle):
            
            total = 0
            for row in xrange(puzzle.n):
                for col in xrange(puzzle.n):
                    
                    ind = puzzle.board[row][col]
                    ind_row = ind / puzzle.n
                    ind_col = ind % puzzle.n
                    
                    total = total + abs(row - ind_row) + abs(col - ind_col)
                    
            return total
            
        q = [(heuristic(puzzle), 0, puzzle)]
        expanded = 0
        min_f = (heuristic(puzzle))
     
        while q:
            
            f, d, p = heapq.heappop(q)
            expanded += 1
        
            if (p.isSolved()):
                break
        
            next_moves = p.getValidMoves()
            
            for move in next_moves:
                p_move = copy.deepcopy(p)
                p_move.applyMove(move)
                h = heuristic(p_move)
                
                heapq.heappush(q, (d+1+h, d+1, p_move))
                
        return -expanded
        

# NPuzzle is a puzzle from 1 to n^2-1 with a blank space in the top left
class NPuzzle(object):
    
    def __init__(self, n, board):
        
        self.board = board
        self.n = n
        
        for row in xrange(n):
            for col in xrange(n):
                if (board[row][col] == 0):
                    self.blank_ind = [row,col]
        
        
    def isValidMove(self, move):
        
        new_row = move['row']
        new_col = move['col']
        off_dist = abs(new_row - self.blank_ind[0]) + abs(new_col - self.blank_ind[1])
        
        return (off_dist == 1 and new_row >= 0 and new_row < self.n and new_col >= 0 and new_col < self.n)
    
    
    def applyMove(self, move):
        
        assert(self.isValidMove(move))
        new_row = move['row']
        new_col = move['col']
        
        b_ind = self.blank_ind
        self.board[b_ind[0]][b_ind[1]], self.board[new_row][new_col] = self.board[new_row][new_col], self.board[b_ind[0]][b_ind[1]]
        self.blank_ind = [new_row, new_col]
        
    def getValidMoves(self):
        
        b_ind = self.blank_ind
        possible = [(1,0), (-1,0), (0,1), (0,-1)]

        moves = []
        for r_off, c_off in possible:
            move = {'row': b_ind[0] + r_off, 'col': b_ind[1] + c_off }
            if self.isValidMove(move):
                moves.append(move)
                
        return moves
     
        
    def getRandomMove(self):
        moves = self.getValidMoves()
                
        selected = random.randint(0,len(moves)-1)
        return moves[selected]
            
            
    def isSolved(self):
        
        for row in xrange(self.n):
            for col in xrange(self.n):
                
                ind = row * self.n + col
                if (self.board[row][col] != ind):
                    return False
        
        return True
        
        
class NPuzzleGenerator(object):
    
    def generatePuzzles(self, puzzle, solver, branching_factor, step, iterations):
        
        generations = []
        
        for i in xrange(iterations):
            print("Running Iteration %d"%(i))
            proposals = []
            puzzle_efficiency = solver.solve(puzzle)
            
            for k in xrange(branching_factor):
                p_move = copy.deepcopy(puzzle)
                
                for s in xrange(step):
                    move = p_move.getRandomMove()
                    p_move.applyMove(move)
                    
                efficiency = solver.solve(p_move)
                proposals.append((efficiency, p_move))
                
            generations.append((puzzle_efficiency,puzzle))
            min_efficiency,min_puzzle = min(proposals, key=lambda s:s[0])
            
            if (min_efficiency <= puzzle_efficiency):
                puzzle = min_puzzle
            
        return (puzzle, generations)
  
        
n = 4
board = [[row*n + col for col in xrange(n)] for row in xrange(n)]
P = NPuzzle(n, board)
S = NPuzzleSolver()
G = NPuzzleGenerator()

puzzle, generations = G.generatePuzzles(P,S, 2, 2, 20)

for efficiency,g in generations:
    
    for row in g.board:
        print row
    print efficiency
    print
    
  
for row in puzzle.board:
    print row
print


