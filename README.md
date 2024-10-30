# UU Game

This project is a 1v1 board game called "UU Game," designed to be played between a human player and an AI opponent. The AI operates on a minimax algorithm with alpha-beta pruning for efficient decision-making. The game objective is to create an uninterrupted path from one side of the game board to the opposite side, with only orthogonally connected (not diagonal) pieces counting toward this path. Our version pre integration is located in the pygame directory, the integrated version is located in the game-dev-ai directory. Note, instructions to play the game version integrated with the other group is available once you start the game.

---

## Table of Contents
- [Game Rules and Objectives](#game-rules-and-objectives)
- [Installation](#installation)

### Game Rules and Objectives
- **Objective**: Each player aims to create an unbroken path across the game board, connecting opposite sides with their pieces.
- **Connectivity**: Only orthogonally (non-diagonally) adjacent pieces count towards the path.
  
**Piece Types**:
- **Flat Piece**: A standard piece placed by left-clicking on a square.
- **Standing Piece**: Standing pieces acts as "blockers" and do not count towards making the path and are invoked by right clicking on a square.

**Move operation**:
1. Player can mark a square they control by hovering the square with the mouse and pressing space
2. The player can then press num keys 1 through 4 to select the amount of pieces to be moved
3. To actually move the pieces once they are selected, the player needs to hover the mouse over the destination square and press space again

### Installation
To run the pre integration version, ensure pygame is installed on your system, then execute python3.x (where x is your version of python3) engine.py.
If pygame isn't installed, you can install it using pip. 

To run the integrated version of the game, execute python3.x (where x is your version of python3) main.py
