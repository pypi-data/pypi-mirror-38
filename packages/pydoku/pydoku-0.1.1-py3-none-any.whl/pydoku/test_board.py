from pydoku import board


def test_row():
    subject = board.Board(2, 2)
    subject[0] = [1, 2, 0, 0]
    assert [1, 2, 0, 0] == subject.row(0)
    assert [0, 0, 0, 0] == subject.row(1)


def test_column():
        subject = board.Board(2, 2)
        subject[0][0] = 1
        subject[1][0] = 2
        subject[2][0] = 3
        subject[3][0] = 4
        assert [1, 2, 3, 4] == subject.column(0)
        assert [0, 0, 0, 0] == subject.column(1)
        assert [0, 0, 0, 0] == subject.column(2)


def test_square():
    subject = board.Board(3, 2)
    subject[0] = [1, 2, 3, 4, 5, 6]
    subject[1] = [4, 5, 6, 1, 2, 3]
    subject[2] = [2, 3, 4, 5, 6, 1]
    subject[3] = [5, 6, 1, 2, 3, 4]
    subject[4] = [3, 4, 5, 6, 1, 2]
    subject[5] = [6, 1, 2, 3, 4, 5]

    assert [1, 2, 3, 4, 5, 6] == subject.square(0)
    assert [4, 5, 6, 1, 2, 3] == subject.square(1)
    assert [2, 3, 4, 5, 6, 1] == subject.square(2)
    assert [5, 6, 1, 2, 3, 4] == subject.square(3)
    assert [3, 4, 5, 6, 1, 2] == subject.square(4)
    assert [6, 1, 2, 3, 4, 5] == subject.square(5)


def test_valid():
    dups = board.Board(2, 2)
    dups[0][0] = 1
    dups[0][1] = 1
    assert not dups.valid()

    dups = board.Board(2, 2)
    dups[0][0] = 1
    dups[1][0] = 1
    assert not dups.valid()

    dups = board.Board(2, 2)
    dups[2][2] = 1
    dups[3][3] = 1
    assert not dups.valid()

    ok = board.Board(2, 2)
    assert ok.valid()

    ok[2][1] = 1
    ok[2][2] = 2
    assert ok.valid()


def test_complete():
    subject = board.Board(3, 2)
    subject[0] = [1, 2, 3, 4, 5, 6]
    subject[1] = [4, 5, 6, 1, 2, 3]
    subject[2] = [2, 3, 4, 5, 6, 1]
    subject[3] = [5, 6, 1, 2, 3, 4]
    subject[4] = [3, 4, 5, 6, 1, 2]
    subject[5] = [6, 1, 2, 3, 4, 5]

    assert subject.complete()

    subject[5][5] = 0
    assert not subject.complete()

    subject[5][5] = 4
    assert not subject.complete()


def test_solve():
    subject_small = board.Board(2, 2)
    subject_small[0] = [1, 2, 3, 4]
    subject_small[1] = [3, 4, 1, 2]
    subject_small[2] = [2, 3, 4, 1]

    solved = subject_small.solve()
    assert solved is not None
    assert [1, 2, 3, 4] == solved[0]
    assert [3, 4, 1, 2] == solved[1]
    assert [2, 3, 4, 1] == solved[2]
    assert [4, 1, 2, 3] == solved[3]

    empty = board.Board()
    solved = empty.solve()
    assert solved is not None
    assert solved.complete()


def test___repr__():
    subject = board.Board()
    got = repr(subject)
    want = """3x3
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
0 0 0 0 0 0 0 0 0 
"""
    assert got == want
