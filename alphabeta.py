'''

Alpha-beta pruning is used with the maximum depth of d = 3
The agent was tested against a normal alpha-beta player with depth 8, and won
    (heuristic of normal alpha-beta player: difference of tiles of the two players.)
A game of the agent against a random greedy player takes about 20 seconds (without graphics)

'''

'''

Heuristic function takes the following strategies into consideration
1. Parity:
    The greedy heuristic, maximizing agent's number of tiles
    parity = # agent tiles - # opponent tiles

2. Weighted square strategy:
    a. Corners and edges are the most important cells
    b. Cells that lead to the opponent taking corners and edges shouldn't ba taken
    Weight matrix:
         4, -3,  2,  2,  2,  2, -3,  4
        -3, -4, -1, -1, -1, -1, -4, -3
         2, -1,  1,  0,  0,  1, -1,  2
         2, -1,  0,  1,  1,  0, -1,  2
         2, -1,  0,  1,  1,  0, -1,  2
         2, -1,  1,  0,  0,  1, -1,  2
        -3, -4, -1, -1, -1, -1, -4, -3
         4, -3,  2,  2,  2,  2, -3,  4

    points = sum of points of agent - sum of points of opponent

    Weight matrix is from:
    https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf


3. Current mobility
    Having no  moves leads to a turn skip so this should be avoided.
    Current mobility is less important than capturing corners and more important cells
    But, having no moves has -3*weighted_ratio points
    Mobility = # moves of agent - #moves of opponent
    The idea was adapted from:
    https://link.springer.com/content/pdf/10.1007/978-0-387-35660-0_10.pdf

Heuristic = parity_ratio * parity + weighted_ratio * weighted_points + mobility
(weighted ratio was set to 50, parity ratio was set to 500)

'''

from player import Player
from copy import deepcopy


class AlphaBetaPlayer(Player):

    def __init__(self,player_number,board):
        super().__init__(player_number,board)
        self.max_depth = 3
        self.parity_ratio = 500
        self.weighted_ratio = 50

    def get_next_move(self):
        depth = 0
        alpha = -1
        beta = 10000
        self.board.start_imagination() # use imaginary_grid from this point on
        best_heuristic, best_move = self.alpha_beta(self.board,depth,alpha,beta,self.player_number)
        if best_move is None:
            # return None if there is no possible move left
            return None
        res_coords = self.get_moves(self.board,self.player_number)[best_move]
        return res_coords

    # recursive function
    # uses alpha beta pruning for finding the next move
    def alpha_beta(self,board,depth,alpha,beta,player_number):
        next_opponent = 1 if player_number==0 else 0
        best_heuristic = -1 # could be min or max considering the type of node
        best_move = -1
        # terminating condition: depth is max_depth or there are no more moves left for either of players
        if self.is_leaf(board,player_number) or depth == self.max_depth:
            return self.get_heuristic(board.imaginary_board_grid),None

        if depth%2==0:
            # max node
            best_heuristic = -1
            for (i,next_board) in enumerate(self.get_next_boards(board,player_number)):
                heuristic,_ = self.alpha_beta(next_board,depth+1,alpha,beta,next_opponent)
                if heuristic > best_heuristic:
                    best_heuristic = heuristic
                    best_move = i
                if heuristic > alpha:
                    alpha = heuristic
                if heuristic >= beta:
                    return best_heuristic, best_move
        else:
            # min node
            best_heuristic = 10000
            for (i, next_board) in enumerate(self.get_next_boards(board,player_number)):
                heuristic,_ = self.alpha_beta(next_board, depth + 1, alpha, beta,next_opponent)
                if heuristic < best_heuristic:
                    best_heuristic = heuristic
                    best_move = i
                if heuristic < beta:
                    beta = heuristic
                if heuristic <= alpha:
                    return best_heuristic, best_move
        return best_heuristic, best_move

    # returns all the possible moves of the player
    # if there is no possible move left, returns none
    def get_moves(self,board,player_number):
        moves = []
        for i in range(board.get_n()):
            for j in range(board.get_n()):
                copy_board = deepcopy(board) # make imaginary moves from this imaginary board on
                if copy_board.is_imaginary_move_valid(player_number, i, j):
                    moves.append((i,j))
        if len(moves) == 0:
            return None
        return moves

    # returns true if there are no more moves possible for the player
    def is_leaf(self, board,player_number):
        if self.get_moves(board,player_number) is None:
            return True
        return False

    # returns the boards corresponding to each possible move
    def get_next_boards(self, board,player_number):
        moves = self.get_moves(board,player_number)
        next_boards = []
        for (i,j) in moves:
            copy_board = deepcopy(board)
            copy_board.imagine_placing_piece(player_number, i, j)
            next_boards.append(deepcopy(copy_board))
        return next_boards

    # returns the heuristic of a grid
    # imaginary grid is passed to this function
    def get_heuristic(self, imaginary_board_grid):
        weight_matrix = [[4, -3,  2,  2,  2,  2, -3,  4],
                        [-3, -4, -1, -1, -1, -1, -4, -3],
                        [2, -1,  1,  0,  0,  1, -1,  2],
                        [2, -1,  0,  1,  1,  0, -1,  2],
                        [2, -1,  0,  1,  1,  0, -1,  2],
                        [2, -1,  1,  0,  0,  1, -1,  2],
                        [-3, -4, -1, -1, -1, -1, -4, -3],
                        [4, -3,  2,  2,  2,  2, -3,  4]]
        # wighted squares
        agent_color = ["black","white"][self.player_number]
        opponent_color = "black" if agent_color=="white" else "white"
        agent_score = 0
        opponent_score = 0
        agent_tiles = 0
        opponent_tiles = 0
        for i in range(self.board.get_n()):
            for j in range(self.board.get_n()):
                if self.get_imaginary_color(imaginary_board_grid,i,j) == agent_color:
                    agent_score += weight_matrix[i][j]
                    agent_tiles += 1
                elif self.get_imaginary_color(imaginary_board_grid,i,j) == opponent_color:
                    opponent_score += weight_matrix[i][j]
                    opponent_tiles += 1
        weighted_heuristic = agent_score - opponent_score
        parity_heuristic = agent_tiles - opponent_tiles
        # mobility score
        opponent_number = 0 if self.player_number==1 else 1
        agent_moves = self.get_moves(self.board,self.player_number)
        opponent_moves = self.get_moves(self.board, self.opponent_number)
        if agent_moves is None:
            agent_mobility = -3*self.weighted_ratio
        else:
            agent_mobility = len(agent_moves)
        if opponent_moves is None:
            opponent_mobility = -3*self.weighted_ratio
        else:
            opponent_mobility = len(opponent_moves)
        mobility_heuristic = (agent_mobility - opponent_mobility)

        heuristic = self.parity_ratio * parity_heuristic + self.weighted_ratio * weighted_heuristic + mobility_heuristic
        return heuristic

    # returns the color of a position of an imaginary grid
    def get_imaginary_color(self,imaginary_board_grid, i, j):
        colors = ["black","white"]
        if imaginary_board_grid[i][j] not in [0, 1]:
            return None
        return colors[imaginary_board_grid[i][j]]
