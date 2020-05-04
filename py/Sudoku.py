import math
from itertools import permutations
from pprint import pprint

class PuzzleError(Exception):
    def __init__(self, puzzle, message):
        self.puzzle = puzzle
        self.message = message

class Sudoku:
    __puzzle = []
    __rcb = []

    def __init__(self):
        pass

    def read_file(self, filename):
        f = open(filename, 'r')

        for line in f.readlines():
            self.__puzzle.append(list(map(lambda x: None if x == '0' else int(x),
                                          line.strip().split(','))))

        f.close()

        self.__verify_puzzle()
        self.__calc_rcb()

    def __box_number(self, row, col, puzzle_len):
        sqrt_len = int(math.sqrt(puzzle_len))

        col_box = (math.ceil((col + 1) / sqrt_len) - 1)
        row_box = (math.ceil((row + 1) / sqrt_len) - 1)

        return col_box + row_box * sqrt_len

    # row/column/box indices
    def __calc_rcb(self):
        rcb = []

        for row in range(len(self.__puzzle)):
            rcb.append([])
            for col in range(len(self.__puzzle)):
                rcb[row].append((row, col, self.__box_number(row, col, len(self.__puzzle))))

        self.__rcb = rcb

    def __verify_dimensions(self):
        for line in self.__puzzle:
            if len(line) != len(self.__puzzle):
                raise PuzzleError(self.__puzzle,
                                  'Puzzle has incorrect dimensions')

    def __is_square(self, n):
        n = abs(n)
        x = n // 2
        seen = set([x])
        while x * x != n:
            x = (x + (n // x)) // 2
            if x in seen:
                return False
            seen.add(x)

        return True

    def __verify_numbers(self):
        # row duplicates
        for row, line in enumerate(self.__puzzle):
            dup_check = set()
            for element in line:
                if element in dup_check:
                    raise PuzzleError(self.__puzzle,
                                      'Puzzle has duplicate numbers in row {}'
                                      .format(row))

                if element is not None:
                    if element > len(self.__puzzle) or element < 1:
                        raise PuzzleError(self.__puzzle,
                                          '{} is not a valid value'
                                          .format(element))

                    dup_check.add(element)

        for column in range(len(self.__puzzle)):
            dup_check = set()
            for row in self.__puzzle:
                if row[column] in dup_check:
                    raise PuzzleError(self.__puzzle,
                                      'Puzzle has duplicate numbers in column {}'
                                      .format(column))

                if row[column] is not None:
                    dup_check.add(row[column])

        # puzzle len must be a perfect square
        if not self.__is_square(len(self.__puzzle)):
            raise PuzzleError(self.__puzzle, 'Puzzle length isn\'t a perfect square')

        boxlen = int(math.sqrt(len(self.__puzzle)))

        offsets = set(permutations(list(range(boxlen)) * boxlen, 2))

        for offset in offsets:
            dup_check = set()
            for i in range(boxlen):
                for k in range(boxlen):
                    element = self.__puzzle[offset[0] * boxlen + i][offset[1] * boxlen + k]

                    if element in dup_check:
                        raise PuzzleError(self.__puzzle,
                                          'Puzzle has duplicate numbers in box {}'
                                          .format(offset))

                    if element is not None:
                        dup_check.add(element)

    # ensures puzzle is formatted properly
    def __verify_puzzle(self):
        # check dimensions
        self.__verify_dimensions()

        # check no double numbers in row/column/box
        self.__verify_numbers()

    def is_solved(self):
        self.__verify_puzzle()

        for row in self.__puzzle:
            for element in row:
                if element is None:
                    return False

        return True

    def __avl(self, coords, puzzle):
        if puzzle[coords[0]][coords[1]] is not None:
            return []

        avl = list(range(1, len(self.__puzzle) + 1))

        this_rcb = self.__rcb[coords[0]][coords[1]]

        flat_rcb = [item for sublist in self.__rcb for item in sublist]
        contention = list(filter(lambda x: x[0] == this_rcb[0]
                                 or x[1] == this_rcb[1]
                                 or x[2] == this_rcb[2],
                                 flat_rcb))

        for cell in contention:
            cell_element = puzzle[cell[0]][cell[1]]
            if cell_element in avl:
                avl.remove(cell_element)

        return avl

    def __at(self, coords, avl, puzzle):
        ret = []
        for element in avl:
            new = [row[:] for row in puzzle]
            new[coords[0]][coords[1]] = element
            ret.append(new)

        return ret

    def solve(self):
        vec = [[row[:] for row in self.__puzzle]]
        empty = [(i, k)
                 for i in range(len(self.__puzzle))
                 for k in range(len(self.__puzzle))
                 if self.__puzzle[i][k] is None]

        for coords in empty:
            newvec = []
            for puzzle in vec:
                avl = self.__avl(coords, puzzle)
                if avl != []:
                    newvec.extend(self.__at(coords, avl, puzzle))

            vec = newvec

        if len(vec) != 1:
            raise PuzzleError(self.__puzzle,
                              'Multiple solutions found: {}'.format(vec))

        self.__puzzle = vec[0]

    def __puzzle_to_string(self, puzzle):
        output = ''
        cell_width = (len(puzzle) // 10) + 1

        for row in puzzle:
            for element in row:
                output += '{} '.format(element if element is not None else ' ').ljust(cell_width)
            output = output[:-1] + '\n'

        return output

    def __str__(self):
        return self.__puzzle_to_string(self.__puzzle)
