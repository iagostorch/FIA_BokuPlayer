# TODO:	improve performance of eval_empty_edges_two/three/four
#		to allow overlapping empty spots -> 0110110

import c
from multiprocessing import Pool


def remove_forbidden_moves(moves, forbidden_moves):
	possible_moves = []

	for move in moves:
		if(move in forbidden_moves):	# if current move is in forbidden moves list, do nothing
			continue
		else:							# if its not forbidden, add to possible moves list
			possible_moves.append(move)

	return possible_moves


def get_forbidden_moves(board, server_moves):
	local_moves = get_available_moves(board)
	# print("MOVIMENTOS LOCAL")
	# print(local_moves)

	forbidden_moves = []

	for move in local_moves:
		if list(move) in server_moves:
			continue
		else:
			# print("Proibido " + str(move))
			forbidden_moves.append(move)

	return forbidden_moves


def is_removal(board, player, moves):
	if(player == 1):
		for move in moves:
			if(board[move[0]][move[1]] != '2'):
				return False
	else:
		for move in moves:
			if(board[move[0]][move[1]] != '1'):
				return False
	return True


def get_available_moves(board):
	# print("AVAIL BOARD")
	# print(board)
	l = []

	for column in range(len(board)):
		for line in range(len(board[column])):
			if board[column][line] == '0':
				l.append((column, line))
	return l


def remove_unavailable_moves(board, moves):
	l = []
	for move in moves:
		if(board[move[0]][move[1]] == '0'):
			l.append(move)
			# print("APPEND")

	return l


def adapt_index(moves):
	new_moves = []
	for move in moves:
		new_move = [move[0]-1,move[1]-1]
		new_moves.append(new_move)

	return new_moves


def perform_move(board, move, player):
	# print(move)
	board[move[0]][move[1]] = str(player)

	return board

def parse_board_resp(bad_board):
	board = []
	for column in range(11):
		if column <= 5:
			height = 5 + column
		else:
			height = 15 - column
		board.append([0] * height)

	pieces_list = []

	for ele in bad_board:
		if(ele >= 48 and ele <= 50):
			pieces_list.append((chr(ele)))

	board[0] = pieces_list[0:5]
	board[1] = pieces_list[5:11]
	board[2] = pieces_list[11:18]
	board[3] = pieces_list[18:26]
	board[4] = pieces_list[26:35]
	board[5] = pieces_list[35:45]
	board[6] = pieces_list[45:54]
	board[7] = pieces_list[54:62]
	board[8] = pieces_list[62:69]
	board[9] = pieces_list[69:75]
	board[10] = pieces_list[75:80]

	return board

def list_to_string(char_list):
	new = ""
	# print(char_list)
	for c in char_list:
		new+= c
	return new

def calc_score(board, player):
	five_seq  = c.five_seq  * eval_five_seq(board, player)
	four_seq  = c.four_seq  * eval_four_seq(board, player)
	three_seq = c.three_seq * eval_three_seq(board, player)
	two_seq   = c.two_seq   * eval_two_seq(board, player)

	total_score = five_seq + four_seq + three_seq + two_seq

	return total_score


def print_occurrences():
	# Player 1
	print("Player 1")
	print("   TWO_SEQ            " + str(c.P1_OCCUR_TWO_SEQ))
	print("   THREE_SEQ          " + str(c.P1_OCCUR_THREE_SEQ))
	print("   FOUR_SEQ           " + str(c.P1_OCCUR_FOUR_SEQ))
	print("   FIVE_SEQ           " + str(c.P1_OCCUR_FIVE_SEQ))

	print("   BLOCK_TWO_SEQ      " + str(c.P1_OCCUR_BLOCK_TWO_SEQ))
	print("   BLOCK_THREE_SEQ    " + str(c.P1_OCCUR_BLOCK_THREE_SEQ))
	print("   BLOCK_FOUR_SEQ     " + str(c.P1_OCCUR_BLOCK_FOUR_SEQ))

	print("   BLOCK_THREE_EMPTY  " + str(c.P1_OCCUR_BLOCK_THREE_EMPTY))
	print("   BLOCK_FOUR_EMPTY   " + str(c.P1_OCCUR_BLOCK_FOUR_EMPTY))
	print("   BLOCK_FIVE_EMPTY   " + str(c.P1_OCCUR_BLOCK_FIVE_EMPTY))

	print("   MAKE_SANDWISH      " + str(c.P1_OCCUR_MAKE_SANDWISH))

	# Player 2
	print("Player 2")
	print("   TWO_SEQ            " + str(c.P2_OCCUR_TWO_SEQ))
	print("   THREE_SEQ          " + str(c.P2_OCCUR_THREE_SEQ))
	print("   FOUR_SEQ           " + str(c.P2_OCCUR_FOUR_SEQ))
	print("   FIVE_SEQ           " + str(c.P2_OCCUR_FIVE_SEQ))

	print("   BLOCK_TWO_SEQ      " + str(c.P2_OCCUR_BLOCK_TWO_SEQ))
	print("   BLOCK_THREE_SEQ    " + str(c.P2_OCCUR_BLOCK_THREE_SEQ))
	print("   BLOCK_FOUR_SEQ     " + str(c.P2_OCCUR_BLOCK_FOUR_SEQ))

	print("   BLOCK_THREE_EMPTY  " + str(c.P2_OCCUR_BLOCK_THREE_EMPTY))
	print("   BLOCK_FOUR_EMPTY   " + str(c.P2_OCCUR_BLOCK_FOUR_EMPTY))
	print("   BLOCK_FIVE_EMPTY   " + str(c.P2_OCCUR_BLOCK_FIVE_EMPTY))

	print("   MAKE_SANDWISH      " + str(c.P2_OCCUR_MAKE_SANDWISH))

def count_occurrences(board, player):


	c.P1_OCCUR_FIVE_SEQ  = eval_five_seq(board, 1)
	c.P1_OCCUR_FOUR_SEQ  = eval_four_seq(board, 1)
	c.P1_OCCUR_THREE_SEQ = eval_three_seq(board, 1)
	c.P1_OCCUR_TWO_SEQ   = eval_two_seq(board, 1)

	c.P1_OCCUR_BLOCK_TWO_SEQ   = eval_block_two_seq(board, 1)
	c.P1_OCCUR_BLOCK_THREE_SEQ = eval_block_three_seq(board, 1)
	c.P1_OCCUR_BLOCK_FOUR_SEQ  = eval_block_four_seq(board, 1)

	c.P1_OCCUR_BLOCK_THREE_EMPTY = eval_block_three_empty(board, 1)
	c.P1_OCCUR_BLOCK_FOUR_EMPTY  = eval_block_four_empty(board, 1)
	c.P1_OCCUR_BLOCK_FIVE_EMPTY  = eval_block_five_empty(board, 1)

	c.P1_OCCUR_MAKE_SANDWISH     = eval_make_sandwish(board, 1)

	c.P2_OCCUR_FIVE_SEQ  = eval_five_seq(board, 2)
	c.P2_OCCUR_FOUR_SEQ  = eval_four_seq(board, 2)
	c.P2_OCCUR_THREE_SEQ = eval_three_seq(board, 2)
	c.P2_OCCUR_TWO_SEQ   = eval_two_seq(board, 2)

	c.P2_OCCUR_BLOCK_TWO_SEQ   = eval_block_two_seq(board, 2)
	c.P2_OCCUR_BLOCK_THREE_SEQ = eval_block_three_seq(board, 2)
	c.P2_OCCUR_BLOCK_FOUR_SEQ  = eval_block_four_seq(board, 2)

	c.P2_OCCUR_BLOCK_THREE_EMPTY = eval_block_three_empty(board, 2)
	c.P2_OCCUR_BLOCK_FOUR_EMPTY  = eval_block_four_empty(board, 2)
	c.P2_OCCUR_BLOCK_FIVE_EMPTY  = eval_block_five_empty(board, 2)

	c.P2_OCCUR_MAKE_SANDWISH     = eval_make_sandwish(board, 1)


def calc_differential_score(board, player):
	five_seq_p1  = c.FIVE_SEQ  * eval_five_seq(board, 1)
	four_seq_p1  = c.FOUR_SEQ  * eval_four_seq(board, 1)
	three_seq_p1 = c.THREE_SEQ * eval_three_seq(board, 1)
	two_seq_p1   = c.TWO_SEQ   * eval_two_seq(board, 1)

	extra_empty_edges_two_p1 = c.EXTRA_EMPTY_EDGES_TWO   * eval_empty_edges_two(board, 1)
	extra_empty_edges_three_p1 = c.EXTRA_EMPTY_EDGES_TWO * eval_empty_edges_three(board, 1)
	extra_empty_edges_four_p1 = c.EXTRA_EMPTY_EDGES_TWO  * eval_empty_edges_four(board, 1)

	block_two_seq_p1   = c.BLOCK_TWO_SEQ   * eval_block_two_seq(board, 1)
	block_three_seq_p1 = c.BLOCK_THREE_SEQ * eval_block_three_seq(board, 1)
	block_four_seq_p1  = c.BLOCK_FOUR_SEQ  * eval_block_four_seq(board, 1)

	block_three_empty_p1 = c.BLOCK_THREE_EMPTY * eval_block_three_empty(board, 1)
	block_four_empty_p1  = c.BLOCK_FOUR_EMPTY * eval_block_four_empty(board, 1)
	block_five_empty_p1  = c.BLOCK_FIVE_EMPTY * eval_block_five_empty(board, 1)

	make_sandwish_p1	 = c.MAKE_SANDWISH * eval_make_sandwish(board, 1)


	total_score_p1 = 	five_seq_p1 + four_seq_p1 + three_seq_p1 + two_seq_p1 + extra_empty_edges_two_p1 + extra_empty_edges_three_p1 + extra_empty_edges_four_p1 +block_two_seq_p1 + block_three_seq_p1 + block_four_seq_p1 + block_three_empty_p1 + block_four_empty_p1 + block_five_empty_p1 + make_sandwish_p1
	# print("Score P1 " + str(total_score_p1))

	five_seq_p2  = c.FIVE_SEQ  * eval_five_seq(board, 2)
	four_seq_p2  = c.FOUR_SEQ  * eval_four_seq(board, 2)
	three_seq_p2 = c.THREE_SEQ * eval_three_seq(board, 2)
	two_seq_p2   = c.TWO_SEQ   * eval_two_seq(board, 2)

	extra_empty_edges_two_p2 = c.EXTRA_EMPTY_EDGES_TWO   * eval_empty_edges_two(board, 2)
	extra_empty_edges_three_p2 = c.EXTRA_EMPTY_EDGES_TWO * eval_empty_edges_three(board, 2)
	extra_empty_edges_four_p2 = c.EXTRA_EMPTY_EDGES_TWO  * eval_empty_edges_four(board, 2)

	block_two_seq_p2   = c.BLOCK_TWO_SEQ   * eval_block_two_seq(board, 2)
	block_three_seq_p2 = c.BLOCK_THREE_SEQ * eval_block_three_seq(board, 2)
	block_four_seq_p2  = c.BLOCK_FOUR_SEQ  * eval_block_four_seq(board, 2)

	block_three_empty_p2 = c.BLOCK_THREE_EMPTY * eval_block_three_empty(board, 2)
	block_four_empty_p2  = c.BLOCK_FOUR_EMPTY * eval_block_four_empty(board, 2)
	block_five_empty_p2  = c.BLOCK_FIVE_EMPTY * eval_block_five_empty(board, 2)

	make_sandwish_p2	 = c.MAKE_SANDWISH * eval_make_sandwish(board, 2)

	total_score_p2 = 	five_seq_p2 + four_seq_p2 + three_seq_p2 + two_seq_p2 + extra_empty_edges_two_p2 + extra_empty_edges_three_p2 + extra_empty_edges_four_p2 +block_two_seq_p2 + block_three_seq_p2 + block_four_seq_p2 + block_three_empty_p2 + block_four_empty_p2 + block_five_empty_p2 + make_sandwish_p2
	# print("Score P2 " + str(total_score_p2))

	differential_score = total_score_p1 - total_score_p2


	# print(board)
	# print("P1 " + str(total_score_p1) + "\t" + "P2 " + str(total_score_p2))
	# print(differential_score)
	# print()

	return differential_score


def calc_differential_score_parallel(board, player):
	p = Pool(2)

	result = p.starmap(calc_score, [(board,1), (board,2)])
	# print(result)
	differential_score = result[0] - result[1]

	return differential_score

def calc_score(board, player):
	if(player == 1):
		five_seq_p1  = c.FIVE_SEQ  * eval_five_seq(board, 1)
		four_seq_p1  = c.FOUR_SEQ  * eval_four_seq(board, 1)
		three_seq_p1 = c.THREE_SEQ * eval_three_seq(board, 1)
		two_seq_p1   = c.TWO_SEQ   * eval_two_seq(board, 1)

		block_two_seq_p1   = c.BLOCK_TWO_SEQ   * eval_block_two_seq(board, 1)
		block_three_seq_p1 = c.BLOCK_THREE_SEQ * eval_block_three_seq(board, 1)
		block_four_seq_p1  = c.BLOCK_FOUR_SEQ  * eval_block_four_seq(board, 1)

		block_three_empty_p1 = c.BLOCK_THREE_EMPTY * eval_block_three_empty(board, 1)
		block_four_empty_p1  = c.BLOCK_FOUR_EMPTY * eval_block_four_empty(board, 1)
		block_five_empty_p1  = c.BLOCK_FIVE_EMPTY * eval_block_five_empty(board, 1)

		total_score_p1 = five_seq_p1 + four_seq_p1 + three_seq_p1 + two_seq_p1 + block_two_seq_p1 + block_three_seq_p1 + block_four_seq_p1 + block_three_empty_p1 + block_four_empty_p1 + block_five_empty_p1
		
		return total_score_p1
	else:
		five_seq_p2  = c.FIVE_SEQ  * eval_five_seq(board, 2)
		four_seq_p2  = c.FOUR_SEQ  * eval_four_seq(board, 2)
		three_seq_p2 = c.THREE_SEQ * eval_three_seq(board, 2)
		two_seq_p2   = c.TWO_SEQ   * eval_two_seq(board, 2)

		block_two_seq_p2   = c.BLOCK_TWO_SEQ   * eval_block_two_seq(board, 2)
		block_three_seq_p2 = c.BLOCK_THREE_SEQ * eval_block_three_seq(board, 2)
		block_four_seq_p2  = c.BLOCK_FOUR_SEQ  * eval_block_four_seq(board, 2)

		block_three_empty_p2 = c.BLOCK_THREE_EMPTY * eval_block_three_empty(board, 2)
		block_four_empty_p2  = c.BLOCK_FOUR_EMPTY * eval_block_four_empty(board, 2)
		block_five_empty_p2  = c.BLOCK_FIVE_EMPTY * eval_block_five_empty(board, 2)

		total_score_p2 = five_seq_p2 + four_seq_p2 + three_seq_p2 + two_seq_p2 + block_two_seq_p2 + block_three_seq_p2 + block_four_seq_p2 + block_three_empty_p2 + block_four_empty_p2 + block_five_empty_p2
		
		return total_score_p2


# EXTRA SCORE: Player puts a piece forming
# a sequence of two AND both edges of the
# sequence are empty -> 0110
def eval_empty_edges_two(board, player):
	score = 0
	if(player == 1):
		pieces = "0110"
	else:
		pieces = "0220"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


# EXTRA SCORE: Player puts a piece forming
# a sequence of three AND both edges of the
# sequence are empty -> 01110
def eval_empty_edges_three(board, player):
	score = 0
	if(player == 1):
		pieces = "01110"
	else:
		pieces = "02220"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


# EXTRA SCORE: Player puts a piece forming
# a sequence of two AND both edges of the
# sequence are empty -> 0110
def eval_empty_edges_four(board, player):
	score = 0
	if(player == 1):
		pieces = "011110"
	else:
		pieces = "022220"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


# Player puts a piece in a position that makes
# a sandwish, i.e., removes an enemy piece
def eval_make_sandwish(board, player):
	score = 0

	if(player == 1):
		pieces = "1221"
	else:
		pieces = "2112"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


# Player puts a piece in a position that fills
# an empty space in a possible enemy sequence
def eval_block_three_empty(board, player):
	score = 0

	if(player == 1):
		pieces = "212"
	else:
		pieces = "121"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


# Player puts a piece in a position that fills
# an empty space in a possible enemy sequence
def eval_block_four_empty(board, player):
	score = 0

	if(player == 1):
		pieces1 = "2212"
		pieces2 = "2122"
	else:
		pieces1 = "1121"
		pieces2 = "1211"

	found_vertical_1 = find_vertical(board, pieces1)
	found_vertical_2 = find_vertical(board, pieces2)
	found_1_diag_1 = find_diagonal_primary(board, pieces1)
	found_1_diag_2 = find_diagonal_primary(board, pieces2)
	found_2_diag_1 = find_diagonal_secondary(board, pieces1)
	found_2_diag_2 = find_diagonal_secondary(board, pieces2)

	return (found_vertical_1 + found_vertical_2 + found_1_diag_1 + found_1_diag_2 + found_2_diag_1 + found_2_diag_2)


# Player puts a piece in a position that fills
# an empty space in a possible enemy sequence
def eval_block_five_empty(board, player):
	score = 0

	if(player == 1):
		pieces1 = "21222"
		pieces2 = "22212"
		pieces3 = "22122"
	else:
		pieces1 = "12111"
		pieces2 = "11121"
		pieces3 = "11211"

	found_vertical_1 = find_vertical(board, pieces1)
	found_vertical_2 = find_vertical(board, pieces2)
	found_vertical_3 = find_vertical(board, pieces3)
	found_1_diag_1 = find_diagonal_primary(board, pieces1)
	found_1_diag_2 = find_diagonal_primary(board, pieces2)
	found_1_diag_3 = find_diagonal_primary(board, pieces3)
	found_2_diag_1 = find_diagonal_secondary(board, pieces1)
	found_2_diag_2 = find_diagonal_secondary(board, pieces2)
	found_2_diag_3 = find_diagonal_secondary(board, pieces3)

	return (found_vertical_1 + found_vertical_2 + found_vertical_3 + found_1_diag_1 + found_1_diag_2 + found_1_diag_3 + found_2_diag_1 + found_2_diag_2 + found_2_diag_3)


# Player puts a piece in a position that blocks
# opponent sequence in a direction
def eval_block_two_seq(board, player):
	score = 0

	if(player == 1):
		pieces1 = "221"
		pieces2 = "122"
	else:
		pieces1 = "112"
		pieces2 = "211"

	found_vertical_1 = find_vertical(board, pieces1)
	found_vertical_2 = find_vertical(board, pieces2)
	found_1_diag_1 = find_diagonal_primary(board, pieces1)
	found_1_diag_2 = find_diagonal_primary(board, pieces2)
	found_2_diag_1 = find_diagonal_secondary(board, pieces1)
	found_2_diag_2 = find_diagonal_secondary(board, pieces2)

	return (found_vertical_1 + found_vertical_2 + found_1_diag_1 + found_1_diag_2 + found_2_diag_1 + found_2_diag_2)


# Player puts a piece in a position that blocks
# opponent sequence in a direction
def eval_block_three_seq(board, player):
	score = 0

	if(player == 1):
		pieces1 = "2221"
		pieces2 = "1222"
	else:
		pieces1 = "1112"
		pieces2 = "2111"

	found_vertical_1 = find_vertical(board, pieces1)
	found_vertical_2 = find_vertical(board, pieces2)
	found_1_diag_1 = find_diagonal_primary(board, pieces1)
	found_1_diag_2 = find_diagonal_primary(board, pieces2)
	found_2_diag_1 = find_diagonal_secondary(board, pieces1)
	found_2_diag_2 = find_diagonal_secondary(board, pieces2)

	return (found_vertical_1 + found_vertical_2 + found_1_diag_1 + found_1_diag_2 + found_2_diag_1 + found_2_diag_2)


# Player puts a piece in a position that blocks
# opponent sequence in a direction
def eval_block_four_seq(board, player):
	score = 0

	if(player == 1):
		pieces1 = "22221"
		pieces2 = "12222"
	else:
		pieces1 = "11112"
		pieces2 = "21111"

	found_vertical_1 = find_vertical(board, pieces1)
	found_vertical_2 = find_vertical(board, pieces2)
	found_1_diag_1 = find_diagonal_primary(board, pieces1)
	found_1_diag_2 = find_diagonal_primary(board, pieces2)
	found_2_diag_1 = find_diagonal_secondary(board, pieces1)
	found_2_diag_2 = find_diagonal_secondary(board, pieces2)

	return (found_vertical_1 + found_vertical_2 + found_1_diag_1 + found_1_diag_2 + found_2_diag_1 + found_2_diag_2)


def eval_five_seq(board, player):
	score = 0
	if(player == 1):
		pieces = "11111"
	else:
		pieces = "22222"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


def eval_four_seq(board, player):
	score = 0
	if(player == 1):
		pieces = "1111"
	else:
		pieces = "2222"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


def eval_three_seq(board, player):
	score = 0
	if(player == 1):
		pieces = "111"
	else:
		pieces = "222"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


def eval_two_seq(board, player):
	score = 0
	if(player == 1):
		pieces = "11"
	else:
		pieces = "22"

	found_vertical = find_vertical(board, pieces)
	found_1_diag = find_diagonal_primary(board, pieces)
	found_2_diag = find_diagonal_secondary(board, pieces)

	return (found_vertical + found_1_diag + found_2_diag)


def find_vertical(board, pieces):
	found = 0
	for board_column in board:
		column = list_to_string(board_column)
		# print(column)
		a = column.count(pieces)
		if(a > 0):
			found += a

	return found


def find_diagonal_primary(board, pieces):
	found = 0

	# evaluate all primary diags
	for diag in c.primary_diags:
		#print(diag)
		diag_pieces = []
		
		# generate list with pieces in current diagonal, and converts to string
		for position in diag:
			diag_pieces.append(board[position[0]][position[1]])
		diag_pieces = list_to_string(diag_pieces)
		# print(diag_pieces)
		a = diag_pieces.count(pieces)
		if(a > 0):
			found += a
		
	return found


def find_diagonal_secondary(board, pieces):
	found = 0

	# evaluate all secondary diags
	for diag in c.secondary_diags:
		#print(diag)
		diag_pieces = []
		
		# generate list with pieces in current diagonal, and converts to string

		for position in diag:
			diag_pieces.append(board[position[0]][position[1]])
		diag_pieces = list_to_string(diag_pieces)
		# print(diag_pieces)
		a = diag_pieces.count(pieces)
		if(a > 0):
			found += a

	return found