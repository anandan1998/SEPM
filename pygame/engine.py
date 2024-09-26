import pygame
import sys

pygame.init()

window_size = (1000,800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('UU Game')

background = pygame.image.load('res/background.png')

#Color variables(rgb-values)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255,0,0)

#Measurements
grid_size = 4
#Cell = one square in the grid
cell_size = 800//grid_size

#Making sure that 5 pieces can fit within a square
piece_width = cell_size - 20
piece_height = (cell_size - 10)//5

#Dictionary to represent the stack on each cell, key being cell coordinate and item being a list of colors.
#For example, {{(cell_x,cell_y),[Black,white,black,white]}, } is a cell at coordinate cell_x and cell_y containing 2 black pieces and 2 white
piece_stacks = {}

#Both players start with 15 pieces
player1_pieces = 15
player2_pieces = 15

#Draws the background
def draw_background():
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, BLACK, pygame.Rect(800,400,200,5))

#Draws a piece, its drawn at a higher resolution then transformed back to increase smoothness
def draw_piece(x, y, width, height, color):
    piece_surface_size = (width * 4, height * 4)
    piece_surface = pygame.Surface(piece_surface_size, pygame.SRCALPHA)
    border_thickness = 4*4

    pygame.draw.ellipse(piece_surface, RED, (0, 0, piece_surface_size[0], piece_surface_size[1]), border_thickness)
    pygame.draw.ellipse(piece_surface, color, (border_thickness, border_thickness, piece_surface_size[0] - 2 * border_thickness, piece_surface_size[1] - 2 * border_thickness))
    scaled_surface = pygame.transform.smoothscale(piece_surface, (width, height))

    screen.blit(scaled_surface, (x-width//2, y-height//2))

#Returns the closest cell to where the mouse was clicked
def get_cell_position(mouse_x, mouse_y):
    grid_x = (mouse_x // cell_size) * cell_size
    grid_y = (mouse_y // cell_size) * cell_size
    return (grid_x + cell_size // 2, grid_y+cell_size//2)

#Draws the remaining pieces of both players
def draw_available_pieces(player1, player2):
    for i in range(player1):
        y_offset = (player1 - 1 - i) * (piece_height // 2)
        draw_piece(900,(400 - y_offset) - piece_height//2,piece_width,piece_height,BLACK)

    for i in range(player2):
        y_offset = (player2 - 1 - i) * (piece_height // 2)
        draw_piece(900,(800 - y_offset) - piece_height//2,piece_width,piece_height,WHITE)
        
#Draws a stack of pieces on a cell
def draw_stack(cell_x, cell_y, piece_stack):
    for i, color in enumerate(piece_stack):
        y_offset = (len(piece_stack) - 1 - i) * (piece_height // 2)
        draw_piece(cell_x, cell_y + y_offset, piece_width, piece_height, color)

running = True
#move counter
counter = 0
#Gameloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #If the mouse is clicked and either player has pieces left
        elif event.type == pygame.MOUSEBUTTONDOWN and (player1_pieces > 0 or player2_pieces > 0):
            #gets coordinates of mouse click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #gets the x and y of the clicked cell
            cell_x, cell_y = get_cell_position(mouse_x,mouse_y)
            
            cell_key = (cell_x, cell_y)

            #if the cell is not already in the stack dictionary, add it
            if cell_key not in piece_stacks:
                piece_stacks[cell_key] = []
            
            #Every even turn is black, every odd turn is white
            if counter % 2 == 0:
                color = BLACK
                player1_pieces-=1
                counter+=1
            else:
                color = WHITE
                player2_pieces-=1
                counter+=1
            
            #if a stack isnt bigger than 5, add a piece to it
            if len(piece_stacks[cell_key]) < 5:
                piece_stacks[cell_key].append(color)
    
    draw_background()
    draw_available_pieces(player1_pieces,player2_pieces)

    #Draw all pieces
    for (cell_x, cell_y), piece_stack in piece_stacks.items():
        draw_stack(cell_x, cell_y, piece_stack)
    
   
    pygame.display.flip()