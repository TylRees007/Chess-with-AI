import pytest
from chess import Piece, Pawn, King, Knight, Queen, Bishop, Board

def sep_move_info(move):
    source, dest = move.split('-')
    s_column, s_row = list(source)
    s_column = ord(s_column.upper()) - 65
    s_row = 8 - int(s_row)

    d_column, d_row = list(dest)
    d_column = ord(d_column.upper()) - 65
    d_row =  8 - int(d_row)
    
    return [(s_row, s_column), (d_row, d_column)]

def test_pawn_movement():
    test_board = Board()

    moves = ['E2-E3', 'E7-E6', 'D2-D4', 'C7-C5', 'D4-E5', 'D4-C5', 'q']

    for move in moves:
        try:
            src, dst = sep_move_info(move)
            test_board.UpdateBoard(src, dst)
        except ValueError:
            pass
    
    assert isinstance(test_board.board[5][4], Pawn) and test_board.board[5][4].color == "white"
    assert isinstance(test_board.board[3][2], Pawn) and test_board.board[3][2].color == "white"
    assert isinstance(test_board.board[2][4], Pawn) and test_board.board[2][4].color == "black"


    
