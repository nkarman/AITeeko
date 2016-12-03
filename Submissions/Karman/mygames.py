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
        secondMovesDict = {}
        self.secondMovesDict = secondMovesDict


    def actions(self, state):
        try:
            return state.moves
        except:
            pass
        "Legal moves are any square not yet taken."
        moves = []
        secondMoves = []
        #include moves for both phases of games
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                if (x, y) not in state.board.keys():
                    #(x,y) = (y,x)
                    moves.append((x, y))
        if state.firstPhase == True:
            state.moves = moves
            return moves
        else:
            for x in range(1, self.h + 1):
                for y in range(1, self.v + 1):
                    if (x, y) in state.board.keys():
                        if state.to_move == state.board[(x,y)]:
                            #check left statements
                            if x is not 1:
                                if (x-1,y) not in state.board.keys():
                                    self.secondMovesDict[x,y, "left"] = (x-1,y)
                                    secondMoves.append((x,y, "left"))
                            #check right statements
                            if x is not 5:
                                if (x+1,y) not in state.board.keys():
                                    self.secondMovesDict[x,y, "right"] = (x+1,y)
                                    secondMoves.append((x,y,"right"))
                            #check up statements
                            if y is not 1:
                                if (x, y-1) not in state.board.keys():
                                    self.secondMovesDict[x,y,"up"] = (x,y-1)
                                    secondMoves.append((x, y, "up"))
                            #check down statements
                            if y is not 5:
                                if (x, y+1) not in state.board.keys():
                                    self.secondMovesDict[x,y,"down"] = (x,y+1)
                                    secondMoves.append((x, y, "down"))
            state.moves = secondMoves
        return secondMoves



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
            x = move[0]
            y = move[1]
            if move[2] == "left":
                del board[x,y]
                board[x - 1, y] = player
            if move[2] == "right":
                del board[x, y]
                board[x + 1, y] = player
            if move[2] == "up":
                del board[x, y]
                board[x, y - 1] = player
            if move[2] == "down":
                del board[x, y]
                board[x, y + 1] = player
        next_mover = self.opponent(player)
        return GameState(to_move=next_mover, board=board, firstPhase=self.firstPhase)


    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        try:
            return state.utility if player == 'X' else -state.utility
        except:
            pass
        board = state.board
        util = self.check_win(board, 'X', state =state)
        if util == 0:
            util = -self.check_win(board, 'O', state= state)
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
    def check_win(self, board, player, state):
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

        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                if (x, y) in state.board.keys():
                    if state.to_move == state.board[(x, y)]:
                        #bottom left corner
                        if (x,y-1) in state.board.keys() and (x+1,y-1) in state.board.keys() and (x+1,y) in state.board.keys():
                            if state.board[x,y-1] == state.to_move and state.board[x+1 ,y-1] == state.to_move and state.board[x+1,y] == state.to_move:
                                return 1
                        #bottom right corner
                        if (x,y-1) in state.board.keys() and (x-1,y-1) in state.board.keys() and (x-1,y) in state.board.keys():
                            if state.board[x, y - 1] == state.to_move and state.board[x-1,y-1] == state.to_move and state.board[x-1,y] == state.to_move:
                                return 1
                        #top right corner
                        if (x-1,y) in state.board.keys() and (x-1,y+1) in state.board.keys() and (x,y+1) in state.board.keys():
                            if state.board[x-1,y] == state.to_move and state.board[x-1, y+1] == state.to_move and state.board[x,y+1] == state.to_move:
                                return 1
                        # top left corner
                        if (x,y+1) in state.board.keys() and (x+1,y+1) in state.board.keys() and (x+1,y) in state.board.keys():
                            if state.board[x,y+1] == state.to_move and state.board[x+1,y+1] == state.to_move and state.board[x+1, y + 1] == state.to_move:
                                return 1
                        break
        return 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((y, x), '.'), end=' ')
            print()

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return self.utility(state, state.to_move) != 0 or len(self.actions(state)) == 0

myGame = Teeko()

myGames = {
    myGame: [
    ]
}