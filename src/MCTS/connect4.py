OUTCOME_DRAW = 0
OUTCOME_ONE = 1
OUTCOME_TWO = 2
    
PIECE_NONE = ' '
PIECE_ONE = 'x'
PIECE_TWO = 'o'

"""
Models the game of Connect 4 for simulations
"""
class Connect4:
    
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [[PIECE_NONE] * columns for row in range(rows)]
        self.player = PIECE_ONE
        self.lastMove = None
    
    def __str__(self):
        """
        Print Connect 4 board
        """
        boardStr = ""
        boardStr += " 0 1 2 3 4 5 6\n"

        for row in self.board:
            boardStr += '|' + '|'.join(row) + '|' + '\n'
        boardStr += "-" * (self.columns * 2 + 1)
        return boardStr

    def switchPlayer(self):
        """
        Toggle between the two players
        """
        self.player = PIECE_TWO if self.player == PIECE_ONE else PIECE_ONE

    def getLegalMoves(self):
        """
        Return a list of legal moves that a player can make.
        """
        legalMoves = []
        # If column is not full, player can make a move
        for col in range(self.columns):
            if self.board[0][col] == PIECE_NONE:
                legalMoves.append(col)
        return legalMoves

    def dropPiece(self, column):
        """
        Drop a piece into the specified column.
        """
        for row in reversed(range(self.rows)):
            if self.board[row][column] == PIECE_NONE:
                self.board[row][column] = self.player
                self.lastMove = (row, column)
                return
        
    def checkWinFrom(self, row, column):
        """
        Check if a player has won the Connect 4 game by looking 
        for four discs of the same color in a row (vertically, horizontally, and diagonally) 
        in the specified location.
        """
        piece = self.board[row][column]
        # check vertically, horizontally, and diagonally
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for y, x in directions:
            # Count first piece
            count = 1 
            
            # Check +dir
            newRow, newCol = row + y, column + x
            while -1 < newRow < self.rows and -1 < newCol < self.columns:
                if self.board[newRow][newCol] == piece:
                    count += 1
                    newRow += y
                    newCol += x
                else:
                    break

            # Check -dir
            newRow, newCol = row - y, column - x
            while -1 < newRow < self.rows and -1 < newCol < self.columns:
                if self.board[newRow][newCol] == piece:
                    count += 1
                    newRow -= y
                    newCol -= x
                else:
                    break

            if count >= 4:
                return True
        return False
            
    def isGameOver(self):
        """
        Check if the game is over.
        """
        if self.lastMove is None: # No moves have been made, so the game is not over
            return False
        if self.checkWinFrom(self.lastMove[0], self.lastMove[1]):
            return True
        if len(self.getLegalMoves()) == 0:
            return True
        return False
        
    def getOutcome(self):
        """
        Determine if the game ended in a win for a specific player or a draw.
        """
        if self.checkWinFrom(self.lastMove[0], self.lastMove[1]):
            return OUTCOME_ONE if self.player == PIECE_ONE else OUTCOME_TWO
        else:
            return OUTCOME_DRAW
            