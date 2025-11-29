# This is a Tic Tac Toe game program, player vs player.
import random
game = [[' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]


def name(i):
    "This function get the user name. """
    while True:
        print("Please insert your your name")
        p_name = input("Player %d: " % i)
        if p_name == '':
            continue
        return p_name


def begin(names):
    "This function randomly choose the beginner."""
    rand = random.randrange(2)
    return names[rand]


def choose(message):
    "This function let the beginner choose his symbol."""
    while True:
        try:
            value = int(input(message))
        except ValueError:
            print("Value Error")
            continue
        if value == 0:
            symbol = ('O', 'X')
            return symbol
        if value == 1:
            symbol = ('X', 'O')
            return symbol
        else:
            print("invalid number")


def letters():
    "This dictionary gives values for variables so we can 'refer' them in our game board."""
    letter = {'a': 0, 'b': 1, 'c': 2, '0': 0, '1': 1, '2': 2}
    return letter


def game_board(game):
    "This function print our board game."""
    print("    a  b  c ")
    for count, row in enumerate(game):
        print(count, '', end="", sep='  ' u'|\u0305 \u0305')
        print(sep='|\u0305 \u0305', *row)
        print(end="    \u0305 \u0305  \u0305 \u0305  \u0305 \u0305\r")


def play(names, p_symbols, beginner, game):
    "This function make the actual play each turn."""
    current_player = beginner
    letter = letters()
    new_p = p_symbols
    for i in range(9):
        while True:
            game_board(game)
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
                    game[a][b] = new_p[0]
                    if victory(game, new_p, current_player):
                        return "2", current_player, names
                    if current_player == names[0]:            # update the name for next player
                        current_player = names[1]
                    else:
                        current_player = names[0]
                    new_p = p_symbols[(i+1) % 2]            # update the symbol for next player
                    break
    game_board(game)
    print("Draw!")
    return '1'


def victory(game, new_p, current_player):
    "This function found if there is a victory."""
    if game[0][0] == new_p[0] and game[1][1] == new_p[0] and game[2][2] == new_p[0]:
        game_board(game)
        print("The winner is: %s!" % current_player)
        return 1
    if game[0][2] == new_p[0] and game[1][1] == new_p[0] and game[2][0] == new_p[0]:
        game_board(game)
        print("The winner is: %s!" % current_player)
        return 1
    for j in range(3):
        if game[j][0] == new_p[0] and game[j][1] == new_p[0] and game[j][2] == new_p[0]:
            game_board(game)
            print("The winner is: %s!" % current_player)
            return 1
        if game[0][j] == new_p[0] and game[1][j] == new_p[0] and game[2][j] == new_p[0]:
            game_board(game)
            print("The winner is: %s!" % current_player)
            return 1

if __name__ == "__main__":
    # The main starts from here
    name1 = name(1)            # get user names
    name2 = name(2)
    while name2 == name1:
        print("Must have different names")
        name2 = name(2)
    user_names = (name1, name2)
    first = begin(user_names)            # randomly decide who begin
    print("%s you begin first" % first)
    players_symbols = choose("please choose a symbol: \n0 for O, or 1 for X\n")
    points = play(user_names, players_symbols, first, game)            # play the game and get points you get
