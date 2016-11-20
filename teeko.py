from games import (Game)

class GameState
    def __init__(self, to_move, board, label=None):
        self.to_move = to_move
        self.board = board
        self.label = label

    def __str__(self):
       firstPhase = True
        if self.label == None:
            return super(GameState, self).__str__()
        return self.label

class Teeko
    def __init__(self,h=5,v=5,k=4):
        self.h = h
        self.v = v
        self.k = k
        self.initial = GameState(to_move='X', board={})


def actions(self, state):
    try:
        return state.moves
    except:
        pass
    "Legal moves are any square not yet taken."
    moves = []
    #include moves for both phases of games
    for x in range(1, self.h + 1):
        for y in range(1, self.v + 1):
            if (x, y) not in state.board.keys():
                moves.append((x, y))
    state.moves = moves
    return moves


# defines the order of play
def opponent(self, player):
    if player == 'X':
        return 'O'
    if player == 'O':
        return 'X'
    return None


def result(self, state, move):
    if move not in self.actions(state):
        return state  # Illegal move has no effect
    board = state.board.copy()
    player = state.to_move
    board[move] = player
    next_mover = self.opponent(player)
    return GameState(to_move=next_mover, board=board)


def utility(self, state, player):
    "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
    try:
        return state.utility if player == 'X' else -state.utility
    except:
        pass
    board = state.board
    util = self.check_win(board, 'X')
    if util == 0:
        util = -self.check_win(board, 'O')
    state.utility = util
    return util if player == 'X' else -util


# Did I win?
def check_win(self, board, player):
    # check rows
    for y in range(1, self.v + 1):
        if self.k_in_row(board, (1, y), player, (1, 0)):
            return 1
    # check columns
    for x in range(1, self.h + 1):
        if self.k_in_row(board, (x, 1), player, (0, 1)):
            return 1
    # check \ diagonal
    if self.k_in_row(board, (1, 1), player, (1, 1)):
        return 1
    # check / diagonal
    if self.k_in_row(board, (3, 1), player, (-1, 1)):
        return 1
    return 0