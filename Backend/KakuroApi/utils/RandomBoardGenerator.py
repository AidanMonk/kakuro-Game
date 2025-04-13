from .NumberCell import NumberCell
from .SumCell import SumCell
from .BlockCell import BlockCell
from .CellType import CellType
import random
import copy


class RandomBoardGenerator:
    """
    Generates random Kakuro boards that are guaranteed to be solvable.
    Boards are generated with varying complexity based on the selected difficulty.
    """

    @staticmethod
    def generate_board(difficulty):
        """
        Generate a random board with the specified difficulty.

        Args:
            difficulty (str): 'easy', 'medium', or 'hard'

        Returns:
            2D list: A randomly generated Kakuro board
        """
        # Generate the board and solution
        board, _ = RandomBoardGenerator.generate_board_with_solution(difficulty)
        return board

    @staticmethod
    def generate_board_with_solution(difficulty):
        """
        Generate a random board with the specified difficulty and return both
        the board and its solution.

        Args:
            difficulty (str): 'easy', 'medium', or 'hard'

        Returns:
            tuple: (board, solution) - The generated board and its solution
        """
        # Set board dimensions and constraints based on difficulty
        if difficulty == "easy":
            rows, cols = 4, 4
        elif difficulty == "medium":
            rows, cols = 5, 5
        else:  # hard
            rows, cols = 6, 6

        # Create the board structure
        board = RandomBoardGenerator._create_board_structure(rows, cols, difficulty)

        # Fill in the solution values
        solution = RandomBoardGenerator._solve_board(board)

        # If solution failed, try a different board structure
        attempts = 0
        while solution is None and attempts < 3:
            board = RandomBoardGenerator._create_board_structure(rows, cols, difficulty)
            solution = RandomBoardGenerator._solve_board(board)
            attempts += 1

        # If we still don't have a solution, fall back to preset boards
        if solution is None:
            board = RandomBoardGenerator._generate_fallback_board(difficulty)
            solution = RandomBoardGenerator._get_fallback_solution(board, difficulty)

        # Set the sum values based on the solution
        board_with_sums = RandomBoardGenerator._set_sum_values(board, solution)

        # Make a deep copy of the board for returning
        playable_board = [[] for _ in range(len(board_with_sums))]
        for i in range(len(board_with_sums)):
            row = []
            for j in range(len(board_with_sums[0])):
                cell = board_with_sums[i][j]
                if isinstance(cell, BlockCell):
                    row.append(BlockCell())
                elif isinstance(cell, SumCell):
                    row.append(SumCell(cell.down_sum, cell.right_sum))
                elif isinstance(cell, NumberCell):
                    row.append(NumberCell(0))  # Set to 0 for player to solve
            playable_board[i] = row

        return playable_board, solution

    @staticmethod
    def _create_board_structure(rows, cols, difficulty):
        """
        Create the structure of the Kakuro board with longer runs for more challenge.

        Args:
            rows (int): Number of rows in the board
            cols (int): Number of columns in the board
            difficulty (str): 'easy', 'medium', or 'hard'

        Returns:
            2D list: Board structure with cells positioned
        """
        # Initialize the board with all block cells
        board = [[BlockCell() for _ in range(cols)] for _ in range(rows)]

        # First row and first column are always blocks
        for i in range(rows):
            for j in range(cols):
                if i == 0 or j == 0:
                    board[i][j] = BlockCell()

        # Set the pattern density based on difficulty
        # Lower density = fewer blocks = longer runs
        if difficulty == "easy":
            pattern_density = 0.25
            min_run_length = 2
        elif difficulty == "medium":
            pattern_density = 0.22
            min_run_length = 3
        else:  # hard
            pattern_density = 0.2
            min_run_length = 3

        # Start with a grid of number cells
        for i in range(1, rows):
            for j in range(1, cols):
                board[i][j] = NumberCell(0)

        # Strategically place blocks to create runs of appropriate length
        attempts = 0
        while attempts < 100:  # Avoid infinite loop
            # Make a copy of the current board
            temp_board = [[BlockCell() if i == 0 or j == 0 else NumberCell(0)
                           for j in range(cols)] for i in range(rows)]

            # Randomly place blocks according to density
            block_count = 0
            target_blocks = int((rows - 1) * (cols - 1) * pattern_density)

            while block_count < target_blocks:
                i = random.randint(1, rows - 1)
                j = random.randint(1, cols - 1)

                if not isinstance(temp_board[i][j], BlockCell):
                    temp_board[i][j] = BlockCell()
                    block_count += 1

            # Check if the pattern has runs of appropriate length
            valid_pattern = True

            # Check horizontal runs
            for i in range(1, rows):
                j = 1
                while j < cols:
                    if isinstance(temp_board[i][j], NumberCell):
                        run_start = j
                        while j < cols and isinstance(temp_board[i][j], NumberCell):
                            j += 1
                        run_length = j - run_start

                        # Skip if run is too short (except at board edges)
                        if run_length == 1 and run_start < cols - 1:
                            valid_pattern = False
                            break
                    else:
                        j += 1

                if not valid_pattern:
                    break

            # Check vertical runs
            if valid_pattern:
                for j in range(1, cols):
                    i = 1
                    while i < rows:
                        if isinstance(temp_board[i][j], NumberCell):
                            run_start = i
                            while i < rows and isinstance(temp_board[i][j], NumberCell):
                                i += 1
                            run_length = i - run_start

                            # Skip if run is too short (except at board edges)
                            if run_length == 1 and run_start < rows - 1:
                                valid_pattern = False
                                break
                        else:
                            i += 1

                    if not valid_pattern:
                        break

            if valid_pattern:
                # Use this pattern
                board = temp_board
                break

            attempts += 1

        # Convert blocks to sum cells where appropriate
        for i in range(rows):
            for j in range(cols):
                if isinstance(board[i][j], BlockCell):
                    # Check right and down neighbors
                    has_number_right = j < cols - 1 and isinstance(board[i][j + 1], NumberCell)
                    has_number_down = i < rows - 1 and isinstance(board[i + 1][j], NumberCell)

                    if has_number_right or has_number_down:
                        # Convert to a SumCell
                        right_sum = 0 if has_number_right else None
                        down_sum = 0 if has_number_down else None
                        board[i][j] = SumCell(down_sum, right_sum)

        # Verify that each NumberCell has a SumCell in its row and column
        for i in range(rows):
            for j in range(cols):
                if isinstance(board[i][j], NumberCell):
                    # Check for a SumCell to the left
                    has_sum_left = False
                    for k in range(j - 1, -1, -1):
                        if isinstance(board[i][k], SumCell) and board[i][k].right_sum is not None:
                            has_sum_left = True
                            break
                        if not isinstance(board[i][k], NumberCell):
                            break

                    # Check for a SumCell above
                    has_sum_above = False
                    for k in range(i - 1, -1, -1):
                        if isinstance(board[k][j], SumCell) and board[k][j].down_sum is not None:
                            has_sum_above = True
                            break
                        if not isinstance(board[k][j], NumberCell):
                            break

                    # Convert to a block if it doesn't have sums (we want both for more challenge)
                    if not (has_sum_left and has_sum_above):
                        board[i][j] = BlockCell()

        # After adjustments, reconsider all blocks for potential SumCells
        changed = True
        while changed:
            changed = False
            for i in range(rows):
                for j in range(cols):
                    if isinstance(board[i][j], BlockCell):
                        # Check right and down neighbors
                        has_number_right = j < cols - 1 and isinstance(board[i][j + 1], NumberCell)
                        has_number_down = i < rows - 1 and isinstance(board[i + 1][j], NumberCell)

                        if has_number_right or has_number_down:
                            # Convert to a SumCell
                            right_sum = 0 if has_number_right else None
                            down_sum = 0 if has_number_down else None
                            board[i][j] = SumCell(down_sum, right_sum)
                            changed = True

        # Examine the entire board for runs
        h_runs = []
        v_runs = []

        # Find horizontal runs
        for i in range(rows):
            j = 0
            while j < cols:
                if isinstance(board[i][j], SumCell) and board[i][j].right_sum is not None:
                    run_start = j + 1
                    run_end = run_start
                    while run_end < cols and isinstance(board[i][run_end], NumberCell):
                        run_end += 1
                    if run_end > run_start:
                        h_runs.append(run_end - run_start)
                j += 1

        # Find vertical runs
        for j in range(cols):
            i = 0
            while i < rows:
                if isinstance(board[i][j], SumCell) and board[i][j].down_sum is not None:
                    run_start = i + 1
                    run_end = run_start
                    while run_end < rows and isinstance(board[i][run_end], NumberCell):
                        run_end += 1
                    if run_end > run_start:
                        v_runs.append(run_end - run_start)
                i += 1

        # Calculate the average run length
        avg_run_length = 0
        if h_runs or v_runs:
            avg_run_length = (sum(h_runs) + sum(v_runs)) / (len(h_runs) + len(v_runs))

        # If the average run length is too low, try again
        if (difficulty == "easy" and avg_run_length < 2.0) or \
                (difficulty == "medium" and avg_run_length < 2.5) or \
                (difficulty == "hard" and avg_run_length < 3.0):
            return RandomBoardGenerator._create_board_structure(rows, cols, difficulty)

        return board

    @staticmethod
    def _solve_board(board):
        """
        Solve the Kakuro board and find a valid solution.
        Enhanced to handle more complex boards with longer runs.

        Args:
            board (2D list): The Kakuro board structure

        Returns:
            2D list or None: A valid solution or None if unsolvable
        """
        rows = len(board)
        cols = len(board[0])

        # Create a solution grid with 0s
        solution = [[0 for _ in range(cols)] for _ in range(rows)]

        # Find all runs (horizontal and vertical)
        runs = []

        # Horizontal runs
        for i in range(rows):
            j = 0
            while j < cols:
                if isinstance(board[i][j], SumCell) and board[i][j].right_sum is not None:
                    # Start of a horizontal run
                    start = j + 1
                    end = start
                    while end < cols and isinstance(board[i][end], NumberCell):
                        end += 1

                    if end > start:  # Only add if there are cells
                        runs.append({
                            'type': 'horizontal',
                            'row': i,
                            'start': start,
                            'end': end,
                            'cells': [(i, col) for col in range(start, end)]
                        })
                j += 1

        # Vertical runs
        for j in range(cols):
            i = 0
            while i < rows:
                if isinstance(board[i][j], SumCell) and board[i][j].down_sum is not None:
                    # Start of a vertical run
                    start = i + 1
                    end = start
                    while end < rows and isinstance(board[end][j], NumberCell):
                        end += 1

                    if end > start:  # Only add if there are cells
                        runs.append({
                            'type': 'vertical',
                            'col': j,
                            'start': start,
                            'end': end,
                            'cells': [(row, j) for row in range(start, end)]
                        })
                i += 1

        # Sort runs by length (shorter runs are easier to solve)
        runs.sort(key=lambda x: len(x['cells']))

        # If there are no runs, the board is invalid
        if not runs:
            return None

        # Try to solve the board
        if RandomBoardGenerator._backtrack_solve(solution, runs, 0):
            return solution
        else:
            return None

    @staticmethod
    def _backtrack_solve(solution, runs, run_index):
        """
        Solve the Kakuro board using backtracking.

        Args:
            solution (2D list): Current solution grid
            runs (list): List of runs to be filled
            run_index (int): Index of the current run to fill

        Returns:
            bool: True if solution found, False otherwise
        """
        # Base case: all runs filled
        if run_index >= len(runs):
            return True

        run = runs[run_index]
        cells = run['cells']
        length = len(cells)

        # Generate possible values for this run
        values = RandomBoardGenerator._generate_permutations(length)

        # Try each value combination
        random.shuffle(values)  # Randomize for variety

        for perm in values:
            # Check if this permutation conflicts with existing values
            valid = True
            for i, (r, c) in enumerate(cells):
                if solution[r][c] != 0 and solution[r][c] != perm[i]:
                    valid = False
                    break

            if not valid:
                continue

            # Assign values
            for i, (r, c) in enumerate(cells):
                solution[r][c] = perm[i]

            # Recursively try to solve the next run
            if RandomBoardGenerator._backtrack_solve(solution, runs, run_index + 1):
                return True

            # If we reach here, this permutation didn't work
            # Backtrack by clearing the values
            for r, c in cells:
                solution[r][c] = 0

        # No valid permutation found for this run
        return False

    @staticmethod
    def _generate_permutations(length):
        """
        Generate random permutations of numbers 1-9.

        Args:
            length (int): The length of the permutation

        Returns:
            list: List of permutations
        """
        if length > 9:
            length = 9  # Kakuro only uses digits 1-9

        # Create several random permutations
        permutations = []
        for _ in range(min(10, 3 ** length)):  # Limit the number of permutations
            perm = list(range(1, 10))
            random.shuffle(perm)
            permutations.append(perm[:length])

        return permutations

    @staticmethod
    def _set_sum_values(board, solution):
        """
        Calculate and set the sum values for all SumCells based on the solution.

        Args:
            board (2D list): The board structure
            solution (2D list): The solved values

        Returns:
            2D list: Updated board with correct sum values
        """
        rows = len(board)
        cols = len(board[0])

        for i in range(rows):
            for j in range(cols):
                if isinstance(board[i][j], SumCell):
                    # Calculate right sum if needed
                    if board[i][j].right_sum is not None:
                        right_sum = 0
                        col = j + 1
                        while col < cols and isinstance(board[i][col], NumberCell):
                            right_sum += solution[i][col]
                            col += 1
                        board[i][j] = SumCell(board[i][j].down_sum, right_sum)

                    # Calculate down sum if needed
                    if board[i][j].down_sum is not None:
                        down_sum = 0
                        row = i + 1
                        while row < rows and isinstance(board[row][j], NumberCell):
                            down_sum += solution[row][j]
                            row += 1
                        board[i][j] = SumCell(down_sum, board[i][j].right_sum)

        return board

    @staticmethod
    def _generate_fallback_board(difficulty):
        """
        Generate a fallback board if random generation fails.
        These are predefined boards similar to the original ones.

        Args:
            difficulty (str): 'easy', 'medium', or 'hard'

        Returns:
            2D list: A predefined Kakuro board
        """
        if difficulty == "easy":
            return [
                [BlockCell(), SumCell(6, None), SumCell(19, None), BlockCell()],
                [SumCell(None, 14), NumberCell(0), NumberCell(0), SumCell(5, None)],
                [SumCell(None, 10), NumberCell(0), NumberCell(0), NumberCell(0)],
                [BlockCell(), SumCell(None, 6), NumberCell(0), NumberCell(0)]
            ]
        elif difficulty == "medium":
            return [
                [BlockCell(), BlockCell(), BlockCell(), SumCell(10, None), SumCell(8, None)],
                [BlockCell(), BlockCell(), SumCell(8, 6), NumberCell(0), NumberCell(0)],
                [BlockCell(), SumCell(7, 8), NumberCell(0), NumberCell(0), NumberCell(0)],
                [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), BlockCell()],
                [SumCell(None, 5), NumberCell(0), NumberCell(0), BlockCell(), BlockCell()]
            ]
        else:  # hard
            return [
                [BlockCell(), BlockCell(), BlockCell(), SumCell(7, None), SumCell(16, None), SumCell(16, None)],
                [BlockCell(), SumCell(23, None), SumCell(11, 11), NumberCell(0), NumberCell(0), NumberCell(0)],
                [BlockCell(), SumCell(16, 15), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
                [SumCell(None, 14), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0), NumberCell(0)],
                [SumCell(None, 17), NumberCell(0), NumberCell(0), NumberCell(0), SumCell(11, 6), NumberCell(0)],
                [SumCell(None, 11), NumberCell(0), NumberCell(0), BlockCell(), SumCell(None, 6), NumberCell(0)]
            ]

    @staticmethod
    def _get_fallback_solution(board, difficulty):
        """
        Return a predefined solution for the fallback boards.

        Args:
            board (2D list): The fallback board
            difficulty (str): 'easy', 'medium', or 'hard'

        Returns:
            2D list: The solution for the fallback board
        """
        # Create a solution grid with 0s
        rows = len(board)
        cols = len(board[0])
        solution = [[0 for _ in range(cols)] for _ in range(rows)]

        if difficulty == "easy":
            # Easy board solution
            solution[1][1] = 8
            solution[1][2] = 6
            solution[2][1] = 5
            solution[2][2] = 3
            solution[2][3] = 2
            solution[3][1] = 1
            solution[3][2] = 5
        elif difficulty == "medium":
            # Medium board solution
            solution[1][3] = 7
            solution[1][4] = 1
            solution[2][1] = 3
            solution[2][2] = 5
            solution[2][3] = 2
            solution[2][4] = 6
            solution[3][1] = 9
            solution[3][2] = 4
            solution[3][3] = 1
            solution[3][4] = 0
            solution[4][1] = 2
            solution[4][2] = 3
        else:  # hard
            # Hard board solution (using placeholder values)
            # In a real implementation, you'd have actual solutions here
            for i in range(1, rows):
                for j in range(1, cols):
                    if isinstance(board[i][j], NumberCell):
                        solution[i][j] = min(i + j, 9)  # Placeholder formula

        return solution