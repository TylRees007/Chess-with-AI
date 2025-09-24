from abc import ABC, abstractmethod


class Board:
    """
    Class to keep track of what piece is where on a board
    """
    def __init__(self):
        """
        Creates the board that will be used in the game and adds the needed pieces to it.
        """
        # Creates all Pawns
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        for i in range(8):
            self.board[1][i] = Pawn("black", [1,i])
            self.board[6][i] = Pawn("white", [6,i])

        for j in range(2):

            # Creates Rooks
            self.board[0][j * 7] = Rook("black", [0,(j * 7)])
            self.board[7][j * 7] = Rook("white", [7,(j * 7)])

            # Creates Knights
            self.board[0][(1 - j) + (6 * j)] = Knight("black", [0, (1 - j) + (6 * j)])
            self.board[7][(1 - j) + (6 * j)] = Knight("white", [7, (1 - j) + (6 * j)])

            # Creates Bishops
            self.board[0][(2 - (2 * j)) + (5 * j)] = Bishop("black", [0, (2 - (2 * j)) + (5 * j)])
            self.board[7][(2 - (2 * j)) + (5 * j)] = Bishop("white", [7, (2 - (2 * j)) + (5 * j)])

        # Creates Queens
        self.board[0][3] = Queen("black", (0, 3))
        self.board[7][3] = Queen("white", (7, 3))

        # Creates Kings
        self.board[0][4] = King("black", (0, 4))
        self.board[7][4] = King("white", (7, 4))

    def update_board(self, src, dst):
        """
        Updates the board based on what piece is moving and to where it is moving to.
        """
        if self.board[src[0]][src[1]] == ' ':
            raise ValueError

        move_piece = self.board[src[0]][src[1]].move(self.board, dst)
        taken_place = self.board[dst[0]][dst[1]]
        self.board[dst[0]][dst[1]] = move_piece
        self.board[src[0]][src[1]] = " "

        return taken_place

    def __str__(self):
        """
        Will output the current board formatted correctly.
        """
        row_num = 8
        str_ret = ""
        border = "  ---------------------------------\n"
        for curr_row in range(8):
            str_ret += f"{(row_num - curr_row)} |"
            for piece in self.board[curr_row]:
                str_ret += f" {piece} |"
            str_ret += f"\n{border}"

        str_ret += border
        str_ret += "    A   B   C   D   E   F   G   H\n"

        return str_ret

class Piece(ABC):
    """
    Genaric Piece class
    """
    def __init__(self, color, curr_pos, piece_type):
        """
        Creates a genaric piece.
        """
        self.color = color
        self.curr_pos = curr_pos
        self.type = piece_type

    @abstractmethod
    def move(self, curr_board, move):
        '''
        This Method will take in the current board state and a potential move to check if it is 
        valid for the piece that it is trying to move it will then change the curr_pos to the 
        move and return true or keep the piece in the same place and return false based on the 
        result of the check.
        '''

    def knight_check(self, curr_board, move):
        """
        Knights moves are invalid unless the piece is a Knight
        """
        return False

    def diagonal_check(self,curr_board,  move):
        '''
        This method will check to see if a diagonal move is valid
        '''
        m_row, m_column = move

        curr_row, curr_column = self.curr_pos
        row_mod = 1
        col_mod = 1

        row_change = abs(m_row - curr_row)
        col_change = abs(m_column - curr_column)

        if curr_row > m_row:
            row_mod = -1

        if curr_column > m_column:
            col_mod = -1

        if curr_board[m_row][m_column] != ' ' and curr_board[m_row][m_column].color == self.color:
            return False

        if row_change != col_change:
            return False

        for i in range(1,col_change):
            if curr_board[curr_row + (i * row_mod)][curr_column + (i * col_mod)] != ' ':
                return False

        return True
    
    def __eq__(self, other):
        if isinstance(other, Piece):
            other = other.color
        return self.color == other

    def straight_check(self,curr_board, move):
        '''
        This method will check to see if a forward or a sideways move is valid
        '''
        m_row, m_column = move

        curr_row, curr_column = self.curr_pos
        row_mod = 0
        col_mod = 0

        row_change = abs(m_row - curr_row)
        col_change = abs(m_column - curr_column)

        if row_change != 0 and col_change != 0:
            return False

        if curr_board[m_row][m_column] == self:
            return False

        if curr_row > m_row:
            row_mod = -1
        elif curr_row < m_row:
            row_mod = 1

        if curr_column > m_column:
            col_mod = -1
        elif curr_column < m_column:
            col_mod = 1

        for i in range(1,row_change):
            if curr_board[curr_row + (i * row_mod)][curr_column + (i * col_mod)] != ' ':
                return False
        for i in range(1,col_change):
            if curr_board[curr_row + (i * row_mod)][curr_column + (i * col_mod)] != ' ':
                return False
        return True

    def validate_move(self, curr_board, move):
        """
        Returns a bool of whether or not a move is valid for this Piece
        """
        ret_bool = self.diagonal_check(curr_board, move) or self.straight_check(curr_board, move) or self.knight_check(curr_board, move)
        return ret_bool

    def __str__(self):
        return self.type

class Pawn(Piece):
    """
    Class to keep track of the information for the Pawn pieces
    """
    def __init__(self, color, curr_pos):
        """
        Creates a Pawn and includes all needed information:
            - first_move: bool for if it this pieces first move
            - type: a string to represent if it is a black or white pawn
            - move_direction: either a 1 or -1 to indicate the valid direction of the pawn
            - name: string to be used when printing what piece this is.
        """
        piece_type = 'p' if color == "black" else 'P'
        super().__init__(color, curr_pos, piece_type)
        self.first_move = True
        self.move_direction = 1 if color == "black" else -1
        self.promote_rank = 7 if color == "black" else 0
        self.name = f"{color.upper()} Pawn"

    def diagonal_check(self, curr_board, move):
        """
        Checks to see if a diagonal move is valid for this pawn. It is only valid when the piece
        one row up and one column over is a differenct colored piece.
        """
        m_row, m_column = move
        curr_row, curr_column = self.curr_pos
        col_change = abs(curr_column - m_column)
        row_change = abs(m_row - curr_row)

        if curr_board[m_row][m_column] == ' ' or curr_board[m_row][m_column] == self:
            return False
        if col_change != 1 or row_change != 1:
            return False
        if curr_row + (row_change * self.move_direction) != m_row:
            return False

        return True

    def straight_check(self, curr_board, move):
        """
        Checks to see if a straight move is valid for this piece: One or two up to an empty space 
        is valid on first move one move up is valid on any other move.
        """
        m_row, m_column = move

        curr_row, curr_column = self.curr_pos

        row_change = abs(m_row - curr_row)
        col_change = abs(curr_column - m_column)

        if col_change != 0:
            return False
        if curr_row + (row_change * self.move_direction) != m_row:
            return False

        if row_change <= 2:
            for i in range(1,row_change + 1):
                if isinstance(curr_board[curr_row + (self.move_direction * i)][curr_column], Piece) or (i == 2 and not self.first_move):
                    return False
        else:
            return False


        return True

    def move(self, curr_board, move):
        """
        Move is passed in as a tuple in the order of (row, column)
                
        Checks to see if a Diagonal or Straigt move is valid with the move passed in if not 
        raise ValueError if reaches past all that return current piece if new row is not the 
        promotion rank, a new queen if it is the promotion rank
        """
        m_row, _ = move

        if self.diagonal_check(curr_board, move) or self.straight_check(curr_board, move):
            self.first_move = False
            self.curr_pos = move

            if m_row == self.promote_rank:
                return Queen(self.color, self.curr_pos)
            return self
        raise ValueError

class Queen(Piece):
    """
    Class to keep track of the information for the Queen pieces
    """
    def __init__(self, color, curr_pos):
        """
        Creates queen piece with all needed information
        """
        piece_type = 'q' if color == "black" else 'Q'
        super().__init__(color, curr_pos, piece_type)
        self.name = f"{color.upper()} Queen"

    def move(self, curr_board, move):
        """
        Verifies that the move is valid then reassigns the curr_pos to equal the move then
        returns self. If the move is invalid raise a value error
        """
        if self.straight_check(curr_board, move) or self.diagonal_check(curr_board, move):
            self.curr_pos = move
            return self
        raise ValueError

class King(Piece):
    """
    Class to keep track of the information for the King pieces
    """
    def __init__(self, color, curr_pos):
        piece_type = 'k' if color == "black" else 'K'
        super().__init__(color, curr_pos, piece_type)
        self.name = f"{color.upper()} King"

    def straight_check(self, curr_board, move):
        """
        Calls Diagonal check to validate the kings moves
        """
        return self.diagonal_check(curr_board, move)

    def diagonal_check(self, curr_board, move):
        """
        Validates if a move is good for the King to execute and returns a bool if it is.
        """

        m_row, m_column = move
        if curr_board[m_row][m_column] == self:
            return False

        curr_row, curr_column = self.curr_pos

        row_change = abs(m_row - curr_row)
        col_change = abs(m_column - curr_column)

        if row_change > 1 or col_change > 1:
            return False

        return True

    def move(self, curr_board, move):
        """
        Verifies that the move is valid then reassigns the curr_pos to equal the move then
        returns self. If the move is invalid raise a value error
        """
        if self.diagonal_check(curr_board, move) or self.straight_check(curr_board, move):
            self.curr_pos = move
            return self
        raise ValueError

    def is_checked(self, curr_board):
        """
        Reports whether or not self is in check
        """
        curr_row, curr_col = self.curr_pos
        num_index = 8

        valid_index = (lambda x: x >= 0 and x < 8)
        knight_moves = [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, 1), (2, -1)]

        # Knight Check
        for row_change, col_change in  knight_moves:
            check_row = curr_row + row_change
            check_col = curr_col + col_change

            if valid_index(check_row) and valid_index(check_col):
                test_piece = curr_board[check_row][check_col]
                if isinstance(test_piece, Knight) and test_piece.validate_move(curr_board, self.curr_pos):
                    return True

        row_mod = 1
        col_mod = 1

        # Back Right Check
        for i in range(1,num_index):
            check_row = curr_row + (i * row_mod)
            check_col = curr_col + (i * col_mod)
            if valid_index(check_row) and valid_index(check_col):
                test_piece = curr_board[check_row][check_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        row_mod = -1
        col_mod = 1

        # Forward Right Check
        for i in range(1,num_index):
            check_row = curr_row + (i * row_mod)
            check_col = curr_col + (i * col_mod)
            if valid_index(check_row) and valid_index(check_col):
                test_piece = curr_board[check_row][check_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        # Right Check
        for i in range(1,num_index):
            check_col = curr_col + (i * col_mod)
            if valid_index(check_col):
                test_piece = curr_board[curr_row][check_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        # Forward Check
        for i in range(1,num_index):
            check_row = curr_row + (i * row_mod)
            if valid_index(check_row):
                test_piece = curr_board[check_row][curr_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        row_mod = 1
        col_mod = -1

        # Back Left Check
        for i in range(1,num_index):
            check_row = curr_row + (i * row_mod)
            check_col = curr_col + (i * col_mod)
            if valid_index(check_row) and valid_index(check_col):
                test_piece = curr_board[check_row][check_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        # Left Check
        for i in range(1,num_index):
            check_col = curr_col + (i * col_mod)
            if valid_index(check_col):
                test_piece = curr_board[curr_row][check_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        # Back Check
        for i in range(1,num_index):
            check_row = curr_row + (i * row_mod)
            if valid_index(check_row):
                test_piece = curr_board[check_row][curr_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        row_mod = -1
        col_mod = -1

        # Back Left Check
        for i in range(1,num_index):
            check_row = curr_row + (i * row_mod)
            check_col = curr_col + (i * col_mod)
            if valid_index(check_row) and valid_index(check_col):
                test_piece = curr_board[check_row][check_col]
                if isinstance(test_piece, Piece):
                    if test_piece.validate_move(curr_board, self.curr_pos):
                        return True
                    break
            else:
                break

        return False

class Knight(Piece):
    """
    Class to keep track of the information for the Knight pieces
    """
    def __init__(self, color, curr_pos):
        """
        Creates all needed info for the Rook
        """
        piece_type = 'n' if color == "black" else 'N'
        super().__init__(color, curr_pos, piece_type)
        self.name = f"{color.upper()} Knight"

    def straight_check(self, curr_board, move):
        """
        Straight moves are always invalid for the Knight
        """
        return False

    def diagonal_check(self, curr_board, move):
        """
        Straight moves are always invalid for the Knight
        """
        return False

    def knight_check(self, curr_board, move):
        """
        Validates if the move is an approved Knight movement and returns a bool of if it is or not
        """
        m_row, m_column = move

        if curr_board[m_row][m_column] == self:
            return False

        curr_row, curr_column = self.curr_pos

        row_change = abs(m_row - curr_row)

        col_change = abs(m_column- curr_column)

        if (row_change == 1 and col_change == 2) or (row_change == 2 and col_change == 1):
            return True

        return False

    def move(self, curr_board, move):
        """
        Verifies that the move is valid then reassigns the curr_pos to equal the move then
        returns self. If the move is invalid raise a value error
        """

        if self.knight_check(curr_board, move):
            self.curr_pos = move
            return self

        raise ValueError

class Rook(Piece):
    """
    Class to keep track of the information for the Rook pieces
    """
    def __init__(self, color, curr_pos):
        """
        Creates all needed info for the Rook
        """
        piece_type = 'r' if color == "black" else 'R'
        super().__init__(color, curr_pos, piece_type)
        self.name = f"{color.upper()} Rook"

    def diagonal_check(self, curr_board, move):
        """
        Diagonal moves are always invalid for Rooks
        """
        return False

    def move(self, curr_board, move):
        """
        Verifies that the move is valid then reassigns the curr_pos to equal the move then
        returns self. If the move is invalid raise a value error
        """
        if self.straight_check(curr_board,move):
            self.curr_pos = move
            return self

        raise ValueError

class Bishop(Piece):
    """
    Class to keep track of the information for the Bishop pieces
    """
    def __init__(self, color, curr_pos):
        piece_type = 'b' if color == "black" else 'B'
        super().__init__(color, curr_pos, piece_type)
        #self.type = 'b' if color == "black" else 'B'
        self.name = f"{color.upper()} Bishop"

    def straight_check(self, curr_board, move):
        """
        Straight moves are always invalid for Bishops
        """
        return False

    def move(self, curr_board, move):
        """
        Verifies that the move is valid then reassigns the curr_pos to equal the move then returns
        self. If the move is invalid raise a value error
        """

        if self.diagonal_check(curr_board, move):
            self.curr_pos = move
            return self
        raise ValueError
