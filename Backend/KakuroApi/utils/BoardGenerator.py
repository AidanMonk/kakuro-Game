from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell
from .CellType import CellType

class BoardGenerator:
    #KakuroBoard factory class

    @staticmethod
    def generate_board(difficulty):
        if difficulty == "easy":
            return BoardGenerator.generate_easy_board()
        elif difficulty == "medium":
            return BoardGenerator.generate_medium_board()
        elif difficulty == "hard":
            return BoardGenerator.generate_hard_board()

    @staticmethod
    def generate_easy_board():
        return [
            [BlockCell(), SumCell(6,None), SumCell(19, None), BlockCell()],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), SumCell(5, None)],
            [SumCell(None, 10), NumberCell(0), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(None, 6), NumberCell(0), NumberCell(0)]
        ]

    @staticmethod   
    def generate_medium_board():
        return [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(10, None), SumCell(8, None)],
            [BlockCell(), BlockCell(), SumCell(8, 6), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(7, 8), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), BlockCell()],
            [SumCell(None, 5), NumberCell(0), NumberCell(0), BlockCell(), BlockCell()]
        ]

    @staticmethod
    def generate_hard_board():
        return [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(7, None), SumCell(16, None), SumCell(16, None)],
            [BlockCell(), SumCell(23, None), SumCell(11, 11), NumberCell(0), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(16, 15), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 17), NumberCell(0), NumberCell(0), NumberCell(0), SumCell(11, 6), NumberCell(0)],
            [SumCell(None, 11), NumberCell(0), NumberCell(0), BlockCell(), SumCell(None, 6), NumberCell(0)]
        ]