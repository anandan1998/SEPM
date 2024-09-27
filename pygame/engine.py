import pygame
import sys
from GameLogic import GameLogic
from Renderer import Renderer
from MouseListener import MouseListener

pygame.init()

window_size = (1000,800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('UU Game')

background = pygame.image.load('res/background.png')

game_logic = GameLogic()
renderer = Renderer(screen)
mouse_listener = MouseListener()

grid_size = 4
cell_size = 800 // grid_size
piece_width = cell_size-20
piece_height = (cell_size-10)//5

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        mouse_listener.handle_mouse_event(event=event,game_logic=game_logic)

    renderer.draw_background()
    renderer.draw_available_pieces(game_logic.p1_pieces,game_logic.p2_pieces,piece_width,piece_height)

    for (cell_x,cell_y), piece_stack in game_logic.piece_stacks.items():
        renderer.draw_stack(cell_x, cell_y, piece_stack)
    
    if game_logic.selected_cell:
        renderer.highlight_cell(game_logic.selected_cell[0],game_logic.selected_cell[1])

    if game_logic.error_msg:
        renderer.draw_message(game_logic.error_msg,(0, 0, 0), (350, 50), game_logic.msg_timer)
        game_logic.reset_error()

    pygame.display.flip()