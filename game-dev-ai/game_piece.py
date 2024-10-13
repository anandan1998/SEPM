class game_piece:

    color: int  # Black = 0, white = 1 since Black goes first!
    black: int = 0
    white: int = 1
    is_flat : bool

    def __init__(self, color : int, is_flat : bool):
        self.color = color
        self.is_flat = is_flat

if __name__ == "__main__":
    print("This could be used to run tests...")
    print("Exiting... Please run from Main.py")
    exit()
