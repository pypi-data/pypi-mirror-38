# Pydoku

[![Build Status](https://travis-ci.com/marstr/pydoku.svg?branch=master)](https://travis-ci.com/marstr/pydoku)
[![Python](https://img.shields.io/pypi/pyversions/pydoku.svg?maxAge=2592000)](https://pypi.python.org/pypi/pydoku)

Sudoku is a mathematical game, where one looks to completely fill a board with numbers, where no values are repeated in
any given row, column, square or square. You can read more about this game on 
[Wikipedia](https://en.wikipedia.org/wiki/Sudoku). The most common variant uses a 9x9 grid segmented into nine
3x3 squares, with 9 rows and 9 columns. However, the difficulty of the game can be adjusted by changing the size of the 
board. For instance, you can play an easier game in a 6x6 board where each square has 3 columns and 2 rows.

This package looks to expose the ability to solve sudoku puzzles with squares of any dimension (given a powerful enough 
machine!) 

## Install

> Minimum supported version of Python: 3.5

Easily install this package using pip!

``` bash
pip install pydoku
```

## Usage

Solving a default board with a couple of values inserted:

``` Python
import pydoku

subject = pydoku.Board()
subject[0][3] = 6
subject[0][1] = 1
print(subject.solve())

# Output:
# -------------------------
# | 2 1 3 | 6 4 5 | 7 8 9 |
# | 4 5 6 | 7 8 9 | 1 2 3 |
# | 7 8 9 | 1 2 3 | 4 5 6 |
# -------------------------
# | 1 2 4 | 3 5 6 | 8 9 7 |
# | 3 6 5 | 8 9 7 | 2 1 4 |
# | 8 9 7 | 2 1 4 | 3 6 5 |
# -------------------------
# | 5 3 1 | 4 6 2 | 9 7 8 |
# | 6 4 2 | 9 7 8 | 5 3 1 |
# | 9 7 8 | 5 3 1 | 6 4 2 |
# -------------------------
```

## Contributing

Contributions welcome, if not well monitored. Feel free to send PRs, file issues, etc.

## License

This library is available under the MIT license, the full text can be found [here](./LICENSE). Basically though, go use 
it however and for whatever you want, just understand that I'm not liable for issues you encounter.
 