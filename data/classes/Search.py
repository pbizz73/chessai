from data.classes.Board import Board
import model_v1 as model
import torch
import fen2BB
import pytorch_lightning as pl


class Searcher:
    def __init__(self) -> None:
        chessBot = model.EvaluationModel.load_from_checkpoint("lightning_logs/version_47/checkpoints/modelV1")
        chessBot.eval()
        self.mps_device = torch.device('mps')
        chessBot.to(self.mps_device)
        self.bot = chessBot
    #alpha = -inf, beta = +inf
    #figure out why this is not working
    def search(self, depth, board, alpha,beta, maximizing_player = False):
        if depth == 0:
            return  None,self.evaluate(board)
        moves = board.generate_moves(board.turn)
        if len(moves) == 0:
            if board.is_in_checkmate(board.turn):
                return None,-1000.0
            return None,0.0
        best_move = None
        if maximizing_player:
            max_eval = -100.0
            for move in moves:
                starting_square = move[0]
                target_square = move[1]
                copy_of_board = Board(board=board)
                target_square = copy_of_board.get_square_from_pos(target_square.pos)
                starting_square = copy_of_board.get_square_from_pos(starting_square.pos)
                piece2move =copy_of_board.get_piece_from_pos(starting_square.pos)
                copy_of_board.selected_piece = piece2move
                if  piece2move.move(copy_of_board, target_square):
                    copy_of_board.turn = 'white' if copy_of_board.turn == 'black' else 'black'
                current_eval = self.search(depth-1,copy_of_board,alpha,beta, False)[1]
                del copy_of_board
                if current_eval> max_eval:
                    max_eval = current_eval
                    best_move = move
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return best_move,max_eval
        else:
            min_eval = 100.0
            for move in moves:
                starting_square = move[0]
                target_square = move[1]
                copy_of_board = Board(board=board)
                target_square = copy_of_board.get_square_from_pos(target_square.pos)
                starting_square = copy_of_board.get_square_from_pos(starting_square.pos)
                piece2move =copy_of_board.get_piece_from_pos(starting_square.pos)
                copy_of_board.selected_piece = piece2move
                if  piece2move.move(copy_of_board, target_square):
                    copy_of_board.turn = 'white' if copy_of_board.turn == 'black' else 'black'
                current_eval = self.search(depth-1,copy_of_board,alpha,beta, True)[1]
                del copy_of_board
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
                beta = min(beta,current_eval)
                if beta<=alpha:
                    break
            return best_move, min_eval



        #for each move, make a copy of the Board, move the piece in that board, evaulte the postion,
        #record eval, delete copy of board
            

    def evaluate(self, board):
        fen = board.generate_fen()
        binary_fen = fen2BB.fen2BB(fen)
        t = torch.from_numpy(binary_fen).to(self.mps_device)
        prediction = self.bot(t).item()
        print(fen + " the prediction is " + str(prediction))
        return prediction

    