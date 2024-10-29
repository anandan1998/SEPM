import pygame
import time

WINDOW_SIZE = (1000, 800)
GRID_SIZE = 4
CELL_SIZE = 800 // GRID_SIZE
PIECE_WIDTH = CELL_SIZE - 20
PIECE_HEIGHT = (CELL_SIZE - 10) // 5
INITIAL_PIECES = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (102, 153, 255)
RED = (255,0,0)

class Renderer:
    def __init__(self,screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None,48)
        self.background = pygame.image.load('res/background.png')

    def draw_background(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.background,(0,0))
        pygame.draw.rect(self.screen,BLACK,pygame.Rect(800,400,200,8))

    def draw_piece(self,x,y,color,marked,is_capstone):
        border_color = RED if marked else BLUE
        piece_surface_size = (PIECE_WIDTH * 4, PIECE_HEIGHT * 4)
        piece_surface = pygame.Surface(piece_surface_size, pygame.SRCALPHA)
        border_thickness = 16  

        if not is_capstone:
            pygame.draw.ellipse(piece_surface, border_color, (0, 0, piece_surface_size[0], 
                                                    piece_surface_size[1]), border_thickness)
            
            pygame.draw.ellipse(piece_surface, color, (border_thickness, border_thickness,
                    piece_surface_size[0] - 2 * border_thickness, piece_surface_size[1] - 2 * border_thickness))
            
            scaled_surface = pygame.transform.smoothscale(piece_surface, (PIECE_WIDTH, PIECE_HEIGHT))
            
            self.screen.blit(scaled_surface, (x - PIECE_WIDTH // 2, y - PIECE_HEIGHT // 2))
        else:
            capstone_width = PIECE_WIDTH * 0.6
            capstone_height = PIECE_HEIGHT
            capstone_surface = pygame.Surface((capstone_width, capstone_height), pygame.SRCALPHA)
            border_thickness = 4

            pygame.draw.rect(capstone_surface, border_color, (0, 0, capstone_width, capstone_height), border_thickness)
            pygame.draw.rect(capstone_surface, color, (border_thickness, border_thickness, 
                                                   capstone_width - 2 * border_thickness, 
                                                   capstone_height - 2 * border_thickness))
            self.screen.blit(capstone_surface, (x - capstone_width // 2, y - capstone_height // 2))
       

    def draw_stack(self, cell_x, cell_y, piece_stack):
        for i, piece in enumerate(piece_stack):
            y_offset = (len(piece_stack) - 1 - i) * (PIECE_HEIGHT // 2)
            self.draw_piece(cell_x, cell_y + y_offset, BLACK if piece.player == 1 else WHITE,piece.selected,piece.is_capstone)

    def draw_message(self, text, color, position, t):
        x = time.time() - t
        f = max(0, min(1, 1 - (x / 2)))

        message = self.font.render(text, True, color)
        message.set_alpha(int(f * 255))

        tw, th = message.get_size()
        background = pygame.Surface((tw + 20, th + 20))
        background.fill(WHITE)
        background.set_alpha(int(f * 255))
        bp = (position[0] - 10, position[1] - 10)

        self.screen.blit(background, bp)
        self.screen.blit(message, position)
    
    def draw_available_pieces(self, player1_pieces, player2_pieces, piece_width, piece_height):
        for i in range(player1_pieces):
            y_offset = (player1_pieces - 1 - i) * (piece_height // 2)
            self.draw_piece(900, (350 - y_offset) - piece_height // 2, (0, 0, 0),False,False)
        for i in range(player2_pieces):
            y_offset = (player2_pieces - 1 - i) * (piece_height // 2)
            self.draw_piece(900, (750 - y_offset) - piece_height // 2, (255, 255, 255),False,False)

    def highlight_cell(self,cell_x,cell_y):
        pygame.draw.rect(self.screen, (255, 0, 0), (cell_x - 100, cell_y-100, 200, 200), 6) 

        
