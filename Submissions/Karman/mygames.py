from games import (Game)

class GameState:


    def __init__(self, to_move, board, firstPhase, label=None,):
        self.to_move = to_move
        self.board = board
        self.label = label
        self.firstPhase = firstPhase
        if len(board) > 7:
            self.firstPhase = False
        else:
            self.firstPhase = True

    def __str__(self):
        if self.label == None:
            return super(GameState, self).__str__()
        return self.label




class Teeko(Game):
    def __init__(self,h=5,v=5,k=4):
        self.h = h
        self.v = v
        self.k = k
        self.initial = GameState(to_move ='X', board = {}, firstPhase = True)


    def actions(self, state):
        try:
            return state.moves
        except:
            pass
        "Legal moves are any square not yet taken."
        moves = []
        secondMoves = []
        secondMovesDict = {}
        #include moves for both phases of games
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                if (x, y) not in state.board.keys():
                    moves.append((x, y))
        if state.firstPhase == True:
            state.moves = moves
        else:

            for x in range(1, self.h + 1):
                for y in range(1, self.v + 1):
                    if (x, y) in state.board.keys():
                        if state.to_move == state.board[(x,y)]:
                            secondMoves.append((x,y))
                            checkLeft(secondMoves, state)
                            # checkLeft()
                            # check left will add possible left moves to a dictionary with location, and possible moves
                            # if true, x-1,y will be added to possible moves for x,y
                            # makes a call to checkadjaecent
                            # checkRight
                            # checkUp
                            # checkDown

            state.moves = secondMoves
        return moves

    def checkLeft(self, secondMoves, state):
        for token in secondMoves:
            tokenX = token[0]
            tokenY = token[1]
            if tokenX ==  1:
                pass
            else if ((tokenX, tokenY) in state.board.keys()):




        #determines if game token is adjacent to any other game token
        # to be called from

    def checkAdjacent(secondMoves, state):
        for token in secondMoves:
            secondMoves.index(token)
            tokenX =  token.index(o)
            tokenY = token.index(1)
            if(((tokenX+1,tokenY) in state.board.keys()) and ((tokenX+1,tokenY) in state.board.keys())) or ((tokenX+1,tokenY+1) in state.board.keys()):


            return 0
        pass





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
        self.firstPhase = state.firstPhase
        player = state.to_move
        if state.firstPhase == True:
            board[move] = player
        else:
            # set actions for second phase moves
            # account for dictionary of dictionaries
            board[move] = player
        next_mover = self.opponent(player)
        return GameState(to_move=next_mover, board=board, firstPhase=self.firstPhase)


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

    def k_in_row(self, board, start, player, direction):
        "Return true if there is a line through start on board for player."
        (delta_x, delta_y) = direction
        x, y = start
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = start
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted start itself twice
        return n >= self.k


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
        # create conditional to check win on "block" win condition
        return 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

myGame = Teeko()

gameStart = GameState(
    to_move = 'X',
    board =  {},
    firstPhase = True,
    label = 'gameStart'
)

winin1 = GameState(
    to_move = 'X',
    board = {(1,1): 'X', (1,2): 'X',
             (2,1): 'O', (2,2): 'O',
            },
    label = 'winin1',
    firstPhase = True
)

myGames = {
    myGame: [
    ]
}