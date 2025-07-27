"""
Module that contains the Connect 4 AI class.
"""

from math import inf
from random import choice
from Game import Board


class Connect4AI:
    def __init__(self, board: Board, depth: int = 4):
        """
        Connect 4 AI Class

        Parameters:
            board (Board): The current board state
            depth (int): The depth of the minimax search
        """

        self.board = board
        """The current board state"""
        self.depth = depth
        """The depth of the minimax search"""
        self.WEIGHT = [
            [3, 4, 5, 5, 4, 3],
            [4, 6, 8, 8, 6, 4],
            [5, 8, 11, 11, 8, 5],
            [7, 10, 13, 13, 10, 7],
            [5, 8, 11, 11, 8, 5],
            [4, 6, 8, 8, 6, 4],
            [3, 4, 5, 5, 4, 3]
        ]
        """The weight matrix to influence the score"""
        self.DIRECTIONS = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal /
            [(1, -1), (-1, 1)]  # Diagonal \
        ]
        """The directions to check for pieces"""

    def score_pos(self, board: Board) -> int:
        """
        Method that scores the current position of the board.

        Parameters:
            board (Board): The current board state
        """

        score = 0
        rows = self.get_open_rows(board)
        columns = self.get_valid_locations(board)

        for col in columns:
            for row in rows:
                # Evaluate the current position for both pieces
                score += self.evaluate_position(board, col, row, ' 🟡  ')
                score -= self.evaluate_position(board, col, row, ' 🔴  ')

                # Use the weight matrix to influence score
                score += self.WEIGHT[col][row]
        return score

    def evaluate_position(self, board: Board, col: int, row: int, piece: str) -> int:
        """
        Evaluate the score of the position for a specific piece.

        Parameters:
            board (Board): The current board state
            col (int): The column to check
            row (int): The row to check
            piece (str): The piece to check
        """

        score = 0

        # Count pieces in row/column/diagonal for threat levels
        for direction in self.DIRECTIONS:
            line_count = self.count_in_line(board, col, row, piece, direction)
            # Reward moderately for completion of three in a row
            if line_count == 3:
                score += 50
            # Reward slightly for completion of two in a row
            elif line_count == 2:
                score += 10
        return score

    @staticmethod
    def count_in_line(board: Board, col: int, row: int, piece: str, direction: list) -> int:
        """
        Count the number of pieces in a given direction.

        Parameters:
            board (Board): The current board state
            col (int): The column to check
            row (int): The row to check
            piece (str): The piece to check
            direction (list): The direction to check
        """
        count = 0
        for dx, dy in direction:
            step = 1
            while True:
                nx, ny = col + dx * step, row + dy * step
                if 0 <= nx < board.size[0] and 0 <= ny < board.size[1]:
                    if board.data[nx][ny] == piece:
                        count += 1
                    else:
                        break
                else:
                    break
                step += 1
        return count

    def can_win_next(self, board: Board, col: int, row: int, piece: str) -> bool:
        """
        Check if placing the piece in the given column and row would result in a win.

        Parameters:
            board (Board): The current board state
            col (int): The column to check
            row (int): The row to check
            piece (str): The piece to check for a potential win
        """

        b_copy = board.copy()
        self.drop_piece(b_copy, col, piece)
        return b_copy.check_connect(col, row, piece)

    @staticmethod
    def get_open_rows(board: Board) -> list:
        """
        Method that returns a list of the lowest unpopulated row per column

        Parameters:
            board (Board): The current board state
        """

        rows = []
        for col in range(board.size[0]):
            for row in range(board.size[1] - 1, -1, -1):
                if board.data[col][row] == ' ⚫  ':
                    rows.append(row)
                    break
        return rows

    @staticmethod
    def get_valid_locations(board: Board) -> list:
        """
        Method that returns a list of valid locations to drop a piece in the board.

        Parameters:
            board (Board): The current board state
        """

        valid_locations = []
        for col in range(board.size[0]):
            if board.data[col][0] == ' ⚫  ':
                valid_locations.append(col)
        return valid_locations

    def minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizing_player: bool) -> tuple:
        """
        Minimax algorithm with alpha-beta pruning.

        Parameters:
            board (Board): The current board state
            depth (int): The depth of the search
            alpha (int): The alpha value for pruning
            beta (int): The beta value for pruning
            maximizing_player (bool): Whether the player is maximizing or minimizing
        """

        valid_locations = self.get_valid_locations(board)
        open_rows = self.get_open_rows(board)

        # Base case: Check for immediate win or block
        for i in range(len(valid_locations)):
            col = valid_locations[i]
            open_row = open_rows[i]
            # Check for immediate AI win
            if self.can_win_next(board, col, open_row, ' 🟡  '):
                return col, 1000000
            # Check for immediate opponent win
            elif self.can_win_next(board, col, open_row, ' 🔴  '):
                return col, -1000000

        # List to hold safe columns to explore
        safe_columns = []

        # Check for moves that don't reveal wins
        for i in range(len(valid_locations)):
            col = valid_locations[i]
            open_row = max(open_rows[i] - 1, 0)

            b_copy = board.copy()
            self.drop_piece(b_copy, col, ' 🟡  ')

            # Check if placing here would reveal an immediate win for the opponent or the AI
            if not self.can_win_next(b_copy, col, open_row, ' 🔴  ') and not self.can_win_next(b_copy, col, open_row, ' 🟡  '):
                safe_columns.append(col)

        # If no safe moves, fall back to valid locations
        if not safe_columns:
            safe_columns = valid_locations

        # Check if the depth of the search is zero
        if depth == 0:
            return None, self.score_pos(board)

        # Minimax algorithm
        # ----------------------------------------
        # If maximizing player, find the maximum value
        if maximizing_player:
            value = -inf
            # Choose a random column to start
            best_column = choice(safe_columns)
            # Explore each safe column
            for col in safe_columns:
                # Create a copy of the board and drop a piece
                b_copy = board.copy()
                self.drop_piece(b_copy, col, ' 🟡  ')
                # Recursively call the minimax function
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                # Update the best column and value
                if new_score > value:
                    value = new_score
                    best_column = col
                alpha = max(alpha, value)
                # Pruning
                if alpha >= beta:
                    break
            return best_column, value
        # If minimizing player, find the minimum value
        else:
            value = inf
            # Choose a random column to start
            best_column = choice(safe_columns)
            # Explore each safe column
            for col in safe_columns:
                # Create a copy of the board and drop a piece
                b_copy = board.copy()
                self.drop_piece(b_copy, col, ' 🔴  ')
                # Recursively call the minimax function
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                # Update the best column and value
                if new_score < value:
                    value = new_score
                    best_column = col
                beta = min(beta, value)
                # Pruning
                if alpha >= beta:
                    break
            return best_column, value

    @staticmethod
    def drop_piece(board: Board, col: int, char: str):
        """
        Method that drops a piece in the given column.
        """

        for row in range(board.size[1] - 1, -1, -1):
            if board.data[col][row] == ' ⚫  ':
                board.data[col][row] = char
                break

    def get_best_move(self) -> int:
        """
        Method that returns the best move for the AI.
        """

        column, _ = self.minimax(self.board, self.depth, -inf, inf, True)
        if column is None:
            column = choice(self.get_valid_locations(self.board))
        return column
