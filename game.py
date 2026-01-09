"""
This is a simple chess program that allows you and another person to play chess in the console

Enter your move in the format (Source)-(Destination) listing the column letter then the row number
The game will alternate whose turn it is until one of the kings is captured ending the game.
"""
import sys
from chess import Board, Piece, King, Knight
from chess_bot import SimpleBot

class Game:
    """
    Class to keep track of the current game being played
    """
    def __init__(self):
        self.game_board = Board()

        self.active_white_pieces = self.game_board.board[6] + self.game_board.board[7]
        self.active_black_pieces = self.game_board.board[0] + self.game_board.board[1]

        self.white_taken = []
        self.black_taken = []

        self.white_score = 0
        self.black_score = 0

        self.kings = {"black" : self.game_board.board[0][4], "white": self.game_board.board[7][4]}
        self.curr_move = "white"
    
    def detect_checkmate(self):
        """
        This method will detect if the current player is in checkmate
        """
        pass

    def check_detection(self):
        """
        This method will check to see if either king is in check at the end of the moves
            - Check from the king for each diagonal and straight until a peice is 
                reached then see if the move from that piece to the king is valid
            - Check for each knight
            - If a Check ever comed back as true for one king mark it and move on 
                to the next king or the return.
            - Return a tuple of two booleans representing if a king is in check 
                or not (black king bool, white king bool)
        """
        black_check = self.kings['black'].is_checked(self.game_board.board)
        white_check = self.kings['white'].is_checked(self.game_board.board)

        if black_check:
            print("\nBLACK King in check!")

        if white_check:
            print("\nWHITE King in check!")
    

    def run_game(self):
        """
        Main driver for the Game class
        """
        king_capture = False
        file = None
        bot = SimpleBot()
        if len(sys.argv) > 1:
            file = open(sys.argv[1], 'w', encoding = "utf-8")
        while True:
            print("\n----------------------------------")
            self.check_detection()
            print(f"\nBlack Score: {self.black_score}\n")
            print(f"Black Taken: {self.black_taken}\n")
            print(self.game_board)
            print(f"White Score: {self.white_score}\n")
            print(f"White Taken: {self.white_taken}\n")
            if self.curr_move == "white":
                move = input(f"{self.curr_move.upper()}'s move: ").strip()
            else:
                move = bot.move_bot(self.active_black_pieces, self.game_board)
            if file is not None:
                file.write(f"{move}\n")
            if isinstance(move, str) and move.lower() == "q":
                break

            try:
                if self.curr_move == "white":
                    print(f"{move} ", end = '')
                    source, dest = move.split('-')
                    s_column, s_row = list(source)
                    s_column = ord(s_column.upper()) - 65
                    s_row = 8 - int(s_row)

                    d_column, d_row = list(dest)
                    d_column = ord(d_column.upper()) - 65
                    d_row =  8 - int(d_row)

                    if s_column < 0 or d_column < 0:
                        raise ValueError

                    if d_row < 0 or d_column < 0:
                        raise ValueError

                    source = (s_row, s_column)
                    dest = (d_row,d_column)
                else:
                    source = move[0]
                    s_row = source[0]
                    s_column = source[1]

                    dest = move[1]
                    d_row = dest[0]
                    d_column = dest[1]

                if self.game_board.board[s_row][s_column].color != self.curr_move:
                    raise ValueError

                sq_tkn = self.game_board.update_board(source,dest, self.kings)
                if isinstance(sq_tkn, Piece):
                    if self.curr_move == "white":

                        self.active_black_pieces.remove(sq_tkn)

                        self.white_taken.append(sq_tkn)
                        self.white_taken.sort()

                        self.white_score += sq_tkn.point
                    else:
                        self.active_white_pieces.remove(sq_tkn)

                        self.black_taken.append(sq_tkn)
                        self.black_taken.sort()

                        self.black_score += sq_tkn.point


                    print(f"{self.game_board.board[d_row][d_column].name} captured {sq_tkn.name}")
                    if isinstance(sq_tkn, King):
                        king_capture = True
                        break

            except (IndexError, ValueError, AttributeError):
                print("INALID MOVE TRY AGAIN")
                continue


            self.curr_move = "black" if self.curr_move == "white" else "white"

        print(f"\n{self.game_board}")
        if file is not None:
            file.close()
        if king_capture:
            winning_color = 'BLACK' if sq_tkn.color == 'white' else 'WHITE'

            print(f"\nGAME OVER:\n{winning_color} WINS!\n")

def main():
    """
    Programs main
    """
    curr_game = Game()

    curr_game.run_game()

if __name__ == "__main__":
    main()
