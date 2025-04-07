from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell

class KakuroValidator():
    @staticmethod
    def validate_answers(board):
        #check rows
        is_valid = True
        #check horizontally
        for x in range(len(board[0])):
            target_sum = 0
            current_sum = 0 
            count_mode = False
            for y in range(len(board)):
                cell = board[x][y]
                if count_mode:
                    if type(cell) == NumberCell:
                        current_sum += cell.value
                        print("Current sum:", current_sum)
                        if y >= len(board) -1:
                            if current_sum != target_sum:
                                print(f"Validation faileda: {current_sum} ≠ {target_sum} at row {x}, column {y}")
                                is_valid = False
                                count_mode = False
                            else:
                                print("Check passed")
                            current_sum = 0
                    elif type(cell) == BlockCell:
                        if current_sum != target_sum:
                            print(f"Validation failedb: {current_sum} ≠ {target_sum} at row {x}, column {y}")
                            is_valid = False
                        else:
                            print("Check passed")
                            count_mode = False
                        current_sum = 0  
                    elif type(cell) == SumCell:  
                        if current_sum != target_sum:
                            print(f"Validation failedc: {current_sum} ≠ {target_sum} at row {x}, column {y}")
                            is_valid = False
                            count_mode = False
                        current_sum = 0  
                        if cell.right_sum is not None:
                            target_sum = cell.right_sum
                            count_mode = True
                        print("New target sum:", target_sum)
                else:  # count_mode is False
                    if type(cell) == SumCell:
                        if cell.right_sum is not None:
                            print(cell.right_sum)
                            target_sum = cell.right_sum
                            count_mode = True
                            current_sum = 0  # Reset sum for the new count
                            print("New target sum:", target_sum)
            print("-- End of row --")
        #check columns
        for y in range(len(board)):
            target_sum = 0
            current_sum = 0 
            count_mode = False
            for x in range(len(board[0])):
                cell = board[x][y]
                if count_mode:
                    if type(cell) == NumberCell:
                        current_sum += cell.value
                        print("Current sum:", current_sum)
                        if x >= len(board) -1:
                            if current_sum != target_sum:
                                print(f"Validation failedd: {current_sum} ≠ {target_sum} at row {x}, column {y}")
                                is_valid = False
                                count_mode = False
                            else:
                                print("Check passed")
                            current_sum = 0
                    elif type(cell) == BlockCell:
                        if current_sum != target_sum:
                            print(f"Validation failede: {current_sum} ≠ {target_sum} at row {x}, column {y}")
                            is_valid = False
                        else:
                            print("Check passed")
                            count_mode = False
                        current_sum = 0  
                    elif type(cell) == SumCell:  
                        if current_sum != target_sum:
                            print(f"Validation failedf: {current_sum} ≠ {target_sum} at row {x}, column {y}")
                            is_valid = False
                            count_mode = False
                        current_sum = 0  
                        if cell.down_sum is not None:
                            target_sum = cell.down_sum
                            count_mode = True
                        print("New target sum:", target_sum)
                else:  # count_mode is False
                    if type(cell) == SumCell:
                        if cell.down_sum is not None:
                            target_sum = cell.down_sum
                            count_mode = True
                            current_sum = 0  # Reset sum for the new count
                            print("New target sum:", target_sum)
            print("-- End of column --")
        return is_valid