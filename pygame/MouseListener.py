# mouse_listener.py

import pygame

class MouseListener:
    def __init__(self):
        self.last_left_click = False
        self.has_chosen_pieces = False

    def get_cell_position(self, mouse_x, mouse_y, cell_size):
        grid_x = (mouse_x // cell_size) * cell_size
        grid_y = (mouse_y // cell_size) * cell_size
        return (grid_x + cell_size // 2, grid_y + cell_size // 2)

    def handle_mouse_event(self, event, game_logic):
        if event.type == pygame.MOUSEBUTTONDOWN and (game_logic.p1_pieces > 0 or game_logic.p2_pieces > 0):

            mouse_x, mouse_y = pygame.mouse.get_pos()
            cell_x, cell_y = self.get_cell_position(mouse_x, mouse_y, 200)  
            if cell_x > 800:
                return
                
            cell_key = (cell_x, cell_y)

            if event.button == 3:  
                game_logic.add_piece(cell_key)
                self.last_left_click = False

            elif event.button == 1:
                if not self.has_chosen_pieces:
                    game_logic.select_cell(cell_key)
                    self.last_left_click = True
                else:
                    game_logic.move_pieces(cell_key)
                    self.has_chosen_pieces = False
        
        if self.last_left_click and event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4]:
                game_logic.pieces_to_move = int(event.unicode)
                game_logic.select_pieces()
                self.has_chosen_pieces = True
                


