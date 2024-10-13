from player import player
from game_board import game_board
from game_piece import game_piece
import copy

class ai_player(player):

    def __init__(self, color: int):
        super().__init__(color)

    def take_turn(self, board: game_board, timer):
        depth = 2  # Set the depth limit for Minimax
        simulated_remaining_pieces = {
            self.color: self.remaining_pieces,
            1 - self.color: 15  # Adjust as needed based on actual remaining pieces
        }
        best_move, _ = self.minimax(board, depth, True, self.color, simulated_remaining_pieces)
        if best_move is not None:
            if not self.apply_move(board, best_move, self.color):
                pass  # Handle move failure
        else:
            pass  # No valid moves

    def minimax(self, board, depth, maximizing_player, player_color, simulated_remaining_pieces):
        if depth == 0 or board.check_winning_condition(self.color) or board.check_winning_condition(1 - self.color):
            score = self.evaluate_board(board, self.color)
            return None, score

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_all_possible_moves(board, player_color):
                new_board = copy.deepcopy(board)
                new_simulated_remaining_pieces = simulated_remaining_pieces.copy()
                if not self.apply_move(new_board, move, player_color, simulated_remaining_pieces=new_simulated_remaining_pieces):
                    continue  # Skip invalid moves
                _, eval = self.minimax(new_board, depth - 1, False, 1 - player_color, new_simulated_remaining_pieces)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_all_possible_moves(board, player_color):
                new_board = copy.deepcopy(board)
                new_simulated_remaining_pieces = simulated_remaining_pieces.copy()
                if not self.apply_move(new_board, move, player_color, simulated_remaining_pieces=new_simulated_remaining_pieces):
                    continue  # Skip invalid moves
                _, eval = self.minimax(new_board, depth - 1, True, 1 - player_color, new_simulated_remaining_pieces)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move, min_eval

    def get_all_possible_moves(self, board, player_color):
        moves = []

        # Possible 'place' moves
        if self.remaining_pieces > 0:
            for x in range(board.board_size):
                for y in range(board.board_size):
                    position = board.get_position(x, y)
                    if not position or position[-1].is_flat:
                        moves.append(('place', ('flat', x, y)))
                        moves.append(('place', ('standing', x, y)))

        # Possible 'move' and 'split' moves
        for x in range(board.board_size):
            for y in range(board.board_size):
                position = board.get_position(x, y)
                if position and position[-1].color == player_color:
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dx, dy in directions:
                        new_x, new_y = x + dx, y + dy
                        if board.validate_coordinate(new_x, new_y):
                            moves.append(('move', (x, y, new_x, new_y)))
                            # Add possible splits
                            stack_size = len(position)
                            for count in range(1, min(stack_size, board.max_stack_size)):
                                moves.append(('split', (x, y, new_x, new_y, count)))

        return moves

    def apply_move(self, board, move, player_color, simulated_remaining_pieces=None):
        move_type, params = move
        if move_type == 'place':
            piece_type, x, y = params
            if simulated_remaining_pieces is not None:
                if simulated_remaining_pieces[player_color] <= 0:
                    return False
            else:
                if self.remaining_pieces <= 0:
                    return False
            piece = game_piece(player_color, piece_type == 'flat')
            if not board.place_piece(piece, x, y, suppress_output=simulated_remaining_pieces is not None):
                return False
            else:
                if simulated_remaining_pieces is not None:
                    simulated_remaining_pieces[player_color] -= 1
                else:
                    self.remaining_pieces -= 1
        elif move_type == 'move':
            old_x, old_y, new_x, new_y = params
            if not board.move_position(old_x, old_y, new_x, new_y, suppress_output=simulated_remaining_pieces is not None):
                return False
        elif move_type == 'split':
            old_x, old_y, new_x, new_y, count = params
            if not board.split_position(old_x, old_y, new_x, new_y, count, suppress_output=simulated_remaining_pieces is not None):
                return False
        return True

    def evaluate_board(self, board, player_color):
        score = 0
        for x in range(board.board_size):
            for y in range(board.board_size):
                position = board.get_position(x, y)
                if position:
                    top_piece = position[-1]
                    if top_piece.color == player_color:
                        score += 1
                    else:
                        score -= 1
        return score
