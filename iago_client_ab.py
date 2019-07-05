# TODO:		improve the performance of method to
#			verify if we are removing or inserting
#			a piece. Evaluate lenght of move_list

#TODO:		should we consider a tie condition?

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
from multiprocessing import Process, Manager
import time

forbidden_moves = []
identifier = 0
start = 0.0
end = 0.0
in_time = True

# PLAYER 1 -> MAXIMIZE
# PLAYER 2 -> MINIMIZE

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

	# Series of strategic moves to perform at the beginning of match
	if player == 1:
		if len(server_moves) >= 76:
			if [3,4] in server_moves:
				move_list.append([3,4])
				# print("FAST DECISION")
				return
			if [5,4] in server_moves:
				move_list.append([5,4])
				# print("FAST DECISION")
				return
			if [5,6] in server_moves:
				move_list.append([5,6])
				# print("FAST DECISION")
				return
			if [7,4] in server_moves:
				move_list.append([7,4])
				# print("FAST DECISION")
				return
	elif player == 2:
		if len(server_moves) >= 77:
			if [5,4] in server_moves:
				move_list.append([5,4])
				# print("FAST DECISION")
				return
			if [5,5] in server_moves:
				move_list.append([5,5])
				# print("FAST DECISION")
				return
			if [5,3] in server_moves:
				move_list.append([5,3])
				# print("FAST DECISION")
				return
			if [5,6] in server_moves:
				move_list.append([5,6])
				# print("FAST DECISION")
				return


	if(len(forbidden_moves) > 0):
		print("FORBIDDEN MOVES")
		print(forbidden_moves)
		print()


	#	If the returned moves characterize positions
	#	in which there are enemy pieces, then we must
	#	remove one enemy piece
	if(utils.is_removal(board, player, server_moves)):
		print("REMOVE PIECE")
		ab = [-9999999999, 9999999999]
		score = heuristic_remove(root, player, ab)
	else:
		print("iNSERT PIECE")
		# score_old = minimax_place(root, player)
		alpha = -9999999999
		beta  = 9999999999
		ab = [alpha, beta]
		score = minimax_alphabeta(root, player, ab)

		print("score " + str(score))

	nodes = [root]

	children = root.get_lowers()
	max_score = children[0].get_score()
	move = children[0].get_move()

	max_score_array = [max_score]
	move_array = [move]
	best_children_array = [children[0]]


	for child in children:
		if(player == 1): # maximiza
			# If current score is greater than max, score is new max
			# If current score equals max, current is added to max list
			if(child.get_score() > max_score_array[0]):
				max_score_array = [child.get_score()]
				move_array = [child.get_move()]
				best_children_array = [child]
			elif(child.get_score() == max_score_array[0]):
				max_score_array.append(child.get_score())
				move_array.append(child.get_move())
				best_children_array.append(child)
		else: # minimiza
			if(child.get_score() < max_score_array[0]):
				max_score_array = [child.get_score()]
				move_array = [child.get_move()]
			elif(child.get_score() == max_score_array[0]):
				max_score_array.append(child.get_score())
				move_array.append(child.get_move())
	print("DO ONE OF THESE -- STARTING INDEX ZERO")
	print(move_array)
	a = copy.copy(move_array)
	print()

	chosen = random.choice(a)
	print(chosen)
	move_list.append(chosen)



def minimax_alphabeta(curr_node, player, ab):

	global identifier
	global forbidden_moves
	score_list = []
	identifier += 1	
	
	alpha = ab[0]
	beta = ab[1]
	
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
		moves = utils.remove_forbidden_moves(moves, forbidden_moves)
	
	if(player == 1):	
		value = -9999999999
		for move in moves:
			new_board = utils.perform_move(copy.deepcopy(curr_node.get_board()), move, player)
			new_node = node.Node(curr_node, new_board, curr_node.get_depth() + 1, player, move)
			new_node.set_identifier(identifier)

			curr_node.add_lower(new_node)

			move_score = minimax_alphabeta(new_node, 2, ab)

			value = max(move_score, value)

			ab[0] = max(alpha, value)
			if(ab[0] >= beta):
				break

		curr_node.set_score(value)
		return value		
	else:
		value = 9999999999
		for move in moves:
			new_board = utils.perform_move(copy.deepcopy(curr_node.get_board()), move, player)
			new_node = node.Node(curr_node, new_board, curr_node.get_depth() + 1, player, move)
			new_node.set_identifier(identifier)

			curr_node.add_lower(new_node)

			move_score = minimax_alphabeta(new_node, 1, ab)

			value = min(move_score, value)

			ab[1] = min(beta, value)
			if(alpha >= ab[1]):
				break

		curr_node.set_score(value)
		return value						



def heuristic_remove(curr_node, player, ab):

	global identifier
	global forbidden_moves
	score_list = []
	identifier += 1	

	if(curr_node.get_depth() >= c.removal_max_depth):	# if we hit max depth, recursion is stopped
		score = utils.calc_differential_score(curr_node.get_board(), player)
		curr_node.set_score(score)
		return score
	elif(curr_node.is_final()):					# if current state is final, recursion is stopped
		score = utils.calc_differential_score(curr_node.get_board(), player)
		curr_node.set_score(score)
		print("FINAL STATE REMOVE")
		return score

	resp = urllib.request.urlopen("%s/movimentos" % host)
	server_moves = eval(resp.read())
	server_moves = utils.adapt_index(server_moves)
	moves = server_moves
					

	if(player == 1):
		
		value = -9999999999
		for move in moves:
			new_board = utils.perform_move(copy.deepcopy(curr_node.get_board()), move, 0)
			new_node = node.Node(curr_node, new_board, curr_node.get_depth() + 1, player, move)
			new_node.set_identifier(identifier)

			curr_node.add_lower(new_node)

			move_score = heuristic_remove(new_node, player, ab)

			value = max(move_score, value)

			ab[0] = max(ab[0], value)

		curr_node.set_score(value)
		return value		
	else:
		value = 9999999999
		for move in moves:
			new_board = utils.perform_move(copy.deepcopy(curr_node.get_board()), move, 0)
			new_node = node.Node(curr_node, new_board, curr_node.get_depth() + 1, player, move)
			new_node.set_identifier(identifier)

			curr_node.add_lower(new_node)

			move_score = heuristic_remove(new_node, player, ab)

			value = min(move_score, value)

			ab[1] = min(ab[1], value)

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

done = False
while not done:
	# Pergunta quem eh o jogador
	resp = urllib.request.urlopen("%s/jogador" % host)
	player_turn = int(resp.read())

	# Se jogador == 0, o jogo acabou e o cliente perdeu
	if player_turn==0:
		print("I lose.")

		resp = urllib.request.urlopen("%s/tabuleiro" % host)
		data = resp.read()
		board = utils.parse_board_resp(data)

		utils.count_occurrences(board, player)
		utils.print_occurrences()
		
		done = True

	# Se for a vez do jogador
	if player_turn==player:
		
		start = datetime.datetime.now()
		in_time = True
		# Fetch moves from server in case a random choice must be made
		resp = urllib.request.urlopen("%s/movimentos" % host)
		backup_moves = eval(resp.read())

		# Fetch board from server and adjusts the data structure to algorithm execution
		resp = urllib.request.urlopen("%s/tabuleiro" % host)
		data = resp.read()
		# print(data)
		board = utils.parse_board_resp(data)
		
		# # Algorithm to define which move should be performed
		# move = choose_move(board, player)
		with Manager() as manager:
			move_list = manager.list()
			p = Process(target=choose_move, name="Choose_Move", args=(board, player,))
			p.start()

			p.join(c.max_time)
			if p.is_alive():
				print("TIMEOUT -- Selecting random move")
				in_time = False
				p.terminate()
				p.join()

			if in_time:		
				# Sum 1 to the move coordinates because the server starts indexing with 1 instead of 0
				# print(move)
				print("move_list")
				print(move_list)
				corrected_move = list(move_list[0])
				corrected_move[0] += 1
				corrected_move[1] += 1
				corrected_move = tuple(corrected_move)
		#		print("Corrected move " + str(corrected_move))
				move = corrected_move
			else:
				print("RANDOMIZE")
				move = random.choice(backup_moves)
			print(move)
			# Execution time of algorithm
			end = datetime.datetime.now()
			diff = end - start
			print("Time H:M:S\t" + str(diff))
			print(move)
			# Perform the move
			resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,move[0],move[1]))
			msg = eval(resp.read())


			# Se com o movimento o jogo acabou, o cliente venceu
			if msg[0]==0:
				print("I win")
				
				resp = urllib.request.urlopen("%s/tabuleiro" % host)
				data = resp.read()
				board = utils.parse_board_resp(data)
				
				utils.count_occurrences(board, player)
				utils.print_occurrences()

				done = True
			if msg[0]<0:
				raise Exception(msg[1])
	
	# Descansa um pouco para nao inundar o servidor com requisicoes
	time.sleep(1)




