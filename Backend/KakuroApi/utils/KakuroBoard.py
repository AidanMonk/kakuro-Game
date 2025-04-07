from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell
from .CellType import CellType
from .BoardGenerator import BoardGenerator
from .KakuroValidator import KakuroValidator
import random

class KakuroBoard:
    def __init__(self):
        self.board = []

    def select_board(self, difficulty="medium"):

        if difficulty == "easy":
            self.board = BoardGenerator.generate_easy_board()
        elif difficulty == "medium":
            self.board = BoardGenerator.generate_medium_board()
        elif difficulty == "hard":
            self.board = BoardGenerator.generate_hard_board()
        else:
            # Default to medium if invalid difficulty is provided
            self.board = BoardGenerator.generate_medium_board()

        print(self)

    def set_board(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def set_number(self, row, column, value):
        if isinstance(self.board[row][column], NumberCell):
            self.board[row][column].value = value
        else:
            print("set_number_error - cell is not a number")

    @staticmethod
    def validate_answers(board):
        """
        Validate the board solution based on difficulty level
        """
        # Simple check if all cells are filled
        for row in board:
            for cell in row:
                if isinstance(cell, NumberCell) and cell.value == 0:
                    return False
                
        return KakuroValidator.validate_answers(board)

        '''
        # Determine which board we're dealing with based on dimensions and structure
        if len(board) == 4:  # Easy board
            return KakuroBoard._validate_easy_board(board)
        elif len(board) == 5:  # Medium board
            return KakuroBoard._validate_medium_board(board)
        elif len(board) == 6:  # Hard board
            return KakuroBoard._validate_hard_board(board)
        '''

        return False  # Unknown board layout

    @staticmethod
    def _validate_easy_board(board):
        """Validate the easy board solution"""
        expected = [
            [0, 0, 0, 0],            # Row 0
            [0, 0, 7, 6],            # Row 1
            [0, 5, 3, 4],            # Row 2
            [0, 3, 5, 0]             # Row 3
        ]

        # Check number cells match expected values
        for r in range(len(board)):
            for c in range(len(board[0])):
                if isinstance(board[r][c], NumberCell) and expected[r][c] != 0:
                    if board[r][c].value != expected[r][c]:
                        return False

        return True

    @staticmethod
    def _validate_medium_board(board):
        """Validate the medium board solution"""
        # Check specific cells for the medium board (5x5)

        # Row 1 (cells 3-4) should be [7, 9]
        if board[1][3].value != 7 or board[1][4].value != 9:
            return False

        # Row 2 (cells 1-4) should be [3, 5, 2, 6]
        expected_row2 = [3, 5, 2, 6]
        for i in range(4):
            if board[2][i + 1].value != expected_row2[i]:
                return False

        # Row 3 (cells 1-4) should be [9, 4, 1, 3]
        expected_row3 = [9, 4, 1, 3]
        for i in range(4):
            if board[3][i + 1].value != expected_row3[i]:
                return False

        # Row 4 (cells 1-2) should be [5, 9]
        if board[4][1].value != 5 or board[4][2].value != 9:
            return False

        # If all checks pass, the solution is valid
        return True

    @staticmethod
    def _validate_hard_board(board):
        """Validate the hard board solution (6x6)"""
        # The expected solution for the hard board
        expected_values = [
            # Row 1 (indices 3-5)
            [1, 2, 4],
            # Row 2 (indices 2-4)
            [7, 1, 3],
            # Row 3 (indices 1-5)
            [5, 4, 3, 2, 1],
            # Row 4 (indices 1-4, 5)
            [6, 3, 5, 3, 6],
            # Row 5 (indices 1-2, 4)
            [4, 7, 6]
        ]

        # Check Row 1 (board[1][3] through board[1][5])
        for i in range(3):
            if board[1][i + 3].value != expected_values[0][i]:
                return False

        # Check Row 2 (board[2][2] through board[2][4])
        for i in range(3):
            if board[2][i + 2].value != expected_values[1][i]:
                return False

        # Check Row 3 (board[3][1] through board[3][5])
        for i in range(5):
            if board[3][i + 1].value != expected_values[2][i]:
                return False

        # Check Row 4 (board[4][1] through board[4][4], and board[4][5])
        for i in range(4):
            if board[4][i + 1].value != expected_values[3][i]:
                return False
        if board[4][5].value != expected_values[3][4]:
            return False

        # Check Row 5 (board[5][1], board[5][2], and board[5][4])
        if board[5][1].value != expected_values[4][0] or board[5][2].value != expected_values[4][1] or board[5][
            4].value != expected_values[4][2]:
            return False

        # If all checks pass, the solution is valid
        return True

    def serialize(self):
        result = []
        for row in self.board:
            new_row = []
            for cell in row:
                new_row.append(cell.to_dict())
            result.append(new_row)
        return result

    @staticmethod
    def deserialize(board_json):
        deserialized_board = KakuroBoard()

        deserialized_board.board = [[None] * len(board_json[0]) for _ in range(len(board_json))]

        for row_index, row_data in enumerate(board_json):
            for col_index, cell_data in enumerate(row_data):
                cell_type = cell_data.get('type')
                print(cell_data)

                if cell_type == 'block':
                    deserialized_board.board[row_index][col_index] = BlockCell()

                elif cell_type == 'sum':
                    right_sum = cell_data.get('right_sum')
                    down_sum = cell_data.get('down_sum')
                    deserialized_board.board[row_index][col_index] = SumCell(down_sum, right_sum)

                elif cell_type == 'number':
                    value = cell_data.get('value')
                    deserialized_board.board[row_index][col_index] = NumberCell(value)

        return deserialized_board

    def __str__(self):
        board_str = ""
        for row in self.board:
            row_str = []
            for cell in row:
                if isinstance(cell, BlockCell):
                    row_str.append(" ██ ")  # Blocked cells as solid squares
                elif isinstance(cell, SumCell):
                    if cell.right_sum is None:
                        row_str.append(f"/{cell.down_sum}")
                    elif cell.down_sum is None:
                        row_str.append(f"{cell.right_sum}/")
                    else:
                        row_str.append(f"{cell.down_sum} / {cell.right_sum}")

                elif isinstance(cell, NumberCell):
                    row_str.append(f"  {cell.value}  ")  # Empty number cell
            board_str += " | ".join(row_str) + "\n"
        return board_str