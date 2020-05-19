"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for col in row:
            if col == X:
                x_count += 1
            elif col == O:
                o_count += 1

    if x_count > o_count:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)

    if board_copy[action[0]][action[1]] != EMPTY:
        raise Exception("Player " + board_copy[action[0]][action[1]] + " has already gone there!")
    else:
        board_copy[action[0]][action[1]] = player(board_copy)
        return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        # Check for a row win
        if board[i][0] != EMPTY:
            if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
                return board[i][0]

        # Check for a column win
        if board[0][i] != EMPTY:
            if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
                return board[0][i]

    # Check for a diagonal win
    if board[0][0] != EMPTY:
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]

    if board[0][2] != EMPTY:
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        terminal = True
    else:
        none_count = 0
        for row in board:
            for col in row:
                if col == None:
                    none_count += 1
        if none_count == 0:
            terminal = True
        else:
            terminal = False

    return terminal

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        utility = 1
    elif winner(board) == "O":
        utility = -1
    else:
        utility = 0

    return utility

def max_value(state):
    if terminal(state) == True:
        return utility(state), ()
    best_score = float("-inf")
    for action in actions(state):
        new_score = min_value(result(state,action))[0]
        if new_score >= best_score:
            best_action = action
            best_score = new_score
        if best_score == 1:
            break
    return best_score, best_action

def min_value(state):
    if terminal(state) == True:
        return utility(state), ()
    best_score = float("inf")
    for action in actions(state):
        new_score = max_value(result(state,action))[0]
        if new_score <= best_score:
            best_action = action
            best_score = new_score
        if best_score == -1:
            break
    return best_score, best_action

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == "X":
        return max_value(board)[1]
    else:
        return min_value(board)[1]