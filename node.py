#from math import inf as infinity
import numpy as np
import utils

class Node():
	def __init__(self, upper, board, depth, last_player, move):
		self.upper = upper
		self.board = board
		self.depth = depth
		self.last_player = last_player
		self.lowers = []
		self.score = -2
		self.move = move
		self.evaluated = 0
		self.identifier = 0
		# print('tipo ' + str(move[0]))

	def is_final(self):
		score1 = utils.eval_five_seq(self.board, 1)
		score2 = utils.eval_five_seq(self.board, 2)

		if(score1 > 0 or score2 > 0):
			return True
		else:
			return False


	def get_identifier(self):
		return self.identifier

	def set_identifier(self, identifier):
		self.identifier = identifier

	def get_upper(self):
		return self.upper

	def get_board(self):
		return self.board

	def get_last_player(self):
		return self.last_player

	def add_lower(self, lower):
		self.lowers.append(lower)

	def get_lowers(self):
		return self.lowers

	def get_depth(self):
		return self.depth

	def print_board(self):
		print(self.board)

	def set_score(self, score):
		self.score = score

	def get_score(self):
		return self.score

	def get_move(self):
		return self.move

	def set_move(self, move):
		self.move = move

	def is_evaluated(self):
		return self.evaluated

	def set_evaluated(self):
		self.evaluated = 1