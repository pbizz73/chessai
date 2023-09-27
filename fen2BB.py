import chess
import numpy as np
from typing import Optional
import find

WHITE = chess.WHITE
BLACK = chess.BLACK
fen= "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

bitBoard = chess.Board(fen=fen)
if bitBoard.turn == chess.WHITE:
    turnBitBoard = 16
else:
    turnBitBoard = 0



def fen2BB(fen):
    bitBoard = chess.Board(fen=fen)
    if bitBoard.turn == chess.WHITE:
        turnBitBoard = 16
    else:
        turnBitBoard = 0
    #white Pieces
    bitBoardWRooks = np.array(find.bin_array(find.findRooks(bitBoard,WHITE),64))
    bitBoardWQueens = np.array(find.bin_array(find.findQueens(bitBoard,WHITE),64))
    bitBoardWPawns = np.array(find.bin_array(find.findPawns(bitBoard,WHITE),64))
    bitBoardWKnights = np.array(find.bin_array(find.findKnights(bitBoard,WHITE),64))
    bitBoardWBishops = np.array(find.bin_array(find.findBishops(bitBoard,WHITE),64))
    bitBoardWKings = np.array(find.bin_array(bitBoard.king(WHITE),64))
    bitBoardPiecesWhite = np.concatenate((bitBoardWRooks,bitBoardWQueens,bitBoardWPawns, bitBoardWKnights,bitBoardWKings, bitBoardWBishops))

#black Pieces
    bitBoardBRooks = np.array(find.bin_array(find.findRooks(bitBoard,BLACK),64))
    bitBoardBQueens = np.array(find.bin_array(find.findQueens(bitBoard,BLACK),64))
    bitBoardBPawns = np.array(find.bin_array(find.findPawns(bitBoard,BLACK),64))
    bitBoardBKnights = np.array(find.bin_array(find.findKnights(bitBoard,BLACK),64))
    bitBoardBBishops = np.array(find.bin_array(find.findBishops(bitBoard,BLACK),64))
    bitBoardBKings = np.array(find.bin_array(bitBoard.king(WHITE),64))
    bitBoardPiecesBlack= np.concatenate((bitBoardBRooks,bitBoardBQueens,bitBoardBPawns, bitBoardBKnights,bitBoardBKings,bitBoardBBishops))

    bitBoardCastlingRights = np.array(find.bin_array(bitBoard.castling_rights,64))
    bitBoardEP = np.array(find.bin_array(find.findEn_Passant(bitBoard),64))
    fullMoveNum= np.array(find.bin_array(bitBoard.fullmove_number,8))
    halfMoveNum= np.array(find.bin_array(bitBoard.halfmove_clock,8))
    turnBitBoard= np.array(find.bin_array(turnBitBoard,8))

    bitBoardFinal = np.concatenate((bitBoardPiecesWhite,bitBoardPiecesBlack))
    bitBoardFinal = np.append(bitBoardFinal,turnBitBoard )
    bitBoardFinal = np.concatenate((bitBoardFinal,bitBoardCastlingRights,bitBoardEP))

    bitBoardFinal = np.append(bitBoardFinal, fullMoveNum)
    bitBoardFinal = np.append(bitBoardFinal, halfMoveNum)

    return bitBoardFinal.astype(np.float32)


                               





