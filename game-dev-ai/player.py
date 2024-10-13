class player:

    black: int = 0
    white: int = 1

    color: int

    remaining_pieces: int = 15

    def __init__(self, color: int):
        self.color = color


if __name__ == "__main__":
    print("This could be used to run tests...")
    print("Exiting... Please run from Main.py")
    exit()
