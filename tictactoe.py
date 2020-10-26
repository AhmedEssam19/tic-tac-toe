"""
Tic Tac Toe Player
"""

import math

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
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    # X player get his turn if number os x's in board equal o's
    if count_x == count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    new_board = [[board[i][j] for j in range(3)] for i in range(3)]
    new_board[i][j] = player(new_board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (board[i][0] == X and board[i][1] == X and board[i][2] == X) or \
                (board[0][i] == X and board[1][i] == X and board[2][i] == X):
            return X

        elif (board[i][0] == O and board[i][1] == O and board[i][2] == O) or \
                (board[0][i] == O and board[1][i] == O and board[2][i] == O):
            return O

    if (board[0][0] == X and board[1][1] == X and board[2][2] == X) or \
            (board[0][2] == X and board[1][1] == X and board[2][0] == X):
        return X

    elif (board[0][0] == O and board[1][1] == O and board[2][2] == O) or \
            (board[0][2] == O and board[1][1] == O and board[2][0] == O):
        return O

    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    return not any(board[i][j] is EMPTY for i in range(3) for j in range(3))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winPlayer = winner(board)
    if winPlayer == X:
        return 1
    elif winPlayer == O:
        return -1
    else:
        return 0


def Maximum(board, causeAction, traceValue):
    """
    :param board: board we want to maximize its utility
    :param causeAction: action that produced this board
    :param traceValue: Value of the minimum utility of other boards
    :return: Maximum possible utility can get from this and the corresponding action
    """
    if terminal(board):
        return utility(board), causeAction

    maxValue = -2
    optimalAction = None
    for action in actions(board):
        value, _ = Minimum(result(board, action), action, maxValue)

        # Apply alpha-beta pruning to optimize performance
        if value > traceValue:
            return value, action

        if maxValue < value:
            maxValue = value
            optimalAction = action

    return maxValue, optimalAction


def Minimum(board, causeAction, traceValue):
    """
    :param board: board we want to minimize its utility
    :param causeAction: action that produced this board
    :param traceValue: Value of the maximum utility of other boards
    :return: minimum possible utility can get from this and the corresponding action
    """
    if terminal(board):
        return utility(board), causeAction

    minValue = 2
    optimalAction = None
    for action in actions(board):
        value, _ = Maximum(result(board, action), action, minValue)

        # Apply alpha-beta pruning to optimize performance
        if value < traceValue:
            return value, action

        if minValue > value:
            minValue = value
            optimalAction = action

    return minValue, optimalAction


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board)
    if currentPlayer == X:
        return Maximum(board, None, 2)[1]
    else:
        return Minimum(board, None, -2)[1]