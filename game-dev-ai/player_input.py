from player import player
from game_board import game_board
from game_piece import game_piece
from timer import timer
from loguru import logger

import time
import sys
import os

# Remove this line:
# from rich.console import Console

# Import the console from color.py instead
from color import console

class player_input:

    rules_string: str = """
                                    ----HELP----
        1. Example command for placing a "flat" coin at location 1,2: "place f 1 2"
        2. Example command for placing a "standing" coin at location 1,2: "place s 1 2"
        3. Example command for splitting the 3 latest pieces in (1 2) and moving them to (1 3): "split 1 2 1 3 3"
        4. To exit the game, use: "q"
                                    -------------
    """

    def __init__(self, board: game_board):
        self.board = board  # Correctly assign the board reference

    def ask_to_take_turn(self, player: player, timer: timer) -> None:
        timer.start_timer()
        self.parse_and_act_on_move(player, timer=timer)
        timer.pause_timer()
        return

    def parse_and_act_on_move(self, player: player, timer: timer):
        color = player.color
        color_string = "Black" if color == 0 else "White"

        while True:
            remaining_time = timer.check_remaining_time()
            if remaining_time > 0:
                console.print(
                    f"\nOpponent {color_string}'s turn!",
                    style="board",
                )
                console.print("Type cmd(q to quit): ", style="info")
                action_input = input()
                action = action_input.strip().split()

                if not action:
                    console.print("No input detected, try again.", style="warning")
                    continue

                command = action[0].lower()

                if command in ["quit", "q", "exit"]:
                    console.print("Quitting...", style="error")
                    os._exit(1)

                if command == "help":
                    console.print(self.rules_string, style="help")
                    continue

                if command == "place":
                    if len(action) != 4:
                        console.print(
                            "Wrong number of arguments entered, try again.",
                            style="warning",
                        )
                        continue

                    if player.remaining_pieces <= 0:
                        console.print(
                            "No pieces left to place, try again.", style="warning"
                        )
                        continue

                    piece_type = action[1].lower()
                    if piece_type.startswith("f"):
                        piece = game_piece(player.color, True)
                    elif piece_type.startswith("s"):
                        piece = game_piece(player.color, False)
                    else:
                        console.print(
                            "Piece must be 'flat' or 'standing', try again.",
                            style="warning",
                        )
                        continue

                    try:
                        target_x = int(action[2])
                        target_y = int(action[3])
                    except ValueError:
                        console.print(
                            "Coordinates must be integers, try again.",
                            style="warning",
                        )
                        continue

                    if not self.board.place_piece(piece, target_x, target_y):
                        console.print(
                            "Invalid placement of piece, try again.", style="warning"
                        )
                        continue
                    else:
                        player.remaining_pieces -= 1

                        # Check for a winning condition
                        if self.board.check_winning_condition(player.color):
                            console.print(
                                f"Player {color_string} has won!",
                                style="black on white",
                            )
                            os._exit(0)  # Exit the game if someone wins

                        return  # Turn is over

                elif command == "move":
                    if len(action) != 5:
                        console.print(
                            "Wrong number of arguments entered, try again.",
                            style="warning",
                        )
                        continue

                    try:
                        old_x = int(action[1])
                        old_y = int(action[2])
                        target_x = int(action[3])
                        target_y = int(action[4])
                    except ValueError:
                        console.print(
                            "Coordinates must be integers, try again.",
                            style="warning",
                        )
                        continue

                    if not self.board.move_position(old_x, old_y, target_x, target_y):
                        console.print("Illegal move, try again!", style="error")
                        continue
                    else:
                        # Check for a winning condition
                        if self.board.check_winning_condition(player.color):
                            console.print(
                                f"Player {color_string} has won!",
                                style="black on white",
                            )
                            os._exit(0)  # Exit the game if someone wins

                        return  # Turn is over

                elif command == "split":
                    if len(action) != 6:
                        console.print(
                            "Wrong number of arguments entered, try again.",
                            style="warning",
                        )
                        continue

                    try:
                        old_x = int(action[1])
                        old_y = int(action[2])
                        target_x = int(action[3])
                        target_y = int(action[4])
                        pieces = int(action[5])
                    except ValueError:
                        console.print(
                            "Coordinates and count must be integers, try again.",
                            style="warning",
                        )
                        continue

                    if not self.board.split_position(
                        old_x, old_y, target_x, target_y, pieces
                    ):
                        console.print("Illegal move, try again!", style="error")
                        continue
                    else:
                        # Check for a winning condition
                        if self.board.check_winning_condition(player.color):
                            console.print(
                                f"Player {color_string} has won!",
                                style="black on white",
                            )
                            os._exit(0)  # Exit the game if someone wins

                        return  # Turn is over

                else:
                    console.print(
                        "Invalid command. Type 'help' for available commands.",
                        style="warning",
                    )
                    continue

            else:
                console.print(
                    f"Player {color_string} time out!!!", style="error"
                )
                os._exit(0)

        return

if __name__ == "__main__":
    print("This could be used to run tests...")
    print("Exiting... Please run from Main.py")
    exit()
