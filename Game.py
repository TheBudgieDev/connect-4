"""
Module that contains the Connect 4 game class.
"""

from os import system, name
from sys import stdout
from time import sleep
from enum import Enum
from TextFormatting import format_text, Colours, Styles, BGColours


# Different size modes besides S_7x6 are unused for various reasons:
# 1) Gameplay for most of the non-default sizes I found to be worse (especially the smaller ones)
# 2) The AI would need to be much more modular, which is doable but will make it much slower than it already is
class Size(Enum):
    """
    Enum class that stores tuples of the different Connect 4 size configurations.
    """

    S_7x6 = (7, 6)
    S_5x4 = (5, 4)
    S_6x5 = (6, 5)
    S_8x7 = (8, 7)
    S_8x8 = (8, 8)
    S_9x6 = (9, 6)
    S_9x7 = (9, 7)
    S_10x7 = (10, 7)


# Non-default gamemodes are unused since most of them would require their own AI which is too time-consuming
class Mode(Enum):
    """
    Enum class that stores the different Connect 4 gamemodes.
    """

    NORMAL = 0
    # POPOUT = 1
    # POP10 = 2
    # FIVE = 3
    # POWERUP = 4


class Board:
    size = ()
    """Tuple that stores the dimensions of the Connect 4 board"""
    mode = None
    """The type of gamemode the Connect 4 game is in"""
    player_first = True
    """Whether the player goes first"""
    data = []
    """2-Dimensional array that stores the Connect 4 board data"""
    difficulty = 0
    """The difficulty of the computer player"""

    def __init__(self, size: Size = Size.S_7x6, mode: Mode = Mode.NORMAL, player_first: bool = True):
        """
        Console Connect 4 Class

        Arguments:
            size (Size): The type of Connect 4 size configuration
            mode (Mode): The gamemode of the Connect 4 game
            player_first (bool): Whether the player goes first
        """

        self.size = size.value
        self.mode = mode
        self.player_first = player_first
        self.data = [[' ⚫  ' for _ in range(self.size[1])] for _ in range(self.size[0])]

    def drop(self, column: int, char: str) -> bool:
        """
        Method that adds a Connect 4 move to the given column. Returns True if the move is valid.

        Parameters:
            column (int): The column to drop the Connect 4 piece
            char (str): The type of character to drop
        """

        target_idx = -1
        # Find the lowest empty slot in the column
        for i in range(self.size[1] - 1, -1, -1):
            if self.data[column][i] == ' ⚫  ':
                target_idx = i
                break

        # Check if the column is full
        if target_idx < 0:
            return False

        # Animate the piece dropping
        for j in range(target_idx):
            self.data[column][j] = char
            stdout.write(str(self))
            sleep(0.1)
            self.data[column][j] = ' ⚫  '
        self.data[column][target_idx] = char
        return True

    def check_connect(self, x: int, y: int, char: str) -> bool:
        """
        Method that returns whether a connection of 4 was made at the given position with the given character

        Parameters:
            x (int): The x-coordinate of the piece
            y (int): The y-coordinate of the piece
            char (str): The character that the piece is on the board
        """

        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal /
            [(1, -1), (-1, 1)]  # Diagonal \
        ]

        # Check in all directions
        for direction in directions:
            # Start with the current piece
            count = 1
            # Store the pieces in the connection. Used to turn them white if a win is detected
            pieces = [(x, y)]
            # Check in both directions for each direction pair
            for dx, dy in direction:
                # Start counting from the first step away from the current piece
                step = 1
                while True:
                    # Calculate the position of the next piece to check
                    nx, ny = x + dx * step, y + dy * step
                    # Check if the position is in bounds and the character matches
                    if 0 <= nx < len(self.data) and 0 <= ny < len(self.data[0]) and self.data[nx][ny] == char:
                        count += 1
                        pieces.append((nx, ny))
                    # If the position is out of bounds or the character doesn't match, stop checking in that direction
                    else:
                        break
                    step += 1

            # Check for four in a row
            if count >= 4:
                # Turn the winning pieces white
                for i in range(len(pieces)):
                    self.data[pieces[i][0]][pieces[i][1]] = format_text(self.data[pieces[i][0]][pieces[i][1]], bg_colour=BGColours.WHITE)
                return True
        return False

    def copy(self) -> 'Board':
        """
        Creates a copy of the board.
        """

        new_board = Board(size=Size(self.size), mode=self.mode, player_first=self.player_first)

        # Copy the data manually to sever connection between the two boards
        new_board.data = []
        for col in range(self.size[0]):
            new_board.data.append(self.data[col][:])
        return new_board

    def __str__(self):
        """
        Returns a string representation of the board
        """

        # Clear the console
        system('cls' if name == 'nt' else 'clear')

        # Format the board to be blue and bolded
        grid = format_text("\033[1m" + "|", colour=Colours.BLUE, style=Styles.UNDERLINE)

        # Add the column numbers on the top
        for l in range(1, self.size[0] + 1):
            grid += format_text("\033[1m" + f"  {l}  |", colour=Colours.BLUE, style=Styles.UNDERLINE)
        grid += "\n"

        # Add the board data
        for i in range(1, (self.size[1] * 2) + 2):
            for j in range(1, (self.size[0] * 2) + 2):
                if i % 2 == 0 and j % 2 == 0:
                    grid += self.data[int(j * 0.5 - 1)][int(i * 0.5 - 1)]
                elif i % 2 == 0 and j % 2 != 0:
                    grid += format_text("|", colour=Colours.BLUE, style=Styles.BOLD)
                elif i % 2 != 0 and j % 2 == 0:
                    grid += format_text('——————', colour=Colours.BLUE, style=Styles.BOLD)
            if i % 2 != 0:
                grid += format_text('|', colour=Colours.BLUE, style=Styles.BOLD)
            grid += "\n"

        # Add the column numbers on the bottom
        grid += format_text('|', colour=Colours.BLUE, style=Styles.BOLD)
        for l in range(1, self.size[0] + 1):
            grid += format_text("\033[1m" + f"  {l}  |", colour=Colours.BLUE, style=Styles.UNDERLINE)
        grid += "\n\n"

        return grid

    # Unused method used for the POPOFF gamemode. Still kept as that gamemode is the best one besides normal
    # def pop(self, column: int, char: str) -> bool:
    #     """
    #     Method that pops a Connect 4 piece from the bottom. Used for the POPOUT mode. Returns True if the move is valid.
    #
    #     Parameters:
    #         column (int): The column to pop out the Connect 4 piece
    #         char (str): The type of character that wants to be popped
    #     """
    #
    #     if self.data[column][self.size[1] - 1] != char:
    #         print("Cannot pop off that column because your piece is not at the bottom!")
    #         return False
    #
    #     target_idx = 0
    #
    #     for i in range(self.size[1], 0, -1):
    #         if self.data[column][i - 1] == ' ⚫  ':
    #             target_idx = i - 1
    #             break
    #
    #     self.data[column][self.size[1] - 1] = ' ⚫  '
    #     for j in range(self.size[1] - 1, target_idx - 1, -1):
    #         self.data[column][j] = self.data[column][j - 1]
    #         self.data[column][j - 1] = ' ⚫  '
    #         stdout.write(str(self))
    #         sleep(0.1)
    #     return True
