import XO_vs_comp as c


def test_comp_marks_center_first_move():
    game = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    game2 = [[0,0,0],[0,0,0],[0,0,0]]
    game3 = [[0,0,0],[0,0,0],[0,0,0]]

    # comp makes first move
    c.comp(game, game2, game3)

    assert game[1][1] == "O"
    assert game2[1][1] == -1


def test_comp_blocks_win():
    # Player about to win horizontally
    game = [
        ["X", "X", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    game2 = [
        [1, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    game3 = [
        [1, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    c.comp(game, game2, game3)


    assert game[0][2] == "O"
