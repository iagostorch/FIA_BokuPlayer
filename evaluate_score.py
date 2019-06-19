import urllib.request
import sys
import random
import time
import json 
import re
import utils
import c
import copy
import node
import datetime

forbidden_moves = []
identifier = 0
start = 0.0
end = 0.0


# PLAYER 1 -> MAXIMIZA
# PLAYER 2 -> MINIMIZA

def choose_move(board, player):
	global forbidden_moves

	print("PLAYER " + str(player) + "\n")
	if(player == 1):	# last_player is opposite of current player
		root = node.Node(-1,board,0,2,0)
	else:
		root = node.Node(-1,board,0,1,0)

	resp = urllib.request.urlopen("%s/movimentos" % host)
	server_moves = eval(resp.read())
	server_moves = utils.adapt_index(server_moves)

	forbidden_moves = utils.get_forbidden_moves(board, server_moves)

	# print("FORBIDDEN MOVES")
	# print(server_moves)

	if(len(forbidden_moves) > 0):
		print("FORBIDDEN MOVES")
		print(forbidden_moves)
		print()

	# print("INITIAL BOARD")
	# print(board)
	# print()

	#	If the returned moves characterize positions
	#	in which there are enemy pieces, then we must
	#	remove one enemy piece
	if(utils.is_removal(board, player, server_moves)):
		print("REMOVE PIECE -- RANDOM")
		return random.choice(server_moves)

	else:
		print("iNSERT PIECE")
		pontos = minimax_alphabeta(root, player)
		print("pontos " + str(pontos))

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
	print("DO ONE OF THESE -- STARTING INDEX ZERO")
	print(move_array)
	print()
	return random.choice(move_array)


def minimax_alphabeta(curr_node, player, alpha, beta):
	# end = datetime.datetime.now()
	# diff = end - start
	# print(diff)
	# print(curr_node.get_board())
	global identifier
	global forbidden_moves
	score_list = []
	identifier += 1
	
	if(curr_node.get_depth() >= c.max_depth):	# if we hit max depth, recursion is stopped
		score = utils.calc_differential_score(curr_node.get_board(), player)
		curr_node.set_score(score)
		return score
	elif(curr_node.is_final()):					# if current state is final, recursion is stopped
		score = utils.calc_differential_score(curr_node.get_board(), player)
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
		

if len(sys.argv)==1:
	print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:	./random_client.py 1")
	quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

# start = datetime.datetime.now()

done = False
while not done:
	# Pergunta quem eh o jogador
	resp = urllib.request.urlopen("%s/jogador" % host)
	player_turn = int(resp.read())

	# Se jogador == 0, o jogo acabou e o cliente perdeu
	if player_turn==0:
		print("I lose.")
		done = True

	# Se for a vez do jogador
	if player_turn==player:
		
		start = datetime.datetime.now()
		
		# Pega o tabuleiro do servidor e altera a estrutura de dados para a execucao do algoritmo
		resp = urllib.request.urlopen("%s/tabuleiro" % host)
		data = resp.read()
		# print(data)
		board = utils.parse_board_resp(data)
		
		score = utils.calc_differential_score(board, player)
		print("Score " + str(score))
		
		# Tempo transcorrido durate a execucao
		end = datetime.datetime.now()
		diff = end - start
		print("Tempo H:M:S\t" + str(diff))



		# Se com o movimento o jogo acabou, o cliente venceu
		if msg[0]==0:
			print("I win")
			done = True
		if msg[0]<0:
			raise Exception(msg[1])
	
	# Descansa um pouco para nao inundar o servidor com requisicoes
	time.sleep(1)




