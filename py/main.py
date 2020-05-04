import sys

import Sudoku

def main():
    sudoku = Sudoku.Sudoku()

    sudoku.read_file(sys.argv[1])
    print(sudoku)
    sudoku.solve()
    print(sudoku)


if __name__ == '__main__':
    main()
