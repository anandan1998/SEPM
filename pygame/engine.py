import pygame
import sys
from GameLogic import GameLogic
from Renderer import Renderer
from MouseListener import MouseListener

pygame.init()
pygame.mixer.init()


window_size = (1000,800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('UU Game')

background = pygame.image.load('res/background.png')




grid_size = 4
cell_size = 800 // grid_size
piece_width = cell_size-20
piece_height = (cell_size-10)//5

game_logic = GameLogic(grid_size,cell_size)
renderer = Renderer(screen)
mouse_listener = MouseListener()

illegal_move_sound = pygame.mixer.Sound('res/illegal.mp3')
illegal_played = False

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
        if not illegal_played:
            illegal_move_sound.play()
            illegal_played = True
        renderer.draw_message(game_logic.error_msg,(0, 0, 0), (350, 50), game_logic.msg_timer)
        game_logic.reset_error()
    else:
        illegal_played = False

    if game_logic.check_for_winner() == 1:
        print("player 1 wins")
    if game_logic.check_for_winner() == 2:
        print("player 2 wins")

    pygame.display.flip()