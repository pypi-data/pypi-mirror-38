class Board:
    """represents a Sudoku board of nxn dimensions."""

    def __init__(self, width=3, height=3):
        """creates a new empty sudoku board"""

        self._width = width
        self._height = height

        self._contents = []
        # Create an empty board by populating each cell with a zero.
        for i in range(self.total_dimension):
            self._contents.append([])
            for j in range(self.total_dimension):
                self._contents[i].append(0)

    def __getitem__(self, item):
        return self._contents[item]

    def __setitem__(self, key, value):
        self._contents[key] = value

    def copy(self):
        """creates an identical instance of this """
        retval = self.__class__(self._width, self._height)
        for i in range(retval.total_dimension):
            for j in range(retval.total_dimension):
                retval[i][j] = self[i][j]
        return retval

    @property
    def total_dimension(self):
        """returns the size of the whole board instead of a single square."""
        return self._width * self._height

    def __repr__(self):
        retval = str(self._width) + 'x' + str(self._height) + '\n'

        for i in range(self.total_dimension):
            for j in range(self.total_dimension):
                retval += str(self[i][j]) + ' '
            retval += '\n'
        return retval

    def __str__(self):
        retval = ""
        character_width = 2 * self._height * (self._width + 1) + 1
        for i in range(self.total_dimension):
            if i % self._height == 0:
                for k in range(character_width):
                    retval += '-'
                retval += '\n'
            for j in range(self.total_dimension):
                if j % self._width == 0:
                    retval += '| '
                retval += str(self[i][j]) + ' '
            retval += '|\n'

        for k in range(character_width):
            retval += '-'
        retval += '\n'

        return retval

    def row(self, n):
        """returns all values in a given row as seen below on a 9x9 board:
        -------------------------
        | 0 0 0 | 0 0 0 | 0 0 0 |
        | 1 1 1 | 1 1 1 | 1 1 1 |
        | 2 2 2 | 2 2 2 | 2 2 2 |
        -------------------------
        | 3 3 3 | 3 3 3 | 3 3 3 |
        | 4 4 4 | 4 4 4 | 4 4 4 |
        | 5 5 5 | 5 5 5 | 5 5 5 |
        -------------------------
        | 6 6 6 | 6 6 6 | 6 6 6 |
        | 7 7 7 | 7 7 7 | 7 7 7 |
        | 8 8 8 | 8 8 8 | 8 8 8 |
        -------------------------
        """
        return self[n].copy()

    def column(self, n):
        """returns all values in a given column as seen below on a 9x9 board:
        -------------------------
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        -------------------------
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        -------------------------
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        | 0 1 2 | 3 4 5 | 6 7 8 |
        -------------------------
        """
        return [self[i][n] for i in range(self.total_dimension)]

    def square(self, n):
        """returns all values in a given square indexed in row major fashion as seen below on a 9x9 board:
        -------------------------
        | 0 0 0 | 1 1 1 | 2 2 2 |
        | 0 0 0 | 1 1 1 | 2 2 2 |
        | 0 0 0 | 1 1 1 | 2 2 2 |
        -------------------------
        | 3 3 3 | 4 4 4 | 5 5 5 |
        | 3 3 3 | 4 4 4 | 5 5 5 |
        | 3 3 3 | 4 4 4 | 5 5 5 |
        -------------------------
        | 6 6 6 | 7 7 7 | 8 8 8 |
        | 6 6 6 | 7 7 7 | 8 8 8 |
        | 6 6 6 | 7 7 7 | 8 8 8 |
        -------------------------

        or on a 6x6 board (square size 3x2):
        -----------------
        | 0 0 0 | 1 1 1 |
        | 0 0 0 | 1 1 1 |
        -----------------
        | 2 2 2 | 3 3 3 |
        | 2 2 2 | 3 3 3 |
        -----------------
        | 4 4 4 | 5 5 5 |
        | 4 4 4 | 5 5 5 |
        -----------------
        """
        return [
            self[n // self._height * self._height + row][n % self._height * self._width + col]
            for row in range(self._height)
            for col in range(self._width)]

    def _valid_slice(self, subject):
        """determines whether or not any given list has conflicting sudoku values."""
        trimmed = [x for x in subject if x != 0]

        # This feels very expressive to me, but could increase GC pressure. Is there a pythonic 'any' function?
        out_of_bounds = any(x > self.total_dimension for x in trimmed)

        return not out_of_bounds and len(trimmed) == len(set(trimmed))

    def valid(self):
        """determines whether or not a Sudoku board has any conflicting values."""
        return all([
            self._valid_slice(self.row(n)) and
            self._valid_slice(self.column(n)) and
            self._valid_slice(self.square(n))
            for n in range(self.total_dimension)])

    def complete(self):
        """determines whether or not a Sudoku board is both `valid` and contains no empty cells."""
        return self.valid() and not any(
            self[row][col] == 0
            for row in range(self.total_dimension)
            for col in range(self.total_dimension)
        )

    def solve(self):
        """finds a board where by only adding values to this board, all spaces are filled and there are no conflicting
        squares.
        """
        if self.complete():
            return self

        if not self.valid():
            return None

        row, col = next(
            (i, j)
            for i in range(self.total_dimension)
            for j in range(self.total_dimension)
            if self[i][j] == 0)

        updated = self.copy()

        for i in range(self.total_dimension):
            updated[row][col] = i + 1
            candidate = updated.solve()
            if candidate is not None:
                return candidate

        return None

