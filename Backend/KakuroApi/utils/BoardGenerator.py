from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell
from .CellType import CellType

class BoardGenerator:
    @staticmethod
    def generate_easy_board():
        """Generate a simple 4x4 board for beginners"""
        return [
            [BlockCell(), BlockCell(), SumCell(16, None), SumCell(10, None)],
            [BlockCell(), SumCell(16, 13), NumberCell(0), NumberCell(0)],
            [SumCell(None, 12), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 8), NumberCell(0), NumberCell(0), BlockCell()]
        ]

        # Solution: [[0, 0, 0, 0], [0, 0, 7, 6], [0, 5, 3, 4], [0, 3, 5, 0]]

    @staticmethod   
    def generate_medium_board():
        """Generate a 5x5 board with moderate complexity"""
        return [
            [BlockCell(), BlockCell(), BlockCell(), SumCell(16, None), SumCell(24, None)],
            [BlockCell(), SumCell(23, None), SumCell(16, 16), NumberCell(0), NumberCell(0)],
            [SumCell(None, 16), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 17), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
            [SumCell(None, 14), NumberCell(0), NumberCell(0), BlockCell(), BlockCell()]
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