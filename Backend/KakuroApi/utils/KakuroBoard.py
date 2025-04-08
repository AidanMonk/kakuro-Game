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

    def set_board(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def set_number(self, row, column, value):
        if isinstance(self.board[row][column], NumberCell):
            self.board[row][column].value = value
        else:
            print("set_number_error - cell is not a number")

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