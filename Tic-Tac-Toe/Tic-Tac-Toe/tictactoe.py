"""
Tic Tac Toe Player
"""
import random
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
    countx = 0
    county = 0
    for i in board:
        for j in i:
            if j=="X":
                countx += 1
            elif j == "O":
                county += 1
    if countx == 0 and county == 0:
        return X
    elif countx+county == 9:
        return "Anything"
    elif countx > county:
       return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    pactions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                pactions.add((i,j,))
    try:
        return set(random.shuffle(list(pactions)))
    except:
        return pactions
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    ib = action[0]
    jb = action[1]
    if board[ib][jb] != EMPTY:
        raise ValueError
    playert = ""
    playert = player(board)
    deepcopy = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    for i in range(3):
        for j in range(3):
            deepcopy[i][j] = board[i][j]
    deepcopy[ib][jb] = playert
    return deepcopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #horizontal check
    for i in range(0,3):
        j = 0
        if board[i][j] == "X" and board[i][j+1] == "X" and board[i][j+2] == "X":
            return X
        elif board[i][j] == "O" and board[i][j+1] == "O" and board[i][j+2] == "O":
           return O
    #vertical Check
    for i in range(0,3):
        j = 0
        if board[j][i] == "X" and board[j+1][i] == "X" and board[j+2][i] == "X":
            return X
        elif board[j][i] == "O" and board[j+1][i] == "O" and board[j+2][i] == "O":
           return O
    #diagonal Check
    if board[0][0] == "X" and board[1][1] == "X" and board[2][2] == "X":
        return X
    elif board[0][0] == "O" and board[1][1] == "O" and board[2][2] == "O":
       return O
    elif board[0][2] == "X" and board[1][1] == "X" and board[2][0] == "X":
        return X
    elif board[0][2] == "O" and board[1][1] == "O" and board[2][0] == "O":
       return O

    #no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #win
    if winner(board) != None:
        return True

    #Tie
    for i in board:
        if EMPTY in i:
            break
    else:
        return True

    #game is ongoing
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winnerv = winner(board)
    if winnerv == X:
        return 1
    elif winnerv == O:
        return -1
    else:
        return 0




def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -10 #-inf
        for action in actions(board):
            v = max(v,min_value(result(board,action)))
        return v
    def min_value(board):
        if terminal(board):
            return utility(board)
        v = 10 #+inf
        for action in actions(board):
            v = min(v,max_value(result(board,action)))
        return v
    def Max(board):
        oaction = []
        value = []
        action = actions(board)
        for i in action:
            oaction.append(i)
            value.append(min_value(result(board,i)))
        return oaction[value.index(max(value))]
    def Min(board):
        oaction = []
        value = []
        action = actions(board)
        for i in action:
            oaction.append(i)
            value.append(max_value(result(board,i)))
        return oaction[value.index(min(value))]
    if player(board) == X:
        return Max(board)
    else:
        return Min(board)
