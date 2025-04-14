from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell
from .CellType import CellType
import random


class BoardGenerator:
    """
    KakuroBoard factory class that can generate preset or random boards
    """

    @staticmethod
    def generate_board(difficulty):
        # Randomly decide whether to use a preset or random board (80% chance of random)
        use_random = random.random() < 0.8

        if use_random:
            return BoardGenerator.generate_random_board(difficulty)
        else:
            # Use preset boards for fallback
            if difficulty == "easy":
                return BoardGenerator.generate_easy_board()
            elif difficulty == "medium":
                return BoardGenerator.generate_medium_board()
            elif difficulty == "hard":
                return BoardGenerator.generate_hard_board()

    @staticmethod
    def generate_random_board(difficulty):
        """Generate a randomized Kakuro board of the specified difficulty"""

        # Set dimensions based on difficulty
        if difficulty == "easy":
            rows, cols = 4, 4
        elif difficulty == "medium":
            rows, cols = 5, 5
        else:  # hard
            rows, cols = 6, 6

        # Initialize an empty board with BlockCells
        board = [[BlockCell() for _ in range(cols)] for _ in range(rows)]

        # Create a random pattern for the puzzle
        board = BoardGenerator._create_board_pattern(board, rows, cols, difficulty)

        # Assign sums to make the board solvable
        board = BoardGenerator._assign_sum_values(board, rows, cols)

        return board

    @staticmethod
    def _create_board_pattern(board, rows, cols, difficulty):
        """Create the underlying pattern of the Kakuro board"""

        # Top row and left column are always blocks
        for i in range(rows):
            for j in range(cols):
                if i == 0 or j == 0:
                    board[i][j] = BlockCell()

        # Place SumCells and NumberCells according to difficulty
        if difficulty == "easy":
            min_clues = 2
            max_run_length = 3  # Maximum consecutive number cells
        elif difficulty == "medium":
            min_clues = 3
            max_run_length = 4
        else:  # hard
            min_clues = 4
            max_run_length = 5

        # Place initial SumCells
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Randomly decide if this should be a SumCell
                if random.random() < 0.3:  # 30% chance
                    board[i][j] = SumCell(None, None)  # Temporary sums

        # Fill in NumberCells
        for i in range(1, rows):
            for j in range(1, cols):
                # If it's a BlockCell, consider making it a NumberCell
                if isinstance(board[i][j], BlockCell):
                    # Check if there's a SumCell to the left or above
                    has_sum_left = j > 0 and isinstance(board[i][j - 1], SumCell)
                    has_sum_above = i > 0 and isinstance(board[i - 1][j], SumCell)

                    if has_sum_left or has_sum_above:
                        board[i][j] = NumberCell(0)  # Empty cell to be filled by player

        # Verify we have the minimum number of clues
        sum_count = sum(1 for i in range(rows) for j in range(cols) if isinstance(board[i][j], SumCell))

        if sum_count < min_clues:
            # Try again if we don't have enough clues
            return BoardGenerator._create_board_pattern(
                [[BlockCell() for _ in range(cols)] for _ in range(rows)],
                rows, cols, difficulty
            )

        return board

    @staticmethod
    def _assign_sum_values(board, rows, cols):
        """Assign sum values to SumCells to make the puzzle solvable"""

        # First, create a valid solution
        solution = [[0 for _ in range(cols)] for _ in range(rows)]

        # Assign random values (1-9) to each NumberCell
        for i in range(rows):
            for j in range(cols):
                if isinstance(board[i][j], NumberCell):
                    solution[i][j] = random.randint(1, 9)

        # Now compute the sums for each SumCell
        for i in range(rows):
            for j in range(cols):
                if isinstance(board[i][j], SumCell):
                    # Calculate the right sum
                    right_sum = None
                    col_idx = j + 1
                    right_cells = []

                    while col_idx < cols and isinstance(board[i][col_idx], NumberCell):
                        right_cells.append(solution[i][col_idx])
                        col_idx += 1

                    if right_cells:
                        right_sum = sum(right_cells)

                    # Calculate the down sum
                    down_sum = None
                    row_idx = i + 1
                    down_cells = []

                    while row_idx < rows and isinstance(board[row_idx][j], NumberCell):
                        down_cells.append(solution[row_idx][j])
                        row_idx += 1

                    if down_cells:
                        down_sum = sum(down_cells)

                    # Update the SumCell with calculated values
                    board[i][j] = SumCell(down_sum, right_sum)

        return board

    @staticmethod
    def generate_easy_board():
        """Generate a predefined easy board (fallback)"""
        return [
            [BlockCell(), SumCell(6, None), SumCell(19, None), BlockCell()],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), SumCell(5, None)],
            [SumCell(None, 10), NumberCell(0), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(None, 6), NumberCell(0), NumberCell(0)]
        ]

    @staticmethod
    def generate_medium_board():
        """Generate a predefined medium board (fallback)"""
        return [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(10, None), SumCell(8, None)],
            [BlockCell(), BlockCell(), SumCell(8, 6), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(7, 8), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), BlockCell()],
            [SumCell(None, 5), NumberCell(0), NumberCell(0), BlockCell(), BlockCell()]
        ]

    @staticmethod
    def generate_hard_board():
        """Generate a predefined hard board (fallback)"""
        return [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(7, None), SumCell(16, None), SumCell(16, None)],
            [BlockCell(), SumCell(23, None), SumCell(11, 11), NumberCell(0), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(16, 15), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 17), NumberCell(0), NumberCell(0), NumberCell(0), SumCell(11, 6), NumberCell(0)],
            [SumCell(None, 11), NumberCell(0), NumberCell(0), BlockCell(), SumCell(None, 6), NumberCell(0)]
        ]