import time
from Piece import Piece

STARTING_PIECES = 15


class GameLogic:
    def __init__(self):
        self.p_current = 1
        self.piece_stacks = {}
        self.p1_pieces = 15
        self.p2_pieces = 15
        self.error_msg = None
        self.msg_timer = None
        self.selected_cell = None
        self.pieces_to_move = 0


    def add_piece(self,cell_key):
        self.selected_cell = None
        if cell_key not in self.piece_stacks:
            self.piece_stacks[cell_key] = []
        
        if len(self.piece_stacks[cell_key]) < 5:
            if self.p_current == 1:
                self.p1_pieces -= 1
            else:
                self.p2_pieces -= 1
            
            self.piece_stacks[cell_key].append(Piece(self.p_current))
            self.p_current = 1 if self.p_current == 2 else 2
        else:
            self.error_msg = "Invalid move, stack is already full!"
            self.msg_timer = time.time()
    
    def select_cell(self,cell_key):
        if cell_key in self.piece_stacks.keys() and len(self.piece_stacks[cell_key]) > 1:
            if self.piece_stacks[cell_key][-1].player == self.p_current:
                self.selected_cell = cell_key

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
        
        



   


    def reset_error(self):
        if self.msg_timer and time.time() - self.msg_timer > 2:
            self.error_msg = None
            
  