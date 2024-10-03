import time
import random
import copy
from collections import deque

STARTING_PIECES = 15


class Piece:
    def __init__(self, player, is_capstone, selected=False):
        self.player = player
        self.selected = selected
        self.is_capstone = is_capstone

    def set_selected(self, selected):
        self.selected = selected


class GameLogic:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.p_current = 1  # 1 for human player, 2 for AI
        self.piece_stacks = {}
        self.p1_pieces = STARTING_PIECES
        self.p2_pieces = STARTING_PIECES
        self.error_msg = None
        self.selected = False
        self.msg_timer = None
        self.selected_cell = None
        self.pieces_to_move = 0

    def add_piece(self, cell_key, is_capstone):
        self.reset_move_operation()
        if cell_key not in self.piece_stacks:
            self.piece_stacks[cell_key] = []

        if len(self.piece_stacks[cell_key]) < 5:
            if self.p_current == 1:
                self.p1_pieces -= 1
            else:
                self.p2_pieces -= 1

            self.piece_stacks[cell_key].append(Piece(self.p_current, is_capstone=is_capstone))
            self.p_current = 1 if self.p_current == 2 else 2

            # After changing player, check if it's AI's turn
            if self.p_current == 2:
                self.ai_move(4)
        else:
            self.error_msg = "Invalid move, stack is already full!"
            self.msg_timer = time.time()

        # Check for a winner after the move
        winner = self.check_for_winner()
        if winner:
            print(f"Player {winner} wins!")

    def select_cell(self, cell_key):
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
        if self.pieces_to_move <= len(current_cell):
            for piece in current_cell[-self.pieces_to_move:]:
                piece.set_selected(True)

    def reset_move_operation(self):
        if self.selected_cell is not None:
            for piece in self.piece_stacks[self.selected_cell]:
                piece.selected = False
        self.selected_cell = None

    def move_pieces(self, cell_dest):
        pieces_to_move = [piece for piece in self.piece_stacks[self.selected_cell] if piece.selected]

        if cell_dest not in self.piece_stacks:
            self.piece_stacks[cell_dest] = []

        if len(pieces_to_move) + len(self.piece_stacks[cell_dest]) > 5:
            self.error_msg = "Invalid move, too many pieces"
            self.msg_timer = time.time()
            self.reset_move_operation()
            return

        dest_cell = self.piece_stacks[cell_dest]

        for piece in pieces_to_move:
            piece.selected = False
            dest_cell.append(piece)
            self.piece_stacks[self.selected_cell].remove(piece)

        self.p_current = 1 if self.p_current == 2 else 2
        self.selected_cell = None

        # After changing player, check if it's AI's turn
        if self.p_current == 2:
            self.ai_move()

        # Check for a winner after the move
        winner = self.check_for_winner()
        if winner:
            print(f"Player {winner} wins!")

    def ai_move(self,depth ):
        # AI logic for player 2
        print("AI is thinking...")
        # depth = 5  # Set the depth of the minimax algorithm
        best_score = float('-inf')
        best_move = None

        # Generate all possible moves
        moves = self.get_all_possible_moves(2)

        for move in moves:
            # Simulate the move
            simulated_game = copy.deepcopy(self)
            simulated_game.apply_move(move, 2)
            score = self.minimax(simulated_game, depth - 1, False, float('-inf'), float('inf'))

            if score > best_score:
                best_score = score
                best_move = move

        if best_move:
            # Apply the best move
            self.apply_move(best_move, 2)
            print(f"AI performed move: {best_move}")
            # Switch back to human player
            self.p_current = 1
        else:
            # No valid moves, pass the turn
            print("AI has no valid moves")
            self.p_current = 1

        # Check for a winner after the AI's move
        winner = self.check_for_winner()
        if winner:
            print(f"Player {winner} wins!")

    def minimax(self, game_state, depth, is_maximizing_player, alpha, beta):
        winner = game_state.check_for_winner()
        if depth == 0 or winner:
            return self.evaluate_board(game_state, winner)

        if is_maximizing_player:
            max_eval = float('-inf')
            moves = game_state.get_all_possible_moves(2)
            for move in moves:
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_move(move, 2)
                eval = self.minimax(new_game_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            moves = game_state.get_all_possible_moves(1)
            for move in moves:
                new_game_state = copy.deepcopy(game_state)
                new_game_state.apply_move(move, 1)
                eval = self.minimax(new_game_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def evaluate_board(self, game_state, winner):
        if winner == 2:
            return float('inf')
        elif winner == 1:
            return float('-inf')
        else:
            # Heuristic evaluation
            return self.heuristic(game_state)

    def heuristic(self, game_state):
        # Basic heuristic: difference in number of pieces on the board
        ai_score = 0
        player_score = 0

        for stack in game_state.piece_stacks.values():
            if stack:
                top_piece = stack[-1]
                if top_piece.player == 2:
                    ai_score += 1
                elif top_piece.player == 1:
                    player_score += 1

        return ai_score - player_score

    def get_all_possible_moves(self, player):
        moves = []

        # First, consider placing a piece if available
        pieces_left = self.p2_pieces if player == 2 else self.p1_pieces
        if pieces_left > 0:
            empty_cells = []
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    cell_key = (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2)
                    if cell_key not in self.piece_stacks or len(self.piece_stacks[cell_key]) == 0:
                        empty_cells.append(cell_key)
            for cell in empty_cells:
                moves.append(('place', cell, False))  # False indicates not a capstone

        # Now, consider moving pieces
        for cell_key, stack in self.piece_stacks.items():
            if stack and stack[-1].player == player:
                # Try moving in all directions
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
                col = (cell_key[0] - self.cell_size // 2) // self.cell_size
                row = (cell_key[1] - self.cell_size // 2) // self.cell_size
                for dx, dy in directions:
                    new_col = col + dx
                    new_row = row + dy
                    if 0 <= new_col < self.grid_size and 0 <= new_row < self.grid_size:
                        dest_cell = (new_col * self.cell_size + self.cell_size // 2, new_row * self.cell_size + self.cell_size // 2)
                        stack_size = len(self.piece_stacks.get(dest_cell, []))
                        if stack_size + 1 <= 5:
                            moves.append(('move', cell_key, dest_cell))

        return moves

    def apply_move(self, move, player):
        if move[0] == 'place':
            # Place a piece
            cell_key = move[1]
            is_capstone = move[2]
            if cell_key not in self.piece_stacks:
                self.piece_stacks[cell_key] = []
            self.piece_stacks[cell_key].append(Piece(player, is_capstone))
            if player == 2:
                self.p2_pieces -= 1
            else:
                self.p1_pieces -= 1
        elif move[0] == 'move':
            from_cell = move[1]
            to_cell = move[2]
            if to_cell not in self.piece_stacks:
                self.piece_stacks[to_cell] = []
            # Move one piece for simplicity
            moving_piece = self.piece_stacks[from_cell].pop()
            self.piece_stacks[to_cell].append(moving_piece)
            if not self.piece_stacks[from_cell]:
                del self.piece_stacks[from_cell]

    def check_for_winner(self):
        # Matrix representation of the board
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

        if self.dfs_walk(top_matrix, 1):
            return 1
        if self.dfs_walk(top_matrix, 2):
            return 2

        return None

    def dfs_walk(self, top_matrix, player):
        grid_size = len(top_matrix)
        visited = set()

        def dfs(row, col, direction):
            if row < 0 or row >= grid_size or col < 0 or col >= grid_size:
                return False
            if (row, col) in visited or top_matrix[row][col] != player:
                return False

            visited.add((row, col))

            if direction == 'vertical' and row == grid_size - 1:
                return True
            if direction == 'horizontal' and col == grid_size - 1:
                return True

            if direction == 'vertical':
                return (dfs(row + 1, col, 'vertical') or
                        dfs(row, col - 1, 'vertical') or
                        dfs(row, col + 1, 'vertical'))
            elif direction == 'horizontal':
                return (dfs(row, col + 1, 'horizontal') or
                        dfs(row - 1, col, 'horizontal') or
                        dfs(row + 1, col, 'horizontal'))

            return False

        for col in range(grid_size):
            if top_matrix[0][col] == player:
                if dfs(0, col, 'vertical'):
                    return True

        for row in range(grid_size):
            if top_matrix[row][0] == player:
                if dfs(row, 0, 'horizontal'):
                    return True

        return False

    def reset_error(self):
        if self.msg_timer and time.time() - self.msg_timer > 2:
            self.error_msg = None
