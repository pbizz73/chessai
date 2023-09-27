import pygame
import random
from data.classes import Square


class Piece:
	def __init__(self, pos, color, board):
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		self.color = color
		self.has_moved = False
		self.cancastleKingside = True
		self.cancastleQueenside = True
		self.blocking_square = []
		



	def move(self, board, square, force=False):
		board.fullmovenumber +=1
		for i in board.squares:
			i.highlight = False
		# if board.turn == 'black':
		# 	square = self.generate_random_move(board)

		if square in self.get_valid_moves(board) or force:
			board.halfmovenumber += 1
			prev_square = board.get_square_from_pos(self.pos)
			#halfmove
			if square.occupying_piece != None or prev_square.occupying_piece.notation == 'P':
				board.halfmovenumber = 0

			self.pos, self.x, self.y = square.pos, square.x, square.y
			prev_square.occupying_piece = None
			square.occupying_piece = self
			board.selected_piece = None
			#clear blocking pieces 
			for piece in [i.occupying_piece for i in board.squares]:
				if piece != None:
					piece.blocking_square = []
					if piece.notation == "K":
						king = piece
						king.can_castle(board)
			#reset epsqure
			tempboardep = board.epsquare
			board.epsquare = ""
			#check caslting rights
			



			# Pawn promotion
			if self.notation == 'P':
				if self.y == 0 or self.y == 7:
					from data.classes.pieces.Queen import Queen
					square.occupying_piece = Queen(
						(self.x, self.y),
						self.color,
						board
					)

			# Move rook if king castles
			if self.notation == 'K':
				#Queenside Castle
				if prev_square.x - self.x == 2:
					rook = board.get_piece_from_pos((0, self.y))
					rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
					
				elif prev_square.x - self.x == -2:
					rook = board.get_piece_from_pos((7, self.y))
					rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
			#find en_passsant square
			if self.notation =='P':
				if not self.has_moved and abs(prev_square.y - square.y) == 2 and self.color == 'white':
					board.epsquare = Square.Square(prev_square.x,prev_square.y-1,board.tile_width,board.tile_height).get_coord()
				if not self.has_moved and abs(prev_square.y - square.y) == 2 and self.color == 'black':
					board.epsquare = Square.Square(prev_square.x,prev_square.y+1,board.tile_width,board.tile_height).get_coord()
				if tempboardep == square.get_coord() and self.color == 'white':
					x = square.occupying_piece.x
					y = square.occupying_piece.y +1
					pos = [x,y]
					board.get_square_from_pos(pos).occupying_piece = None
				if tempboardep == square.get_coord() and self.color == 'black':
					x = square.occupying_piece.x
					y = square.occupying_piece.y -1
					pos = [x,y]
					board.get_square_from_pos(pos).occupying_piece = None
			
			self.has_moved = True
			 

			return True
		else:
			board.selected_piece = None
			return False


	def get_moves(self, board):
		output = []
		for direction in self.get_possible_moves(board):
			for square in direction:
				if square.occupying_piece is not None:
					if square.occupying_piece.color == self.color:
						break
					else:
						output.append(square)
						break
				else:
					output.append(square)
		return output


	def get_valid_moves(self, board):
		output = []
		for square in self.get_moves(board):
			if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
				output.append(square)
				#change
		while len(self.blocking_square)>0:
				output.append(self.blocking_square.pop())

		return output
	
	def generate_random_move(self,board):
		#need to send a square
		validMoves = self.get_valid_moves(board)
		if len(validMoves) == 0:
			return  None
		else:
			randomMove = random.randint(0,len(validMoves)-1)
			return validMoves[randomMove]



	# True for all pieces except pawn
	def attacking_squares(self, board):
		return self.get_moves(board)
	
