import time
from collections import deque

STARTING_PIECES = 15


class Piece:
    def __init__(self, player, is_capstone,selected=False,):
        self.player = player
        self.selected = selected
        self.is_capstone = is_capstone

    def set_selected(self,selected):
        self.selected = selected


class GameLogic:
    def __init__(self,grid_size,cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.p_current = 1
        self.piece_stacks = {}
        self.p1_pieces = 15
        self.p2_pieces = 15
        self.error_msg = None
        self.selected=False,
        self.msg_timer = None
        self.selected_cell = None
        self.pieces_to_move = 0


    def add_piece(self,cell_key,is_capstone):
        self.selected_cell = None
        if cell_key not in self.piece_stacks:
            self.piece_stacks[cell_key] = []
        
        if len(self.piece_stacks[cell_key]) < 5:
            if self.p_current == 1:
                self.p1_pieces -= 1
            else:
                self.p2_pieces -= 1
            
            self.piece_stacks[cell_key].append(Piece(self.p_current,is_capstone=is_capstone))
            self.p_current = 1 if self.p_current == 2 else 2
        else:
            self.error_msg = "Invalid move, stack is already full!"
            self.msg_timer = time.time()
    
    def select_cell(self,cell_key):
        if cell_key in self.piece_stacks.keys() and len(self.piece_stacks[cell_key]) > 1:
            if self.piece_stacks[cell_key][-1].player == self.p_current:
                self.selected_cell = cell_key
            else:
                self.error_msg = "Invalid move, you don't control this stack"
                self.msg_timer = time.time()
        else:
            self.error_msg = "Invalid move, this stack is too small"
            self.msg_timer = time.time()
        

    def select_pieces(self):
        current_cell = self.piece_stacks[self.selected_cell]
        for piece in current_cell:
            piece.set_selected(False)
        if self.pieces_to_move < len(current_cell):
            for piece in current_cell[-self.pieces_to_move:]:
                piece.set_selected(True)
    

    def move_pieces(self,cell_dest):
        pieces_to_move = [piece for piece in self.piece_stacks[self.selected_cell] if piece.selected]

        if cell_dest not in self.piece_stacks:
            self.piece_stacks[cell_dest] = []

        dest_cell = self.piece_stacks[cell_dest]

        for piece in pieces_to_move:
            piece.selected = False
            dest_cell.append(piece)
            self.piece_stacks[self.selected_cell].remove(piece)

        self.selected_cell = None

    def check_for_winner(self):
        top_matrix = []

        for row in range(self.grid_size):
            rows = []
            for col in range(self.grid_size):
                cell_key = (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2)
                if cell_key in self.piece_stacks and len(self.piece_stacks[cell_key]) > 0 and not self.piece_stacks[cell_key][-1].is_capstone:
                    top_piece = self.piece_stacks[cell_key][-1]
                    rows.append(top_piece.player)
                else:
                    rows.append(0)
            top_matrix.append(rows)
        
        print(top_matrix)

        if self.dfs_walk(top_matrix, 1):
            return 1
        if self.dfs_walk(top_matrix, 2):
            return 2

        return None


    """
    Depth first search from chat GPT
    """
    def dfs_walk(self, top_matrix, player):
        grid_size = len(top_matrix)
        visited = set()

        # Helper function to perform DFS recursively
        def dfs(row, col, direction):
            # If out of bounds, already visited, or not the player's piece
            if row < 0 or row >= grid_size or col < 0 or col >= grid_size:
                return False
            if (row, col) in visited or top_matrix[row][col] != player:
                return False

            # Mark the position as visited
            visited.add((row, col))

            # Check for a winning path
            if direction == 'vertical' and row == grid_size - 1:  # Reached bottom row
                return True
            if direction == 'horizontal' and col == grid_size - 1:  # Reached rightmost column
                return True

            # Explore neighbors
            if direction == 'vertical':
                return (dfs(row + 1, col, 'vertical') or  # down
                        dfs(row, col - 1, 'vertical') or  # left
                        dfs(row, col + 1, 'vertical'))    # right
            elif direction == 'horizontal':
                return (dfs(row, col + 1, 'horizontal') or  # right
                        dfs(row - 1, col, 'horizontal') or  # up
                        dfs(row + 1, col, 'horizontal'))    # down
                
            return False

        # Start DFS for vertical paths from the top row
        for col in range(grid_size):
            if top_matrix[0][col] == player:  # Start from any player piece in the top row
                if dfs(0, col, 'vertical'):
                    return True

        # Start DFS for horizontal paths from the left column
        for row in range(grid_size):
            if top_matrix[row][0] == player:  # Start from any player piece in the left column
                if dfs(row, 0, 'horizontal'):
                    return True

        return False



    def reset_error(self):
        if self.msg_timer and time.time() - self.msg_timer > 2:
            self.error_msg = None
            
  