import pygame
import model_v1 as model
import torch
import fen2BB

from data.classes.Board import Board
from data.classes.Search import Searcher

chessBot = model.EvaluationModel.load_from_checkpoint("lightning_logs/version_47/checkpoints/modelV1")
chessBot.eval()
device = torch.device('cpu')
chessBot.to(device)

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])
board = Board(board=board)
mysearcher = Searcher()

def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()
def searchMyBoard(board, searcher, maximzing_player = False):
	mysearcher = searcher
	best_move = (mysearcher.search(2,board,-100.0,100.0,maximzing_player ))[0]
	best_move_start = best_move[0]
	best_move_end = best_move[1]
	piece2move = board.get_piece_from_pos(best_move_start.pos)
	if piece2move.move(board,best_move_end):
		print(board.turn + " has succsefully moved")
	else:
		print("uhoh")


if __name__ == '__main__':
	running = True
	while running:
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			fen = board.generate_fen()
			binaryFen = fen2BB.fen2BB(fen)
			t = torch.from_numpy(binaryFen)
			prediction = chessBot(t).item()
			print(board.generate_fen() + ", the prediction of this postion is "+ str(prediction) )
			
			# Quit the game if the user presses the close button
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: 
       		# 	# If the mouse is clicked
				if event.button == 1:
					if board.turn == 'black':
						searchMyBoard(board,mysearcher)
						board.turn = 'white' if board.turn == 'black' else 'black'
					else:
						board.handle_click(mx, my, chessBot)
		if board.is_in_checkmate('black'): # If black is in checkmate
			print('White wins!')
			running = False
		elif board.is_in_checkmate('white'): # If white is in checkmate
			print('Black wins!')
			running = False
		elif board.halfmovenumber  == 100:
			print('Draw')
			running = False
		# Draw the board
		draw(screen)