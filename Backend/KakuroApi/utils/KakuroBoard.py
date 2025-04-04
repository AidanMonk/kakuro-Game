"""
Represents a single game board of Kakuro

Created: 30/01/2025
Author: Aidan Monk
"""

from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell

class KakuroBoard:
    def __init__(self):
        self.board = []

    def generate_board(self):
        #generate a random 4x4 for now
        self.board = [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(19, None), SumCell(22, None)],
            [BlockCell(), SumCell(13, None), SumCell(11, 16), NumberCell(7), NumberCell(9)],
            [SumCell(None, 11), NumberCell(1), NumberCell(2), NumberCell(3), NumberCell(5)],
            [SumCell(None, 21), NumberCell(3), NumberCell(1), NumberCell(9), NumberCell(8)],
            [SumCell(None, 17), NumberCell(9), NumberCell(8), BlockCell(), BlockCell()]
        ]
        print(self)

    def set_board(self, board):
        self.board = board
    

    def get_board(self):
        return self.board
    
    def set_number(self, row, column, value):
        if type(self.board[row][column]) == NumberCell:
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