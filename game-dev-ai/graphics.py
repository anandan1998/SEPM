from subprocess import call
from os import system, name
from game_board import game_board
from game_piece import game_piece
from timer import timer

from loguru import logger


from color import *

# import logging

# logger = logging.getLogger(__name__)


class graphics:

    def __init__(self):
        pass

    def clear(self):
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")

    def start_screen(self):
        self.clear()

    """
    Example board.
    /-------x-------x-------x-------\
    | _____ | _____ | _____ | _____ |
    x-------+-------+-------+-------x
    | _____ | _____ | _____ | _____ |
    x-------+-------+-------+-------x
    | _____ | _____ | _____ | _____ |
    x-------+-------+-------+-------x
    | _____ | _____ | _____ | _____ |
    \-------x-------x-------x-------/  
    
    """

    def draw(self, gameboard: game_board, player1_timer: timer, player2_timer: timer):

        console.print("              Curr move              ", style="board")
        console.print("x-------+-------+-------+-------x", style="board")
        for row in gameboard.board:
            console.print(self.draw_board_row(row), style="board")
            console.print("x-------+-------+-------+-------x", style="board")
        console.print("\n--------Time Remaining------------\n", style="info")
        console.print(
            "opponent Black :"
            + " {:.2f}".format(player1_timer.check_remaining_time())
            + " seconds",
            style="info",
        )
        console.print(
            "opponent White :"
            + " {:.2f}".format(player2_timer.check_remaining_time())
            + " seconds",
            style="info",
        )
        console.print("\n----------------------------------", style="board")

    def draw_board_row(self, row: list) -> str:
        row_string: str = "| "
        for position in row:
            for piece in position:
                row_string = (
                    row_string + str(piece.color)
                    if piece.is_flat
                    else row_string + "[r]" + str(piece.color) + "[/r]"
                )

            max_stack_size = game_board.max_stack_size
            blank_space = max_stack_size - len(position)
            for _ in range(blank_space):
                row_string = row_string + " "
            row_string = row_string + " | "
        return row_string

    def draw_prev_board(self, gameboard: game_board):
        console.print("              Prev move              ", style="prevboard")
        console.print("x-------+-------+-------+-------x", style="prevboard")
        for row in gameboard.prev_board:
            console.print(self.draw_prev_board_row(row), style="prevboard")
            console.print("x-------+-------+-------+-------x", style="prevboard")

    def draw_prev_board_row(self, row: list) -> str:
        row_string: str = "| "
        for position in row:
            for piece in position:
                if piece == 3:
                    row_string = row_string + "[r]" + str(piece - 3) + "[/r]"
                elif piece == 4:
                    row_string = row_string + "[r]" + str(piece - 3) + "[/r]"
                else:
                    row_string = row_string + str(piece)
            max_stack_size = game_board.max_stack_size
            blank_space = max_stack_size - len(position)
            for _ in range(blank_space):
                row_string = row_string + " "
            row_string = row_string + " | "
        return row_string


if __name__ == "__main__":
    print("This could be used to run tests...")
    print("Exiting... Please run from Main.py")
    exit()
