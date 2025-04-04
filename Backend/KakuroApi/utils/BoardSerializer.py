from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell
from .KakuroBoard import KakuroBoard

class BoardSerializer:
    @staticmethod
    def serialize(board):
        result = []
        for row in board:
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
        print(deserialized_board)
        return deserialized_board
