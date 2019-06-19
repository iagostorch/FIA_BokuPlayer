# -*- coding: utf-8 -*-

import copy
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import node
import utils
import c
import c1
import c2
import random
import datetime


forbidden_moves = []
identifier = 0

#####################
#       FUNCTIONS FROM THE CLIENT SIDE
def choose_move(game, player):
    global forbidden_moves
    board = game.board
    # print(board)

    new_board = []
    for column in board:
        new_column = []
        for element in column:
            new_column.append(str(element))
        new_board.append(new_column)
        new_column = []
    board = new_board
    # print(board)


    if(player == 1):    # last_player is opposite of current player
        root = node.Node(-1,board,0,2,0)
    else:
        root = node.Node(-1,board,0,1,0)

    server_moves = game.get_available_moves()
    moves = utils.adapt_index(server_moves)
    forbidden_moves = utils.get_forbidden_moves(board, moves)

    # print("SERVER MOVES")
    # print(server_moves)

    # if(len(forbidden_moves) > 0):
    #     print("FORBIDDEN MOVES")
    #     print(forbidden_moves)
    #     print()

    # print("INITIAL BOARD")
    # print(board)
    # print()


    #   If the returned moves characterize positions
    #   in which there are enemy pieces, then we must
    #   remove one enemy piece
    if(utils.is_removal(board, player, moves)):
        # print("REMOVE PIECE -- RANDOM")
        return random.choice(moves)

    else:
        # print("iNSERT PIECE")
        #score_old = minimax_place(root, player)
        alpha = -9999999999
        beta  = 9999999999
        score = minimax_alphabeta(root, player, alpha, beta)
        # if(score_old != score):
        #   print("\n\n\n\n")
        #   print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #   print("MINIMAX DIVERGENCE WITH AND WITHOUT ALPHABETA")
        #   print("Old " + str(score_old) + "\tAB " + str(score))
        #   print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #   print("\n\n\n\n")
        #   exit()
        # print("score " + str(score))

    nodes = [root]

    # print
    # print(root)
    # print

    children = root.get_lowers()
    max_score = children[0].get_score()
    move = children[0].get_move()

    max_score_array = [max_score]
    move_array = [move]

    for child in children:
        # print(str(child.get_score()))
        if(player == 1): # maximiza
            # If current score is greater than max, score is new max
            # If current score equals max, current is added to max list
            if(child.get_score() > max_score_array[0]):
                max_score_array = [child.get_score()]
                move_array = [child.get_move()]
            elif(child.get_score() == max_score_array[0]):
                max_score_array.append(child.get_score())
                move_array.append(child.get_move())
        else: # minimiza
            if(child.get_score() < max_score_array[0]):
                max_score_array = [child.get_score()]
                move_array = [child.get_move()]
            elif(child.get_score() == max_score_array[0]):
                max_score_array.append(child.get_score())
                move_array.append(child.get_move())
    # print("DO ONE OF THESE -- STARTING INDEX ZERO")
    # print(move_array)
    # print()
    return random.choice(move_array)

####


def minimax_alphabeta(curr_node, player, alpha, beta):
    # end = datetime.datetime.now()
    # diff = end - start
    # print(diff)
    # print(curr_node.get_board())
    global identifier
    global forbidden_moves
    score_list = []
    identifier += 1
    
    if(curr_node.get_depth() >= c.max_depth):   # if we hit max depth, recursion is stopped
        score = utils.calc_differential_score_distinct_weights(curr_node.get_board(), player)
        curr_node.set_score(score)
        return score
    elif(curr_node.is_final()):                 # if current state is final, recursion is stopped
        score = utils.calc_differential_score_distinct_weights(curr_node.get_board(), player)
        curr_node.set_score(score)
        return score


    moves = utils.get_available_moves(curr_node.get_board())

    # If there are forbidden moves, they must be removed from available moves list
    if(len(forbidden_moves) > 0):
        # print("REMOVE FORBIDDEN MOVES")
        # print(str(forbidden_moves))
        # print()
        moves = utils.remove_forbidden_moves(moves, forbidden_moves)
    
    if(player == 1):
        value = -9999999999
        for move in moves:
            new_board = utils.perform_move(copy.deepcopy(curr_node.get_board()), move, player)
            new_node = node.Node(curr_node, new_board, curr_node.get_depth() + 1, player, move)
            new_node.set_identifier(identifier)
            # print("New move " + str(move[0]) + ',' + str(move[1]))
            # print(new_node.get_board())
            # print()
            # print
            curr_node.add_lower(new_node)

            move_score = minimax_alphabeta(new_node, 2, alpha, beta)

            value = max(move_score, value)
            alpha = max(alpha, value)
            if(alpha >= beta):
                break

        curr_node.set_score(value)
        return value        
    else:
        value = 9999999999
        for move in moves:
            new_board = utils.perform_move(copy.deepcopy(curr_node.get_board()), move, player)
            new_node = node.Node(curr_node, new_board, curr_node.get_depth() + 1, player, move)
            new_node.set_identifier(identifier)
            # print("New move " + str(move[0]) + ',' + str(move[1]))
            # print(new_node.get_board())
            # print()
            # print
            curr_node.add_lower(new_node)

            move_score = minimax_alphabeta(new_node, 1, alpha, beta)

            value = min(move_score, value)
            beta = min(beta, value)

            if(alpha >= beta):
                break

        curr_node.set_score(value)
        return value                        

######################




forbidden_moves = []

def get_coordinates(column, line):
    x0 = 10
    y0 = 57

    w = 16.5
    h = 19.5

    incl = 10

    x = (column) * w + x0
    if column <= 5:
        y = line * h - incl * column + y0
    else:
        y0 = h - incl * 5 + y0
        y = y0 + line * h - h - incl * (5 - column)

    return (x, y)


def print_board(board):
    img = mpimg.imread('board.png')

    ig, ax = plt.subplots(1)
    ax.set_aspect('equal')

    for column in range(0, len(board)):
        for line in range(0, len(board[column])):
            (x, y) = get_coordinates(column, line)
            if board[column][line] == 0:
                color = 'white'
            elif board[column][line] == 1:
                color = 'red'
            else:
                color = 'green'
            circ = Circle((x, y), 5, color=color)
            ax.add_patch(circ)
    plt.imshow(img)


class Game:
    board = []
    player = 1
    ended = False
    waiting_removal = False
    forbidden_moves = None
    movements = 0
    last_column = 0
    last_line = 0

    # Initialize the board. 0 is empty space. 1 and 2 are the players.
    def init_board(self):
        self.ended = False
        self.board = []
        self.player = 1
        self.waiting_removal = False
        self.forbidden_moves = None
        self.movements = 0

        self.last_column = -1
        self.last_line = -1

        for column in range(11):
            if column <= 5:
                height = 5 + column
            else:
                height = 15 - column
            self.board.append([0] * height)

                                #upper left     #lower left
        self.board =             [[0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0]]
                               #upper right    # lower right


                        # TEST CASE COM O TABULEIRO EM ESTAGIO FINAL
        # self.board =             [[0, 2, 0, 2, 0],
        #                         [0, 0, 0, 0, 1, 0],
        #                       [0, 0, 2, 0, 2, 0, 0],
        #                     [0, 1, 1, 1, 2, 1, 2, 0],
        #                   [0, 1, 0, 0, 0, 0, 0, 0, 0],
        #                  [0, 1, 0, 0, 2, 1, 1, 2, 2, 1],
        #                   [0, 0, 2, 0, 0, 1, 0, 0, 2],
        #                     [0, 0, 0, 0, 0, 0, 1, 1],
        #                       [0, 2, 2, 0, 2, 0, 2],
        #                         [0, 1, 0, 2, 0, 1],
        #                          [1, 0, 2, 0, 1]]
                               #upper right    # lower right



                        # TEST CASE PARA REMOVER UMA PECA ADVERSARIA
        # self.board =             [[0, 0, 0, 0, 0],
        #                         [0, 0, 0, 0, 0, 0],
        #                       [0, 0, 0, 0, 0, 0, 0],
        #                     [0, 2, 0, 0, 0, 0, 2, 0],
        #                   [1, 1, 0, 0, 0, 0, 2, 0, 0],
        #                  [2, 1, 2, 0, 0, 0, 0, 0, 0, 0],
        #                   [1, 1, 2, 0, 0, 0, 0, 0, 0],
        #                     [1, 1, 0, 0, 0, 0, 0, 0],
        #                       [1, 2, 0, 0, 0, 0, 0],
        #                         [2, 0, 0, 0, 0, 0],
        #                          [0, 0, 0, 0, 0]]
        #                        #upper right    # lower right


        # #                 # TEST CASE PARA NAO INSERIR UMA PECA RECEM REMOVIDA. JOGAR COMO PLAYER 2
        # self.board =             [[0, 0, 1, 0, 0],
        #                         [0, 0, 0, 0, 0, 0],
        #                       [0, 0, 0, 0, 0, 0, 0],
        #                     [0, 0, 0, 0, 0, 0, 0, 0],
        #                   [0, 0, 0, 0, 1, 0, 0, 0, 0],
        #                  [0, 0, 0, 1, 2, 2, 2, 1, 0, 0],
        #                   [0, 0, 0, 2, 0, 0, 0, 0, 0],
        #                     [0, 0, 0, 0, 0, 0, 0, 0],
        #                       [0, 0, 0, 0, 0, 0, 0],
        #                         [0, 0, 0, 0, 0, 0],
        #                          [2, 0, 1, 0, 0]]



    def get_position(self, column, line):
        return self.board[column - 1][line - 1]

    def set_position(self, column, line, state):
        b = copy.deepcopy(self.board)
        b[column - 1][line - 1] = state
        return b

    # Put a piece on a board. State is the player (or 0 to remove a piece)
    def place_piece(self, column, line, state):
        self.board = self.set_position(column, line, state)

    # Get a fixed-size list of neighbors: [top, top-right, top-left, down, down-right, down-left].
    # None at any of those places where there's no neighbor
    def neighbors(self, column, line):
        l = []

        if line > 1:
            l.append((column, line - 1))  # up
        else:
            l.append(None)

        if (column < 6 or line > 1) and (column < len(self.board)):
            if column >= 6:
                l.append((column + 1, line - 1))  # upper right
            else:
                l.append((column + 1, line))  # upper right
        else:
            l.append(None)
        if (column > 6 or line > 1) and (column > 1):
            if column > 6:
                l.append((column - 1, line))  # upper left
            else:
                l.append((column - 1, line - 1))  # upper left
        else:
            l.append(None)

        if line < len(self.board[column - 1]):
            l.append((column, line + 1))  # down
        else:
            l.append(None)

        if (column < 6 or line < len(self.board[column - 1])) and column < len(self.board):
            if column < 6:
                l.append((column + 1, line + 1))  # down right
            else:
                l.append((column + 1, line))  # down right
        else:
            l.append(None)

        if (column > 6 or line < len(self.board[column - 1])) and column > 1:
            if column > 6:
                l.append((column - 1, line + 1))  # down left
            else:
                l.append((column - 1, line))  # down left
        else:
            l.append(None)

        return l

    # Check if there's any possible removal (trapped pieces)
    # Returns (player,[positions]), where [positions] is a list of the two possibilities to be removed
    def can_remove(self, player):
        removals = []
        l = []

        #test vertical
        
        #test upward
        s = ""
        for line in range(max(self.last_line-3,1), self.last_line+1):
          
            state = self.board[self.last_column-1][line-1]
            s += str(state)
        
        if ("1221" in s and player==1) or ("2112" in s and player==2):
            removals.append([(self.last_column,self.last_line-1),(self.last_column,self.last_line-2)])

        #test downward
        s = ""
        for line in range(self.last_line,  min(self.last_line+3,len(self.board[self.last_column-1]))+1):
        
            state = self.board[self.last_column-1][line-1]
            s += str(state)
        
        if ("1221" in s and player==1) or ("2112" in s and player==2):
            removals.append([(self.last_column,self.last_line+1),(self.last_column,self.last_line+2)])
                 

        # test upward diagonals
        diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = self.board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = self.neighbors(column, line)[1]
            if coords == None:
                break

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            # print(coords)
            column = coords[0]
            line = coords[1]
            state = self.board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            # print(s)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = self.neighbors(column, line)[5]
            if coords == None:
                break

        # test downward diagonals
        diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                 (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = self.board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = self.neighbors(column, line)[2]
            if coords == None:
                break

        col = self.last_column
        line = self.last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            # print(coords)
            column = coords[0]
            line = coords[1]
            state = self.board[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            # print(s)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = self.neighbors(column, line)[4]
            if coords == None:
                break

        if len(removals) > 0:
            removals = [item for sublist in removals for item in sublist]
            return removals
        else:
            return None

    # Check if a board is in an end-game state. Returns the winning player or None.
    def is_final_state(self):
        # test vertical
        for column in range(len(self.board)):
            s = ""
            for line in range(len(self.board[column])):
                state = self.board[column][line]
                s += str(state)
                if "11111" in s:
                    return 1
                if "22222" in s:
                    return 2

        # test upward diagonals
        diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
        for column_0, line_0 in diags:
            s = ""
            coords = (column_0, line_0)
            while coords != None:
                column = coords[0]
                line = coords[1]
                state = self.board[column - 1][line - 1]
                s += str(state)
                if "11111" in s:
                    return 1
                if "22222" in s:
                    return 2
                coords = self.neighbors(column, line)[1]

        # test downward diagonals
        diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                 (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
        for column_0, line_0 in diags:
            s = ""
            coords = (column_0, line_0)
            while coords != None:
                column = coords[0]
                line = coords[1]
                state = self.board[column - 1][line - 1]
                s += str(state)
                if "11111" in s:
                    return 1
                if "22222" in s:
                    return 2
                coords = self.neighbors(column, line)[4]

        return None

    # Returns a list of positions available on a board
    def get_available_moves(self):
        l = []

        removal_options = self.can_remove(self.player)
        if removal_options != None:
            self.waiting_removal = True
            return removal_options
        else:
            for column in range(len(self.board)):
                for line in range(len(self.board[column])):
                    if self.board[column][line] == 0:
                        if (column + 1, line + 1) != self.forbidden_moves:
                            l.append((column + 1, line + 1))
            return l

    def get_available_boards(self):
        l = self.get_available_moves()
        possible_boards = []
        for (column, line) in l:
            possible_boards.append(
                self.set_position(column, line, self.player))
        return (self.player, possible_boards)

    def take_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1
        return self.player

    def make_move(self, player, column, line):

        if self.ended:
            return (-1, "Game is over")

        if player != self.player:
            return (-2, "Not your turn")

        if column > len(self.board) or column < 0:
            return (-3, "No such column")

        if line < 0 or line > len(self.board[column - 1]):
            return (-4, "No such line in column %d" % column)

        if (column, line) == self.forbidden_moves:
            return (-5, "Position (%d,%d) not available (forbidden)" % (column, line))

        if self.get_position(column, line) == 0 or self.waiting_removal:
            forbidden_just_set = False
            if self.waiting_removal:
                if (column, line) in self.can_remove(self.player):
                    state = 0
                    self.waiting_removal = False
                    self.forbidden_moves = (column, line)
                    forbidden_just_set = True
                else:
                    return (-6, "Invalid removal")
            else:
                state = player
            self.board = self.set_position(column, line, state)
            if not forbidden_just_set:
                self.forbidden_moves = None
        else:
            return (-7, "Position (%d,%d) not available" % (column, line))

        f = self.is_final_state()
        if f != None:
            self.ended = True
            return (0, "%d wins" % f)

        self.last_line = line
        self.last_column = column

        # Check for sandwiches
        possible_states = []

        removal_options = self.can_remove(self.player)
        if removal_options != None:
            self.waiting_removal = True
            return (2, "must remove")
            # for option in removal_options:
            #     possible_states.append(self.set_position(option[0],option[1],0))
            # return (player,possible_states)
        else:
            self.take_turn()

        self.movements += 1

        return (1, "ok")


###### SERVER ######

game = Game()
game.init_board()

board = game.board
fim = False

while(fim == False):
    player = game.player
    start = datetime.datetime.now()
    move = choose_move(game, player)
    end = datetime.datetime.now()
    diff = end-start
    print("Player " + str(player) + ", MOVE  " + str(move) + ", TIME " + str(diff))
    resp = game.make_move(player, move[0]+1, move[1]+1)
    # print(resp)

    ganhador = game.is_final_state()
    if(ganhador != None):
        print("WINNER " + str(ganhador))
        utils.count_occurrences(board, player)
        print("FOI")
        utils.print_occurrences()
        fim = True

    moves = game.get_available_moves()
    if(len(moves) == 0):
        print("EMPATE")
        fim = True


