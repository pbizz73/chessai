import pygame
import queue
from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn
from data.classes.Piece import Piece
import random
import numpy



# Game state checker
class Board:
	#delete if not used
	def __init__(self, width=600, height=600, board=None, fen=None):
		#if you want to create a board with fen, need to update state of pieces from fen,
		#castling rights has or has not moved and such. 
		if board != None:
			self.height = board.height
			self.width = board.width
			self.tile_width = board.width // 8
			self.tile_height = board.height // 8
			self.selected_piece = board.selected_piece
			if fen == None:
				self.turn = board.turn
				self.epsquare = board.epsquare
				self.halfmovenumber = board.halfmovenumber
				self.fullmovenumber = board.fullmovenumber
				self.squares = self.generate_squares(board)
			else:
				#organize fen string
				self.squares = self.generate_squares()
				split_fen = fen.split('/', 8)
				endingstring = split_fen[len(split_fen)-1]
				split_endingstring = endingstring.split(' ')
				del split_fen[-1]
				for token in split_endingstring:
					split_fen.append(token)
				#set turn
				if split_fen[8] == 'b':
					self.turn = "black"
				else:
					self.turn = 'white'
				self.config = self.fen2config(fen)
				#set epsquare
				self.epsquare = split_fen[10]
				#set halfmove/fullmove
				self.halfmovenumber = int(split_fen[11])
				self.fullmovenumber = int(split_fen[12])
				self.setup_board(fen=split_fen)

		else:
			self.width = width
			self.height = height
			self.tile_width = width // 8
			self.tile_height = height // 8
			self.selected_piece = None
			self.turn = 'white'
			self.epsquare = ""
			self.halfmovenumber = 0
			self.fullmovenumber = 0

		# try making it chess.board.fen()
			self.config = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
			]

			self.squares = self.generate_squares()

			self.setup_board()
	
	def generate_squares(self, board=None):
		output = []
		if board == None:
			for y in range(8):
				for x in range(8):
					output.append(
						Square(x,  y, self.tile_width, self.tile_height)
					)
			return output
		else:
			for square in board.squares:
				new_square = Square(square.x,square.y, self.tile_width, self.tile_height )
				if square.occupying_piece != None:
					if square.occupying_piece.notation == "P":
						new_piece = Pawn(square.occupying_piece.pos,square.occupying_piece.color, self)
						self.assign_square(new_piece,square.occupying_piece)
						new_square.occupying_piece = new_piece
					if square.occupying_piece.notation == "R":
						new_piece = Rook(square.occupying_piece.pos,square.occupying_piece.color, self)
						self.assign_square(new_piece,square.occupying_piece)
						new_square.occupying_piece = new_piece
					if square.occupying_piece.notation == "Q":
						new_piece = Queen(square.occupying_piece.pos,square.occupying_piece.color, self)
						self.assign_square(new_piece,square.occupying_piece)
						new_square.occupying_piece = new_piece
					if square.occupying_piece.notation == "K":
						new_piece = King(square.occupying_piece.pos,square.occupying_piece.color, self)
						self.assign_square(new_piece,square.occupying_piece)
						new_square.occupying_piece = new_piece
					if square.occupying_piece.notation == "B":
						new_piece = Bishop(square.occupying_piece.pos,square.occupying_piece.color, self)
						self.assign_square(new_piece,square.occupying_piece)
						new_square.occupying_piece = new_piece
					if square.occupying_piece.notation == "N":
						new_piece = Knight(square.occupying_piece.pos,square.occupying_piece.color, self)
						self.assign_square(new_piece,square.occupying_piece)
						new_square.occupying_piece = new_piece
				output.append(new_square)

			return output
		

	def assign_square(self,new_piece, old_piece):
		new_piece.has_moved = old_piece.has_moved
		new_piece.cancastleKingside = old_piece.cancastleKingside
		new_piece.cancastleQueenside = old_piece.cancastleQueenside
		new_piece.blocking_square =old_piece.blocking_square

	def get_square_from_pos(self, pos):
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square


	def get_piece_from_pos(self, pos):
		return self.get_square_from_pos(pos).occupying_piece

	def fen2config(self, fen):
		config = []
		split_fen = fen.split('/', 8)
		endingstring = split_fen[len(split_fen)-1]
		split_endingstring = endingstring.split(' ')
		del split_fen[-1]
		for token in split_endingstring:
			split_fen.append(token)

		
		for str in split_fen[:8]:
			row = []
			row_indvidual_list = list(str)
			for char in row_indvidual_list:
				if char.isdigit():
					numOfEmptySquares=int(char)
					for space in range(numOfEmptySquares):
						row.append('')
				else:
					if char.isupper():
						row.append('w'+char)
					else:
						row.append('b'+ char)
			config.append(row)



		return config
		
		
	def setup_board(self, fen = None):
		# iterating 2d list
		#need to update castling from fen string and whether pawns have moved
		for y, row in enumerate(self.config):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.get_square_from_pos((x, y))

					# looking inside contents, what piece does it have
					if piece[1].capitalize() == 'R':
						square.occupying_piece = Rook(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					# as you notice above, we put `self` as argument, or means our class Board

					elif piece[1].capitalize()== 'N':
						square.occupying_piece = Knight(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1].capitalize() == 'B':
						square.occupying_piece = Bishop(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1].capitalize() == 'Q':
						square.occupying_piece = Queen(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1].capitalize()== 'K':
						square.occupying_piece = King(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
						
						if fen != None:
							castling_rights_list= list(fen[9])
							if castling_rights_list[0] == '-':
								square.occupying_piece.cancastleKingside = False
								square.occupying_piece.cancastleQueenside = False
								square.occupying_piece.has_moved = True
							if square.occupying_piece.color == "white":
								if 'K' in castling_rights_list:
									square.occupying_piece.cancastleKingside = True
								if 'Q' in castling_rights_list:
									square.occupying_piece.cancastleQueenside = True
							else:
								if 'k' in castling_rights_list:
									square.occupying_piece.cancastleKingside = True
								if 'q' in castling_rights_list:
									square.occupying_piece.cancastleQueenside = True
	
					elif piece[1].capitalize() == 'P':
						square.occupying_piece = Pawn(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
						if fen != None:
							if square.occupying_piece.color == 'white' and square.occupying_piece.y != 6:
								square.occupying_piece.has_moved = True
							if square.occupying_piece.color == 'black' and square.occupying_piece.y != 1:
								square.occupying_piece.has_moved = True



	# def handle_click(self, mx, my):
	# 	x = mx // self.tile_width
	# 	y = my // self.tile_height
	# 	clicked_square = self.get_square_from_pos((x, y))
	# 	if self.turn == 'black':
	# 		self.selected_piece = self.generate_random_piece()
	# 		while(not self.selected_piece.move(self, clicked_square)):
	# 			self.selected_piece = self.generate_random_piece()
	# 		self.turn = 'white' if self.turn == 'black' else 'black'		
		
	# 	if self.selected_piece is None:
	# 		if clicked_square.occupying_piece is not None:
	# 			if clicked_square.occupying_piece.color == self.turn:
	# 				self.selected_piece = clicked_square.occupying_piece

	# 	elif self.selected_piece.move(self, clicked_square) and self.turn == 'white':
	# 		self.turn = 'white' if self.turn == 'black' else 'black'

	# 	elif clicked_square.occupying_piece is not None:
	# 		if clicked_square.occupying_piece.color == self.turn:
	# 			self.selected_piece = clicked_square.occupying_piece

	def handle_click(self, mx, my, bot = None):
		x = mx // self.tile_width
		y = my // self.tile_height
		clicked_square = self.get_square_from_pos((x, y))
		if self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece
		
		elif self.selected_piece.move(self, clicked_square):
			self.turn = 'white' if self.turn == 'black' else 'black'

		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == self.turn:
				self.selected_piece = clicked_square.occupying_piece


	
	def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
		output = False
		king_pos = None
		attacking_squares = []
		shortest_attack_path_squares = []
		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.occupying_piece
					old_square = square
					old_square.occupying_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.occupying_piece
					new_square.occupying_piece = changing_piece

		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K' and piece.color == color:
						king_pos = piece.pos
		#check for surronding squares that are empty 
		#then see if sqaure.pos is = the surronding squares

		king_pos_x = king_pos[0]
		king_pos_y = king_pos[1]
		surronding_king_squares = []
		for pos_x in range(king_pos_x-1, king_pos_x+2):
			for pos_y in range(king_pos_y-1, king_pos_y +2):
				if (
				pos_x < 8 and
				pos_x >= 0 and 
				pos_y< 8 and 
				pos_y >= 0
				):
					new_pos = [pos_x, pos_y]
					if (pos_x != king_pos_x) or (pos_y != king_pos_y):
						surronding_king_squares.append(self.get_square_from_pos(new_pos))		
						
		for piece in pieces:
			if piece.color != color:
				for square in piece.attacking_squares(self):
					if square.pos == king_pos:
						attacking_piece = piece
						attacking_squares = piece.attacking_squares(self)
						output = True

#Checking for blocking piece code		
		for attacking_square in attacking_squares:
			#shortest attacking square only used for blocking and cant block horse attack
			if attacking_piece.notation != 'N':
				diry = numpy.sign(king_pos_y-attacking_piece.y)
				dirx = numpy.sign(king_pos_x-attacking_piece.x)
				if attacking_square.x == king_pos_x:
					for pos_y in range(attacking_piece.y, king_pos_y+diry,diry if diry != 0 else 1 ):
						pos = [king_pos_x, pos_y]
						if self.get_square_from_pos(pos) in attacking_squares:
							shortest_attack_path_squares.append( self.get_square_from_pos(pos))
					#makes sure king is in shortest path
					if self.get_square_from_pos(king_pos) in shortest_attack_path_squares:
						break
					else:
						shortest_attack_path_squares = []				
				elif attacking_square.y == king_pos_y:
					
					for pos_x in range(attacking_piece.x, king_pos_x + dirx, dirx if dirx != 0 else 1):
						pos = [pos_x, king_pos_y]
						if self.get_square_from_pos(pos) in attacking_squares:
							shortest_attack_path_squares.append(self.get_square_from_pos(pos))
					#makes sure king is in shortest path
					if self.get_square_from_pos(king_pos) in shortest_attack_path_squares:
						break
					else:
						shortest_attack_path_squares = []	
					break
				elif abs(king_pos_x - attacking_piece.x) == abs(king_pos_y - attacking_piece.y):
					for pos_x in range(attacking_piece.x, king_pos_x + dirx, dirx if dirx != 0 else 1 ):
						for pos_y in range(attacking_piece.y, king_pos_y+ +diry,diry if diry != 0 else 1):
							if abs(king_pos_x - pos_x) == abs(king_pos_y-pos_y):
								pos = [pos_x, pos_y]
								if self.get_square_from_pos(pos) in attacking_squares:
									shortest_attack_path_squares.append(self.get_square_from_pos(pos))
						#makes sure king is in shortest path
					if self.get_square_from_pos(king_pos) in shortest_attack_path_squares:
						break
					else:
						shortest_attack_path_squares = []	
			# else:
			# 	if attacking_square.pos == king_pos:
			# 		shortest_attack_path_squares.append(attacking_square)
					

			#get blocking piece

		for blocking_piece in pieces:
			if blocking_piece.color == color and blocking_piece.notation != 'K':
				for blocking_square in blocking_piece.attacking_squares(self):
					if blocking_square in shortest_attack_path_squares:
						blocking_piece.blocking_square.append(blocking_square)

		if board_change is not None:
			old_square.occupying_piece = changing_piece
			new_square.occupying_piece = new_square_old_piece
						
		return output


	def is_in_checkmate(self, color):
		output = False

		for piece in [i.occupying_piece for i in self.squares]:
			if piece != None:
				if piece.notation == 'K' and piece.color == color:
					king = piece
		if king.get_valid_moves(self) == []:
			if self.is_in_check(color):
				output = True

		for piece in [i.occupying_piece for i in self.squares]:
			if piece != None:
				if len(piece.blocking_square)>0 :
					output = False

		return output


	def draw(self, display):
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)

	def generate_random_piece(self):
		availableSquares = []
		for square in self.squares:
			if  square.occupying_piece != None and square.occupying_piece.color == 'black':
				availableSquares.append(square)
		randomSquare = random.randint(0,len(availableSquares)-1)
		return availableSquares[randomSquare].occupying_piece
	

	def generate_fen(self):


		row = queue.Queue()
		num = []
		row_num = 0
		fen = ""
		castlerights =""
		epsquare = ""
		for square in self.squares:
			row_num += 1
			if square.occupying_piece != None and square.occupying_piece.color == 'black':
				while len(num) != 0:
					row.put(str(num.pop()))
				row.put(square.occupying_piece.notation.lower())
				if square.occupying_piece.notation == 'K':
					castlerights = castlerights+self.castlerightsfen(square).lower()
			elif square.occupying_piece != None and square.occupying_piece.color == 'white':
				while len(num) != 0:
					row.put(str(num.pop()))
				row.put(square.occupying_piece.notation)
				if square.occupying_piece.notation == 'K':
					castlerights = self.castlerightsfen(square)+castlerights
			else:
				if len(num) != 0:
					num.append(num.pop()+1)
				else:
					num.append(1)
			if row_num %8 == 0:
				if len(num) != 0:
					row.put(str(num.pop()))
				while not row.empty() :
					fen = fen + row.get()
				num = []
				if row_num <64:
					fen = fen + "/"
		#turn
		if self.turn == "black":
			fen = fen + " b"
		else: 
			fen = fen + " w"
		#castlerights
		if castlerights == "":
			fen = fen + " -"
		else:
			fen = fen + " "+castlerights
		#ep_square
		if self.epsquare == "":
			fen = fen + " -"
		else:
			fen = fen  +" " +self.epsquare 
		#halfmove and fullmove
		fen = fen + " "+ str(self.halfmovenumber)+ " " + str(self.fullmovenumber)
	

		return fen
	

	#change this for new function
	def castlerightsfen(self, square):
		castlerights = ""
		if square.occupying_piece.cancastleQueenside == True:
			castlerights = castlerights + "Q"
		if square.occupying_piece.cancastleKingside == True:
			castlerights = "K" + castlerights
		if castlerights == "":
			return ""
		else:
			return castlerights
	def generate_moves(self, color):
		all_moves= [] 
		for square in self.squares:
			if square.occupying_piece != None and square.occupying_piece.color == color:
				for move2square in square.occupying_piece.get_valid_moves(self):
					all_moves.append((square ,move2square))
		return all_moves



			

		
	