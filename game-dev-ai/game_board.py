from game_piece import game_piece
from loguru import logger

class game_board:

    board = []
    prev_board: list = []
    max_stack_size: int = 5
    board_size: int = 4

    def __init__(self):
        self.board = []
        for _ in range(self.board_size):
            row = [[] for _ in range(self.board_size)]
            self.board.append(row)

    # Maybe remove before finishing - Not used right now
    def display(self):
        print(str(self.board))

    def save_board(self):
        self.prev_board = []

        for row in self.board:
            row_state = []
            for position in row:
                if position:
                    temp2 = []
                    for piece in position:
                        if piece.is_flat:
                            temp2.append(piece.color)
                        else:
                            temp2.append(3 if piece.color == 0 else 4)

                    row_state.append(temp2)
                else:
                    row_state.append([])

            self.prev_board.append(row_state)

    """
    def place_piece(self, piece, x, y) -> bool:
    
        Places a game_piece object onto the stack at the specified position.

        piece : game_piece 
            A game_piece object to be added onto the stack at the specified position.
        x : int
            X-coordinate of the specified position.
        y : int
            Y-coordinate of the specified position.

        returns: success-state : bool
    """

    def place_piece(self, piece: game_piece, x: int, y: int, suppress_output=False) -> bool:

        if not self.validate_coordinate(x, y):
            return False  # The entered coordinate is not a valid position

        position: list[game_piece] = self.get_position(x, y)  # Get the specified position

        if len(position) > 0:
            if not position[-1].is_flat:
                if not suppress_output:
                    print("Top piece is standing, you may not place here")
                return False

        if len(position) >= self.max_stack_size:
            return False  # Cannot place more than max stack size

        # Place the piece
        self.board[x][y].append(piece)
        return True  # Placement was successful

    """
    def validate_coordinate(self, x : int, y : int) -> bool:
    
        Checks if a given pair of coordinates x, y is valid for the board.

        x : int
            X coordinate of the specified position.
        y : int
            Y coordinate of the specified position.
        
        returns: success-state : bool
    """

    def validate_coordinate(self, x: int, y: int) -> bool:
        if x >= self.board_size or x < 0:  # Is x out of range?
            return False
        if y >= self.board_size or y < 0:  # Is y out of range?
            return False

        return True  # Neither was out of range so return True for the success.

    """
    def get_position(self, x, y) -> list[game_piece]:

        Gets the pieces / stack at the specified game position.

        x : int
            X coordinate of the specified position.
        y : int
            Y coordinate of the specified position.

        returns: position / stack : list[game_piece]
    """

    def get_position(self, x: int, y: int) -> list:
        if not self.validate_coordinate(x, y):
            raise Exception(
                "Error: "
                + str(x)
                + ", "
                + str(y)
                + " is not a valid coordinate for the board."
            )

        return self.board[x][y]  # Return the stack at the position x, y

    """
    def move_position(self, old_x : int, old_y : int, target_x : int, target_y : int) -> bool:
    
        Tries to move the stack at (old_x, old_y) to the stack at (target_x, target_y).

        old_x : int
            X coordinate of the specified position.
        old_y : int
            Y coordinate of the specified position.
        target_x : int
            X coordinate of the specified position.
        target_y : int
            Y coordinate of the specified position.

        returns: success-state : bool
    """

    def move_position(
        self, old_x: int, old_y: int, target_x: int, target_y: int, suppress_output=False
    ) -> bool:
        if not self.validate_coordinate(old_x, old_y):
            return False  # Not valid
        if not self.validate_coordinate(target_x, target_y):
            return False  # Not valid

        old_position: list[game_piece] = self.get_position(old_x, old_y)

        n_old_pieces: int = len(old_position)

        if n_old_pieces <= 0:
            if not suppress_output:
                print("No pieces to move.")
            return False  # Fail if moving no pieces

        if not self.check_position_has_room_for(
            target_x, target_y, n_old_pieces
        ):
            if not suppress_output:
                print("Not enough room at target position.")
            return False  # Fail if there is no room at the target position

        target_position: list[game_piece] = self.get_position(target_x, target_y)

        # Check if moving onto a standing piece
        if len(target_position) > 0 and not target_position[-1].is_flat:
            if not suppress_output:
                print("Cannot move onto a standing piece.")
            return False

        # Move the stack
        self.board[target_x][target_y].extend(old_position)
        self.board[old_x][old_y] = []

        return True  # Move was successful

    """
    def split_position(self, old_x : int, old_y : int, target_x : int, target_y : int, count : int) -> bool:
    
        Tries to move (count) pieces from the stack at (old_x, old_y) to the stack at (target_x, target_y).

        old_x : int
            X coordinate of the specified position.
        old_y : int
            Y coordinate of the specified position.
        target_x : int
            X coordinate of the specified position.
        target_y : int
            Y coordinate of the specified position.

        returns: success-state : bool
    """

    def split_position(
        self, old_x: int, old_y: int, target_x: int, target_y: int, count: int, suppress_output=False
    ) -> bool:
        if not self.validate_coordinate(old_x, old_y):
            return False  # Not valid
        if not self.validate_coordinate(target_x, target_y):
            return False  # Not valid
        if count <= 0:
            if not suppress_output:
                print("Must move at least one piece.")
            return False  # Not valid
        if count > self.max_stack_size:
            if not suppress_output:
                print("Cannot move more than max stack size.")
            return False  # Not valid

        old_position: list[game_piece] = self.get_position(old_x, old_y)
        n_old_pieces: int = len(old_position)

        if count > n_old_pieces:
            if not suppress_output:
                print("Not enough pieces to move.")
            return False  # Not valid

        if not self.check_position_has_room_for(
            target_x, target_y, count
        ):
            if not suppress_output:
                print("Not enough room at target position.")
            return False  # Fail if there is no room at the target position

        target_position: list[game_piece] = self.get_position(target_x, target_y)

        # Before moving, check if the top piece on the target stack is standing
        if len(target_position) > 0 and not target_position[-1].is_flat:
            if not suppress_output:
                print("Cannot move onto a standing piece.")
            return False

        pieces_to_move = old_position[-count:]  # Take the top 'count' pieces
        new_old_position = old_position[:-count]  # Remaining pieces

        # Move the pieces
        self.board[target_x][target_y].extend(pieces_to_move)
        self.board[old_x][old_y] = new_old_position

        return True

    def check_winning_condition(self, player_color: int) -> bool:
        """Checks if the given player has won by having a connected line of flat pieces."""
        # Check for horizontal win (start from the left side)
        for row in range(self.board_size):
            if self.dfs(row, 0, player_color, "horizontal", set()):
                return True

        # Check for vertical win (start from the top side)
        for col in range(self.board_size):
            if self.dfs(0, col, player_color, "vertical", set()):
                return True

        return False

    def dfs(
        self, x: int, y: int, player_color: int, direction: str, visited: set
    ) -> bool:
        """Performs a depth-first search (DFS) to check if there is a snake-like winning path."""
        # If the current position is out of bounds, return False
        if not self.validate_coordinate(x, y):
            return False

        # If we've already visited this position, return False
        if (x, y) in visited:
            return False

        # Get the current position's stack of pieces
        position = self.get_position(x, y)

        # If the stack is empty, or the top piece is not flat, or the piece color doesn't match, return False
        if (
            len(position) == 0
            or not position[-1].is_flat
            or position[-1].color != player_color
        ):
            return False

        # If we are on the last column/row and in the correct direction, the player has won
        if direction == "horizontal" and y == self.board_size - 1:
            return True
        if direction == "vertical" and x == self.board_size - 1:
            return True

        # Mark this position as visited
        visited.add((x, y))

        # Explore all adjacent positions (up, down, left, right)
        return (
            self.dfs(x, y + 1, player_color, direction, visited)  # Right
            or self.dfs(x, y - 1, player_color, direction, visited)  # Left
            or self.dfs(x + 1, y, player_color, direction, visited)  # Down
            or self.dfs(x - 1, y, player_color, direction, visited)  # Up
        )

    """
    def check_position_empty(self, x : int, y : int) -> bool:
        
        Checks if a position is empty or not.

        x : int
            X coordinate of the specified position.
        y : int
            Y coordinate of the specified position.

        returns: success-state : bool
    """

    def check_position_empty(self, x: int, y: int) -> bool:
        position: list[game_piece] = self.get_position(x, y)  # Validates the position
        return len(position) == 0

    """
    def check_position_has_room_for(self, x : int, y : int, count : int) -> bool:
        
        Checks if the position has room for (count) many pieces.

        x : int
            X coordinate of the specified position.
        y : int
            Y coordinate of the specified position.
        count : int
            Count of pieces to check if they fit.
        
        returns: success-state : bool
    """

    def check_position_has_room_for(self, x: int, y: int, count: int) -> bool:
        if count > self.max_stack_size or count < 0:
            return False  # Impossible to fit more than max stack size or negative number of pieces.
        position: list[game_piece] = self.get_position(x, y)  # Validates the position
        return len(position) + count <= self.max_stack_size


if __name__ == "__main__":
    print("This could be used to run tests...")
    print("Exiting... Please run from Main.py")
    exit()
