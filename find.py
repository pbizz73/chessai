import chess
import numpy as np
from typing import Optional

def findRooks(Board:chess.Board, color: bool) -> Optional[chess.Square]:

        rook_mask = Board.occupied_co[color] & Board.rooks 
        return rook_mask if rook_mask else 0
def findQueens(Board:chess.Board, color: bool) -> Optional[chess.Square]:

        Queen_mask = Board.occupied_co[color] & Board.queens 
        return Queen_mask if Queen_mask else 0
def findBishops(Board:chess.Board, color: bool) -> Optional[chess.Square]:

        Bishop_mask = Board.occupied_co[color] & Board.bishops
        return Bishop_mask if Bishop_mask else 0
def findKnights(Board:chess.Board, color: bool) -> Optional[chess.Square]:

        knights_mask = Board.occupied_co[color] & Board.knights
        return knights_mask if knights_mask else 0
def findPawns(Board:chess.Board, color: bool) -> Optional[chess.Square]:

        pawns_mask = Board.occupied_co[color] & Board.pawns
        return pawns_mask if pawns_mask else 0

def findEn_Passant(Board:chess.Board) -> Optional[chess.Square]:

        ep_mask = Board.ep_square
        return ep_mask if ep_mask else 0

def bin_array(num, m):
    """Convert a positive integer num into an m-bit bit vector"""
    return np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8)
fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"