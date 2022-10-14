import Board

class GlobalBoard():
    def __init__(self,boards):
        self._global_board = boards
        self._global_winner = None

    def get_global_winner(self) -> str:
        if self._global_winner:
            return self._global_winner

        for i in range(3):
            row = self._check_global_row_winner(i)
            if row:
                self._global_winner = row
                return self._global_winner

        for i in range(3):
            col = self._check_global_col_winner(i)
            if col:
                self._global_winner = col
                return self._global_winner

        if self._check_global_diagonal():
            self._global_winner = self._check_global_diagonal()

        elif self._check_tie():
            self._global_winner = "Tie"
        return self._global_winner

    def get_board_winnner(self,board):
        return self._global_board[board].get_winner()

    def get_board(self,board):
        return self._global_board[board]


    def _check_global_row_winner(self, row):
        if self._global_board[row * 3].get_winner() == self._global_board[row * 3 + 1].get_winner() and self._global_board[
            row * 3 + 1].get_winner() ==  self._global_board[row * 3 + 2].get_winner() and self._global_board[row * 3]:
            return self._global_board[row * 3].get_winner()
        return None

    def _check_global_col_winner(self, col):
        if self._global_board[col].get_winner() == self._global_board[col + 3].get_winner() and self._global_board[
            col + 3].get_winner() ==  self._global_board[col + 6].get_winner() and self._global_board[col]:
            return self._global_board[col].get_winner()
        return None

    def _check_global_diagonal(self):
        if self._global_board[0].get_winner() == self._global_board[4].get_winner() and self._global_board[4].get_winner() == \
                self._global_board[8].get_winner() and self._global_board[0].get_winner():
            return self._global_board[0].get_winner()
        if self._global_board[2].get_winner() == self._global_board[4].get_winner() and self._global_board[4].get_winner() == \
                self._global_board[6].get_winner() and self._global_board[2].get_winner():
            return self._global_board[2].get_winner()
        return None

    def _check_tie(self):
        for i in range(9):
            if not self._global_board[i].get_winner():
                return False
        return True