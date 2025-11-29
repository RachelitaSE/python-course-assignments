# This program shows high scores in tic tac toe game program.
# You can play player vs player, player vs computer, show high scores and exit.
from pathlib import Path
from collections import OrderedDict

import XO as xo_functions

import numpy as np          # need to pip install numpy


# functions stars from here
def make_file():
    "This function make sure there is a file to read from it.\n"\
        "It appends nothing to the file (appends '') in case its already exist."""
    file = open('high_score.dat', 'a')  # Make sure there is a file to read
    file.write('')
    file = open('high_score.dat', 'r')
    d = file.read()
    file.close()
    return d


def read():
    "This function reads data from a file, save it to a dictionary and return it"""
    data = dict()
    with open('high_score.dat', 'r') as raw_data:
        for item in raw_data:  # read back from file to a dictionary
            if ':' in item:
                key, value = item.split(':', 1)
                data[key] = int(str.strip(value, '\n'))
            else:
                pass  # deal with bad lines of text here
    return data


def sort_dict(dict):
    "This function get a dictionary and return it sorted by value in descending order"""
    r = OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))        # reverse sort by value dictionary
    return r


def write(rev):
    "This function get a dictionary and write its keys and values to a file, line by line"
    with open('high_score.dat', 'w') as file:
        for key, value in rev.items():
            file.write('%s: %s\n' % (key, value))  # write high scores to file in descending order
    file.close()


# main starts from here
while True:
    choose = input(" Main menu: \n 1 for Player vs Player \n 2 for Player vs Computr \n "
                   "3 for high score \n 0 for exit \n please choose an option: ")

    if choose == '1':           # player vs player
        exec(open(f"{Path.cwd()}/XO.py").read())
        make_file()  # make sure there is a file to read
        scores = read()  # read from file to a dictionary (values represented as string type at this stage)
        
        if points[0] == '2':            # check if there is a winner
            winner = points[1]
            names = points[2]
            if winner == names[0]:
                loser = names[1]
            else:
                loser = names[0]

            if winner in scores:            # check if name is already on the dictionary
                s = int(scores[winner]) + 2            # convert dict values from string type to int
                scores[winner] = s
            else:
                scores[winner] = 2            # if not, add new name with value to the dictionary
            if not loser in scores:
                scores[loser] = 0
            else:
                scores[loser] = int(scores[loser])

        if points[0] == '1':            # if its a draw
            player_a = user_names[0]
            player_b = user_names[1]
            if player_a in scores:
                s = int(scores[player_a]) + 1
                scores[player_a] = s
            else:
                scores[player_a] = 1
            if player_b in scores:
                s = int(scores[player_b]) + 1
                scores[player_b] = s
            else:
                scores[player_b] = 1
        r_dic = sort_dict(scores)            # reverse sort the dictionary in descending order
        write(r_dic)            # write to file in descending order
        continue

    if choose == '2':            # player vs computer
        exec(open(f"{Path.cwd()}/XO_vs_comp.py").read())
        make_file()
        scores = read()
        if points == '2':
            if name1 in scores:
                s = int(scores[name1]) + 2          # convert key values from string to int
                scores[name1] = s
            else:
                scores[name1] = 2           # if player is not on the high score "list" yet, add him to the dict.
        if points == '1':
            if name1 in scores:
                s = int(scores[name1]) + 1
                scores[name1] = s
            else:
                scores[name1] = 1
        if points == '0':
            if not name1 in scores:
                scores[name1] = 0
        r_dic = sort_dict(scores)
        write(r_dic)
        continue

    if choose == "3":            # high score list
        content = make_file()
        if content == "":            # Make sure there is any high score
            print("There is no high score yet.")
        else:
            print("HIGH SCORES:\n" + content)
        continue

    if choose == '0':            # Exit
        break
    else:
        print("Invalid input")
        continue
