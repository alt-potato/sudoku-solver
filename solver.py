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
            self.bits = ~0b0
        else:
            self.bits = 1 << (index - 1)

    def empty():
        return Cell(0)

    def full():
        return Cell(~0b0)

    def __str__(self):
        return str("".join(["1" if self[i] else "0" for i in range(1, self.size + 1)]))

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
        return bin(self.bits & mask).count('1')


class Sudoku:
    def validate_size(count: int) -> int:
        """Ensures that the puzzle is a square and a multiple of 3.

        Returns the side length of the puzzle if valid, and raises an exception if not.

        NOTE: THIS IMPLEMENTATION IS INCORRECT! TODO: FIX
        From wikipedia:
            The classic 9x9 Sudoku format can be generalized to an NxN row-column grid 
            partitioned into N regions, where each of the N rows, columns and regions 
            have N cells and each of the N digits occur once in each row, column or region.
        """

        N = math.sqrt(count)
        if N % 1 != 0:
            raise Exception("Puzzle must be square.")
        if N % 3 != 0:
            raise Exception("Puzzle size must be a multiple of 3.")
        N = int(N)

        return N

    def __init__(self, puzzle: np.ndarray):
        N = Sudoku.validate_size(puzzle.size)
        if puzzle.shape != (N, N):
            raise Exception("Puzzle must be square.")

        self.size = N
        self.puzzle = puzzle

    def new_from_string(puzzle: str) -> Sudoku:
        """Parse the puzzle string into an NxN numpy array, where (N | 3).

        Throws an exception if the puzzle does not meet this condition.
        """

        N = Sudoku.validate_size(len(puzzle))
        cells = [Cell(int(c)) for c in puzzle]
        puzzle = np.array(cells).reshape((N, N))

        return Sudoku(puzzle)

    def solve(self) -> str:
        """
        Attempts to solve the puzzle.
        """

        if self.size == 0:
            return ""

        print(puzzle)

        return

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


# test puzzle
puzzle_str = (
    "030104506201000009407600080700000342306020908000308700000589200180430605590006007"
)

puzzle = Sudoku.new_from_string(puzzle_str)
puzzle.solve()
