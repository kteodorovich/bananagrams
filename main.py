import random

import numpy as np

'''
2: J, K, Q, X, Z
3: B, C, F, H, M, P, V, W, Y
4: G
5: L
6: D, S, U
8: N
9: T, R
11: O
12: I
13: A
18: E
'''


def get_letter_bank():
    letter_bank = []
    letter_bank += ['A'] * 13
    letter_bank += ['B'] * 3
    letter_bank += ['C'] * 3
    letter_bank += ['D'] * 6
    letter_bank += ['E'] * 18
    letter_bank += ['F'] * 3
    letter_bank += ['G'] * 4
    letter_bank += ['H'] * 3
    letter_bank += ['I'] * 12
    letter_bank += ['J'] * 2
    letter_bank += ['K'] * 2
    letter_bank += ['L'] * 5
    letter_bank += ['M'] * 3
    letter_bank += ['N'] * 8
    letter_bank += ['O'] * 11
    letter_bank += ['P'] * 3
    letter_bank += ['Q'] * 2
    letter_bank += ['R'] * 9
    letter_bank += ['S'] * 6
    letter_bank += ['T'] * 9
    letter_bank += ['U'] * 6
    letter_bank += ['V'] * 3
    letter_bank += ['W'] * 3
    letter_bank += ['X'] * 2
    letter_bank += ['Y'] * 3
    letter_bank += ['Z'] * 2

    letter_bank.sort()
    return letter_bank


def load_scrabble_words():
    words = []
    with open('scrabble.txt', 'r') as f:
        for line in f.readlines()[2:]:
            words.append(line.strip())

    return words


def realloc(board: np.ndarray, loc):
    if loc[0] < 0:
        new_rows = np.full((abs(loc[0]), board.shape[1]), ' ')
        board = np.concatenate((new_rows, board), 0)
    elif loc[0] >= board.shape[0]:
        new_rows = np.full((loc[0] - board.shape[0] + 1, board.shape[1]), ' ')
        board = np.concatenate((board, new_rows), 0)

    if loc[1] < 0:
        new_cols = np.full((board.shape[0], abs(loc[1])), ' ')
        board = np.concatenate((new_cols, board), 1)
    elif loc[1] >= board.shape[1]:
        new_cols = np.full((board.shape[0], loc[1] - board.shape[1] + 1), ' ')
        board = np.concatenate((board, new_cols), 1)

    return board


def add_letter(board, hand, letter, loc):
    if loc[0] < 0 or loc[0] >= len(board) or loc[1] < 0 or loc[1] >= len(board[0]):
        board = realloc(board, loc)
        if loc[0] < 0:
            loc = (0, loc[1])
        if loc[1] < 0:
            loc = (loc[0], 0)

    if board[loc] != ' ' and board[loc] != letter:
        hand.append(board[loc])

    board[loc] = letter
    if letter != ' ':
        hand.remove(letter)

    return board, hand


def print_board(board):
    print('  ', end='')
    for i in range(board.shape[1]):
        space = ' ' if i < 10 else ''
        print(f'  {space}{i}', end='')
    print()

    for i, row in enumerate(board):
        space = ' ' if i < 10 else ''
        print(str(i) + space + ' [', end='')
        for j, letter in enumerate(row):
            space1 = '  ' if j < 10 else ' '
            space2 = space1 if j < len(row) - 1 else ''
            print(f"'{letter}'{space2}", end='')
        print(']')


def draw_random_letter(letter_bank):
    idx = random.randint(0, len(letter_bank) - 1)
    return letter_bank.pop(idx)


def get_hand(letter_bank, num):
    hand = []
    while len(hand) < num:
        hand.append(draw_random_letter(letter_bank))

    return hand


def dump(letter_bank, letter):
    if len(letter_bank) < 3:
        print('cant dump right now!')
        return []

    letter_bank.append(letter)
    letter_bank.sort()

    out = []
    for i in range(3):
        out.append(draw_random_letter(letter_bank))

    return out


def get_all_words(board):
    words = []
    word = ''
    for row in board:
        for letter in row:
            if letter != ' ':
                word += letter
            elif word != '':
                words.append(word)
                word = ''

        if word != '':
            words.append(word)
            word = ''

    word = ''
    for col in board.T:
        for letter in col:
            if letter != ' ':
                word += letter
            elif word != '':
                words.append(word)
                word = ''

        if word != '':
            words.append(word)
            word = ''

    return [word for word in words if len(word) > 1]


def check_all_words(words, scrabble_words):
    for word in words:
        if word not in scrabble_words:
            print(word, 'is not a valid scrabble word!')
            return False

    return True


if __name__ == '__main__':
    board = np.full((16, 16), ' ')
    letter_bank = get_letter_bank()
    hand = get_hand(letter_bank, 21)
    scrabble_words = load_scrabble_words()

    while True:
        print_board(board)
        print(hand)
        choice = int(input('1. add letter\n2. remove letter\n3. dump\n4. check words\n'))

        if choice == 1:
            letter = input('input a letter: ').upper()
            if letter not in hand:
                print('invalid letter!')
                continue

            loc = (int(input('row: ')), int(input('col: ')))

            board, hand = add_letter(board, hand, letter, loc)

            if len(hand) == 0 and check_all_words(get_all_words(board), scrabble_words):
                let = draw_random_letter(letter_bank)
                print(f'peel! got letter: [{let}]')
                hand.append(let)


        elif choice == 2:
            loc = (int(input('row: ')), int(input('col: ')))
            board, hand = add_letter(board, hand, ' ', loc)


        elif choice == 3:
            letter = input('which letter are you dumping? ').upper()
            new_letters = dump(letter_bank, letter)
            print('dumped', letter, 'and got:', new_letters)
            hand.remove(letter)
            hand += new_letters

        elif choice == 4:
            words = get_all_words(board)
            print(words)
            if check_all_words(words, scrabble_words):
                print('all words valid!')

        else:
            print('invalid input!')
