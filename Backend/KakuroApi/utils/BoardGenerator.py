from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell
from .CellType import CellType

class BoardGenerator:
    @staticmethod
    def generate_easy_board():
        """Generate a simple 4x4 board for beginners"""
        return [
            [BlockCell(), SumCell(6,None), SumCell(19, None), BlockCell()],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), SumCell(5, None)],
            [SumCell(None, 10), NumberCell(0), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(None, 6), NumberCell(0), NumberCell(0)]
        ]

        # Solution: [[0, 0, 0, 0], [0, 0, 7, 6], [0, 5, 3, 4], [0, 3, 5, 0]]

    @staticmethod   
    def generate_medium_board():
        """Generate a 5x5 board with moderate complexity"""
        return [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(10, None), SumCell(8, None)],
            [BlockCell(), BlockCell(), SumCell(8, 6), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(7, 8), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), BlockCell()],
            [SumCell(None, 5), NumberCell(0), NumberCell(0), BlockCell(), BlockCell()]
        ]

        # Solution: [7, 9], [3, 5, 2, 6], [9, 4, 1, 3], [5, 9]

    @staticmethod
    def generate_hard_board():
        """Generate a 6x6 board with higher complexity"""
        return [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(7, None), SumCell(16, None), SumCell(16, None)],
            [BlockCell(), SumCell(23, None), SumCell(11, 11), NumberCell(0), NumberCell(0), NumberCell(0)],
            [BlockCell(), SumCell(16, 15), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 17), NumberCell(0), NumberCell(0), NumberCell(0), SumCell(11, 6), NumberCell(0)],
            [SumCell(None, 11), NumberCell(0), NumberCell(0), BlockCell(), SumCell(None, 6), NumberCell(0)]
        ]