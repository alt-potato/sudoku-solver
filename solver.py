import numpy as np
import math


class Cell:
    """Represents a cell in a sudoku puzzle and all possible valid numbers.

    If a cell is initialized with 0, the cell is created as full.

    1-indexed.
    """

    def __init__(self, index: int = 0):
        if index < 1:
            self.bits = 0b111111111
        else:
            self.bits = 1 << (index - 1)

    def empty():
        return Cell(0)

    def full():
        return Cell(0b111111111)

    def __str__(self):
        return str("".join(["1" if self[i] else "0" for i in range(1, 10)]))

    def __repr__(self):
        return str("".join(["1" if self[i] else "0" for i in range(1, 10)]))

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
        return [self[i] for i in range(1, 10)]


def puzzle_from_string(puzzle: str) -> np.ndarray:
    """Parse the puzzle string into an NxN numpy array, where (N | 3).

    Throws an exception if the puzzle does not meet this condition.
    """

    N = math.sqrt(len(puzzle))
    if N % 1 != 0:
        raise Exception("Puzzle must be a square.")
    if N % 3 != 0:
        raise Exception("Puzzle size must be a multiple of 3.")
    N = int(N)
    if N == 0:
        return np.array([])

    cells = [Cell(int(c)) for c in puzzle]
    puzzle = np.array(cells).reshape((N, N))

    return puzzle


def solve(puzzle: str) -> str:
    """
    Attempts to solve the puzzle.
    """

    puzzle = puzzle_from_string(puzzle)
    if puzzle.size == 0:
        return ""

    print(puzzle)

    return


# test puzzle
puzzle_str = (
    "030104506201000009407600080700000342306020908000308700000589200180430605590006007"
)

solve(puzzle_str)
