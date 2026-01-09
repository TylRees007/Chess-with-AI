from chess import Board, Piece, King, Knight
import random

class ChessBot:

    def generate_valid_moves(self, pieces, curr_board):
        """
        this method will generate all valid moves for the current player
        """
        valid_moves = {}
        
        num_index = 8
        surrounding_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, 1), (2, -1)]

        valid_index = (lambda x: x >= 0 and x < 8)

        

        for piece in pieces:
            if isinstance(piece, Knight):
                for row_change, col_change in  knight_moves:
                    check_row = piece.curr_pos[0] + row_change
                    check_col = piece.curr_pos[1] + col_change
                    if valid_index(check_row) and valid_index(check_col):
                        if piece.validate_move(curr_board.board, (check_row, check_col)):
                            if piece in valid_moves:
                                valid_moves[piece].append((check_row, check_col))
                            else:
                                valid_moves[piece] = [(check_row, check_col)]
                        

            for row, col in surrounding_moves:
                for i in range(1,num_index):
                    check_row = piece.curr_pos[0] + (i * row)
                    check_col = piece.curr_pos[1] + (i * col)
                    if valid_index(check_row) and valid_index(check_col):
                        if piece.validate_move(curr_board.board, (check_row, check_col)):
                            if piece in valid_moves:
                                valid_moves[piece].append((check_row, check_col))
                            else:
                                valid_moves[piece] = [(check_row, check_col)]
                    else:
                        break
        return valid_moves


class SimpleBot(ChessBot):
    def move_bot(self, pieces, curr_board):
        possible_moves = self.generate_valid_moves(pieces, curr_board)
        piece = random.choice(list(possible_moves.keys()))
        move = random.choice(possible_moves[piece])
        return [piece.curr_pos, move]