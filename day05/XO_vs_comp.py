# This is a Tic Tac Toe game program, player vs computer.
import random
import numpy as np          # you need to pip install numpy
import XO as xo_functions

game = [[' ', ' ', ' '],            # This "blank" matrix represent our started boardgame
        [' ', ' ', ' '],
        [' ', ' ', ' ']]

game2 = [[0, 0, 0],            # We will use this matrix to save values: -1 for 'O', and 1 for 'X'
         [0, 0, 0],
         [0, 0, 0]]

game3 = [[0, 0, 0],            # we will use this matrix to represent vacant as 0 and occupied as 1
         [0, 0, 0],
         [0, 0, 0]]
# Functions start from here
def name():
    "This function get the user name."""
    print("Please insert your your name")
    u_name = input("Player: ")
    return u_name


def play(names, beginner, game, game2, game3):
    "This function make the actual play each turn."""
    current_player = beginner
    letter = xo_functions.letters()
    for i in range(9):
        while True:
            xo_functions.game_board(game)
            if current_player == 'Computer':
                comp(game, game2, game3)
                if victory(current_player):
                    return '0'
                if current_player == names[0]:          # update the name for next player
                    current_player = names[1]
                else:
                    current_player = names[0]
                break
            move = input("\n%s please choose your move (letter and number): " % current_player)
            if move == '':
                continue
            if move[0] != 'a' and move[0] != 'b' and move[0] != 'c':
                print("invalid input")
                continue
            if len(move) != 2 or (move[1] != '0' and move[1] != '1' and move[1] != '2'):
                print("invalid input\n")
                continue
            else:
                a = letter[move[1]]
                b = letter[move[0]]
                if game[a][b] == 'X' or game[a][b] == 'O':
                    print("invalid move, already occupied")
                else:
                    game[a][b] = 'X'
                    game2[a][b] = 1
                    if victory(current_player):
                        return '2'
                    if current_player == names[0]:
                        current_player = names[1]
                    else:
                        current_player = names[0]
                    break
    xo_functions.game_board(game)
    print("Draw!")
    return '1'


def comp(game, game2, game3):
    "This function Play the computer side algorithm."""
    count, diag_r, diag_r_game3 = 0, 0, 0
    col = np.sum(game2, 0)
    middle = int(len(game)/2)
    for i in range(3):
        for j in range(3):
            if game2[i][j]:
                game3[i][j] = 1         # Represent vacant as 0 and occupied as 1
            if not game[i][j] == ' ':
                count += 1
        diag_r += game2[i][2 - i]        # calc the second diagonal line of game2
        diag_r_game3 += game3[i][2 - i]  # calc the second diagonal line of game3
    # Computer's algorithm starts from here:
    # Stage 1 - if at most one slot marked and the middle is empty, play it.
    if game[middle][middle] == ' ' and (count <= 1):
        game[middle][middle] = 'O'
        game2[middle][middle] = -1
        return
    # Stage 2 - if there is 2 O's in a row/column/diagonally play the third one to win.
    if calc(game, game2, diag_r, -2):
        return
    # Stage 3 - if there is 2 X's in a row/column/diagonally play the third one to prevent loss.
    if calc(game, game2, diag_r, 2):
        return
    # Extra stage - create a fork that leads to win
    if count == 2 and game[middle][middle] == 'O':
        if game[0][1] == 'X' or game[1][0] == 'X':
            game[0][0] = 'O'
            game2[0][0] = -1
            return
        if game[2][1] == 'X' or game[1][2] == 'X':
            game[2][2] = 'O'
            game2[2][2] = -1
            return
    # Stage 4 - If there is a free slot on a column/row/diagonal which mark with 2 O's and doesn't include X - mark it.
    if (diag_r == -1 and col[2] == -1) or (diag_r == -1 and sum(game2[0]) == -1):
        if game[0][2] == ' ':
            game[0][2] = 'O'
            game2[0][2] = -1
            return
    if (diag_r == -1 and col[0] == -1) or (diag_r == -1 and sum(game2[2]) == -1):
        if game[2][0] == ' ':
            game[2][0] = 'O'
            game2[2][0] = -1
            return
    # Stage 5 - if there is 3 slots marked, center is O and two opposite slots marked with X, play and edge slot.
    occupied = 0
    for j in range(3):
        for k in range(3):
            if not game[j][k] == ' ':
                occupied += 1
    if occupied == 3 and game[middle][middle] == 'O':
        if (game[0][0] == 'X' and game[2][2] == 'X') or (game[0][2] == 'X' and game[2][0] == 'X'):    # Prevent loss
            game[0][1] = 'O'
            game2[0][1] = -1
            return
        if game[1][0] == 'X' and game[1][2] == 'X':            # Create fork that leads to win
            game[0][1] = 'O'
            game2[0][1] = -1
            return
        if game[0][1] == 'X' and game[2][1] == 'X':            # Create fork that leads to win
            game[1][0] = 'O'
            game2[1][0] = -1
            return
        # Stage 6 - if 3 slots marked and center is O, play a corner that cover two of the opponent sign (X).
        for i in range(3):
            for j in range(3):
                if sum(game2[i]) == 1 and col[j] == 1:
                    if not game2[i][j] == 1:
                        game[i][j] = 'O'
                        game2[i][j] = -1
                        return
    # Stage 7 - if there is a free corner and its col and row are empty, play it.
    col_game3 = np.sum(game3, 0)
    if not sum(game3[0]):           # If a corner is vacant and also its row and column, mark it.
        if not col_game3[0]:
            game[0][0] = 'O'
            game2[0][0] = -1
            return
        if not col_game3[2]:
            game[0][2] = 'O'
            game2[0][2] = -1
            return
    if not sum(game3[2]):
        if not col_game3[0]:
            game[2][0] = 'O'
            game2[2][0] = -1
            return
        if not col_game3[2]:
            game[2][2] = 'O'
            game2[2][2] = -1
            return
    # Stage 8 - if center is free, play it.
    if game[middle][middle] == ' ':
        game[middle][middle] = 'O'
        game2[middle][middle] = -1
        return
    # Stage 9 - if 3 slots are free in a row or diagonally, play the corner.
    if not sum(game3[0]) or not np.trace(game3):
        game[0][0] = 'O'
        game2[0][0] = -1
        return
    if not sum(game3[2]) or not diag_r_game3:
        game[2][0] = 'O'
        game2[2][0] = -1
        return
    # Stage 10 - if corner is 'O' and there is two free opposite edges, play one of them.
    if game[middle][middle] == 'O':
        if np.trace(game3) == 1:
            game[0][0] = 'O'
            game2[0][0] = -1
            return
        if diag_r_game3 == 1:
            game[0][2] = 'O'
            game2[0][2] = -1
            return
        if sum(game3[1]) == 1:
            game[1][0] = 'O'
            game2[1][0] = -1
            return
        if col_game3[1] == 1:
            game[0][1] = 'O'
            game2[0][1] = -1
            return
    # Stage 11 - if there is a free corner, play it.
    if game[0][0] == ' ':
        game[0][0] = 'O'
        game2[0][0] = -1
        return
    if game[0][2] == ' ':
        game[0][2] = 'O'
        game2[0][2] = -1
        return
    if game[2][0] == ' ':
        game[2][0] = 'O'
        game2[2][0] = -1
        return
    if game[2][2] == ' ':
        game[2][2] = 'O'
        game2[2][2] = -1
        return
    # Stage 12 - if there is a free slot, mark it.
    for i in range(3):
        for j in range(3):
            if game[i][j] == ' ':
                game[i][j] = 'O'
                game2[i][j] = -1
                return


def calc(game, game2, diag_r, num):
    "This function helps the computer side function comp().\n"\
        "It counts how many times a symbol shows constantly in a row/column/diagonal line.\n"\
        "If it meets the conditions, it play the move for the computer and place 'O' in the designated place."""
    col = np.sum(game2, 0)
    for j in range(3):
        for k in range(3):
            if sum(game2[j]) == num:            # how many times a symbol shows constantly in a row
                if game[j][k] == ' ':
                    game[j][k] = 'O'
                    game2[j][k] = -1
                    return 1
            if col[j] == num:            # how many times a symbol shows constantly in a column
                if game[k][j] == ' ':
                    game[k][j] = 'O'
                    game2[k][j] = -1
                    return 1
            if np.trace(game2) == num:            # how many times a symbol shows constantly in the diagonal line
                if game[k][k] == ' ':
                    game[k][k] = 'O'
                    game2[k][k] = -1
                    return 1
            if diag_r == num:           # how many times a symbol shows constantly in the second diagonal line
                if game[k][2 - k] == ' ':
                    game[k][2 - k] = 'O'
                    game2[k][2 - k] = -1
                    return 1


def three(counter, current_player):
    "This function help the victory function. It prints out the winner if there is any."""
    if counter == 3 or counter == -3:
        xo_functions.game_board(game)
        print("%s win!" % current_player)
        return 1

def victory(current_player):
    "This function Count to victory."""
    diag_l = np.trace(game2)            # find if there is 3 same symbols on the main diagonal line
    if three(diag_l, current_player):
        return 1
    diag_r = 0
    for j in range(len(game)):
        diag_r += game2[j][2 - j]             # find if there is 3 same symbols on the second diagonal line
        if three(diag_r, current_player):
            return 1
        row = sum(game2[j])            # find if there is 3 same symbols on the same row
        if three(row, current_player):
            return 1
        col = np.sum(game2, 0)            # find if there is 3 same symbols on the same column
        if three(col[j], current_player):
            return 1


# The main starts from here
name1 = name()            # get the user name
name2 = "Computer"
user_names = (name1, name2)
first = xo_functions.begin(user_names)            # randomly decide who begin
print("%s begin first" % first)
points = play(user_names, first, game, game2, game3)            # play the game and get points you get
