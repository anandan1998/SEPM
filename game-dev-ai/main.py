from game_board import game_board
from game_piece import game_piece
from player import player
from ai_player import ai_player  # Import the AI player class
from player_input import player_input

from loguru import logger

from graphics import graphics
from timer import timer

logger.remove()
from color import *

graphics = graphics()

def main():
    """
    Main application
    """
    global ai_player_flag
    ai_player_flag = False  # Initialize the AI player flag
    graphics.clear()

    while True:
        console.print(
            "Do you want to play against the AI? (y/n):",
            style="info",
        )
        ai_choice = input().strip().lower()
        if ai_choice == 'y':
            ai_player_flag = True
            break
        elif ai_choice == 'n':
            ai_player_flag = False
            break
        else:
            console.print(
                "Invalid input. Please type 'y' or 'n'.",
                style="info",
            )

    while True:
        console.print(
            "Write 'play' to start the game, 'rules' to see the rules or 'q' to quit the game:",
            style="info",
        )
        command = input().strip().lower()

        if command == "play":
            test()  # Start the game
            break
        elif command == "rules":
            console.print(player_input.rules_string, style="help")
        elif command == "q":
            exit()
            break
        else:
            console.print(
                "Invalid input. Please type 'play' to start the game, 'rules' to see the rules or 'q' to exit.",
                style="info",
            )
    return

def test():
    """
    application logic
    """
    logger.debug("test started...")
    board: game_board = game_board()
    if ai_player_flag:
        player_black = ai_player(color=0)
    else:
        player_black = player(color=0)
    player_white = player(color=1)
    input_handler = player_input(board=board)

    playing = True
    player1_timer = timer(duration=5)  # 5 min timer
    player2_timer = timer(duration=5)  # 5 min timer
    first = True
    board.save_board()
    while playing:
        if not first:
            graphics.draw_prev_board(gameboard=board)
        board.save_board()
        graphics.draw(
            gameboard=board, player1_timer=player1_timer, player2_timer=player2_timer
        )

        if ai_player_flag:
            player1_timer.start_timer()
            player_black.take_turn(board=board, timer=player1_timer)
            player1_timer.pause_timer()
        else:
            input_handler.ask_to_take_turn(player=player_black, timer=player1_timer)
            player1_timer.pause_timer()

        first = False
        graphics.draw_prev_board(gameboard=board)
        board.save_board()
        graphics.draw(
            gameboard=board, player1_timer=player1_timer, player2_timer=player2_timer
        )
        input_handler.ask_to_take_turn(player=player_white, timer=player2_timer)
        player2_timer.pause_timer()

        if (
            player1_timer.check_remaining_time() > 0
            and player2_timer.check_remaining_time() > 0
        ):
            playing = True
        else:
            playing = False
            print("Timeout!!!! Game ends!!!!")
            return

if __name__ == "__main__":
    print("Running main()...")
    main()
    print("Exiting...")
    exit()
