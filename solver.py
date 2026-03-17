import numpy as np
import math


BOX_LINES = ["─", "│", "┌", "┐", "└", "┘", "├", "┤", "┬", "┴", "┼"]
CHARS = "0123456789ABCDEFG"


class Cell:
    """Represents a cell in a sudoku puzzle and all possible valid numbers.

    If a cell is initialized with 0, the cell is created as full.

    1-indexed.
    """

    def __init__(self, index: int = 0, size: int = 9):
        self.size = size

        if index < 1:
            self.bits = (1 << size) - 1
        else:
            self.bits = 1 << (index - 1)

    def empty(size: int = 9):
        return Cell(0, size)

    def full(size: int = 9):
        cell = Cell.empty(size)
        cell.bits = (1 << size) - 1  # just manually set the bits tbh

        return cell

    def __str__(self):
        return str(self.get_value())

    def __repr__(self):
        return str("".join(["1" if self[i] else "0" for i in range(1, self.size + 1)]))

    def __or__(self, other):
        return Cell(self.bits | other.bits)

    def __and__(self, other):
        return Cell(self.bits & other.bits)

    def __xor__(self, other):
        return Cell(self.bits ^ other.bits)

    def __invert__(self):
        return Cell(~self.bits)

    def __eq__(self, other):
        return self.bits == other.bits

    def __ne__(self, other):
        return self.bits != other.bits

    def __getitem__(self, index) -> bool:
        return self.bits & (1 << (index - 1)) != 0

    def __setitem__(self, index: int, value: bool):
        if value:
            self.bits |= 1 << (index - 1)
        else:
            self.bits &= ~(1 << (index - 1))

    def set_flag(self, value: int):
        self[value] = True

    def unset_flag(self, value: int):
        self[value] = False

    def test(self, value: int):
        return self.bits[value]

    def decompose(self):
        return [self[i] for i in range(1, self.size + 1)]

    def get_value(self) -> int:
        """Returns the value if only one bit is set, otherwise 0."""
        if self.bits > 0 and (self.bits & (self.bits - 1)) == 0:
            return int(math.log2(self.bits)) + 1
        return 0

    def get_possibility_count(self) -> int:
        """Returns the number of possible values for this cell."""
        mask = (1 << self.size) - 1
        return bin(self.bits & mask).count("1")


class Sudoku:
    def validate_shape(shape: (int, int)) -> int:
        """Ensures that the puzzle is a valid NxN grid.

        Returns the side length of the puzzle if valid, and raises an exception if not.

        ---

        From Wikipedia:
            The classic 9x9 Sudoku format can be generalized to an NxN row-column grid
            partitioned into N regions, where each of the N rows, columns and regions
            have N cells and each of the N digits occur once in each row, column or region.
        """

        if shape[0] != shape[1]:
            raise Exception("Puzzle must be square.")
        if shape[0] < 0:
            raise Exception("Puzzle cannot be negative size.")
        if math.sqrt(shape[0]) % 1 != 0:
            raise Exception("Puzzle cannot be split into squares.")

        return shape[0]

    def __init__(self, puzzle: np.ndarray):
        N = Sudoku.validate_shape(puzzle.shape)

        self.size = N
        self.puzzle = puzzle

    def new_from_string(puzzle: str) -> Sudoku:
        """Parse the puzzle string into an NxN numpy array, where N = M^2.

        Throws an exception if the puzzle does not meet this condition.
        """

        if len(puzzle) == 0:
            return Sudoku([])

        N = int(math.sqrt(len(puzzle)))
        if N * N != len(puzzle):
            raise Exception("Puzzle must be square.")

        cells = [Cell(int(c)) for c in puzzle]
        puzzle = np.array(cells).reshape((N, N))

        return Sudoku(puzzle)

    def solve(self) -> str:
        """
        Attempts to solve the sudoku puzzle.
        """

        # print(self)
        # print(self.puzzle)

        # trivial cases
        if self.size == 0:
            return ""
        if self.size == 1:
            return "1"

        solved_cells = set()

        def next_solved() -> (int, int):
            for r in range(self.size):
                for c in range(self.size):
                    if self.puzzle[r, c].get_value() != 0:
                        if (r, c) not in solved_cells:
                            solved_cells.add((r, c))
                            return (r, c)
            return (-1, -1)

        # naive: use solved cells to remove possible values
        while True:
            # find a cell with a single possible value
            (r, c) = next_solved()
            if r == -1 or c == -1:
                break

            # get value of cell
            val = self.puzzle[r, c].get_value()
            if val == 0:
                raise Exception("Solved cell has no value.")

            # remove value from all other cells in row
            for c2 in range(self.size):
                if c2 != c:
                    self.puzzle[r, c2].unset_flag(val)

            # remove value from all other cells in column
            for r2 in range(self.size):
                if r2 != r:
                    self.puzzle[r2, c].unset_flag(val)

            # remove value from all other cells in block
            block_size = int(math.sqrt(self.size))
            block_row = r // block_size
            block_col = c // block_size
            for r2 in range(block_row * block_size, (block_row + 1) * block_size):
                for c2 in range(block_col * block_size, (block_col + 1) * block_size):
                    if r2 != r or c2 != c:
                        self.puzzle[r2, c2].unset_flag(val)

        # print(self)
        # print(self.puzzle)

        # TODO: lookahead/backtracking/whatever it's supposed to be

        return self.to_string()

    def __str__(self):
        if self.size == 0:
            return ""

        block_size = int(math.sqrt(self.size))

        def format_sep(left, mid, right):
            block_segment = BOX_LINES[0] * (2 * block_size + 1)
            segments = [block_segment] * (self.size // block_size)
            return left + mid.join(segments) + right + "\n"

        def format_row(r):
            res = BOX_LINES[1] + " "
            for c in range(self.size):
                cell = self.puzzle[r, c]
                val = cell.get_value()
                if val != 0:
                    display = CHARS[val]
                else:
                    count = cell.get_possibility_count()
                    display = "·" if count == self.size else "?"
                res += display + " "
                if (c + 1) % block_size == 0:
                    res += BOX_LINES[1] + " "
            return res.rstrip() + "\n"

        output = format_sep(BOX_LINES[2], BOX_LINES[8], BOX_LINES[3])
        for r in range(self.size):
            output += format_row(r)
            if (r + 1) % block_size == 0 and (r + 1) != self.size:
                output += format_sep(BOX_LINES[6], BOX_LINES[10], BOX_LINES[7])

        output += format_sep(BOX_LINES[4], BOX_LINES[9], BOX_LINES[5])
        return output

    def __repr__(self):
        return str(self)

    def to_string(self) -> str:
        return "".join([str(c) for c in self.puzzle.flat])


if __name__ == "__main__":
    # for testing purposes only!
    puzzle_str = (
        "030104506201000009407600080700000342306020908000308700000589200180430605590006007"
    )
    solution_str = (
        "839174526261853479457692183718965342346721958925348761673589214182437695594216837"
    )

    puzzle = Sudoku.new_from_string(puzzle_str)
    puzzle.solve()
    assert puzzle.to_string() == solution_str
