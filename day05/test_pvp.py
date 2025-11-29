import XO


def test_letters_mapping():
    letters = XO.letters()
    assert letters["a"] == 0
    assert letters["b"] == 1
    assert letters["c"] == 2
    assert letters["0"] == 0
    assert letters["2"] == 2


def test_begin_returns_valid_name():
    names = ("Alice", "Bob")
    starter = XO.begin(names)
    assert starter in names


def test_victory_row():
    game = [
        ["X", "X", "X"],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    assert XO.victory(game, ("X", "O"), "Alice") == 1


def test_victory_col():
    game = [
        ["O", " ", " "],
        ["O", " ", " "],
        ["O", " ", " "]
    ]
    assert XO.victory(game, ("O", "X"), "Bob") == 1


def test_victory_diag():
    game = [
        ["X", " ", " "],
        [" ", "X", " "],
        [" ", " ", "X"]
    ]
    assert XO.victory(game, ("X", "O"), "Alice") == 1
