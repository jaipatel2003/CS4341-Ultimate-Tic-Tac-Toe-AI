from re import L
from tabnanny import check
import Tile


class Board():
    def __init__(self):
        # Local Board Game Piece with helper functions such as check tile, assign winner, etc
        self._board = [[Tile.Tile() for j in range(3)] for i in range(3)]
        self._winner = None
        self._global_board = [[self._board for j in range(3)] for i in range(3)]
        self._global_winner = None
        self.highlighted = False

    def find_tile(self, tile):
        if tile == 0:
            return 0, 0
        if tile == 1:
            return 0, 1
        if tile == 2:
            return 0, 2
        if tile == 3:
            return 1, 0
        if tile == 4:
            return 1, 1
        if tile == 5:
            return 1, 2
        if tile == 6:
            return 2, 0
        if tile == 7:
            return 2, 1
        if tile == 8:
            return 2, 2

    def check_tile(self, i, j):
        return not self._board[i][j].get_winner()

    def get_tile_winner(self, i, j):
        if self._board[i][j].get_winner():
            return self._board[i][j].get_winner()
        return None

    def assign_winner_tile(self, tile, winner):
        x, y = self.find_tile(tile)
        # print("tile {} {} with winner {}".format(x,y,winner))
        self.assign_winner_tile_xy(x, y, winner)

    def unassign_winner_tile(self, tile):
        x, y = self.find_tile(tile)
        self.unassign_winner_tile_xy(x, y)

    def assign_winner_tile_xy(self, i, j, winner):
        if i < 0 or i >= 3 or j < 0 or j >= 3:
            raise Exception
        self._board[i][j].assign_winner(winner)
        # print("THIS SSHOUD BE: {} {} {}".format(i,j,self._board[i][j].get_winner()))

    def unassign_winner_tile_xy(self, i, j):
        self._board[i][j].assign_winner(None)

    def print_board(self):
        for i in range(3):
            for j in range(3):
                self.get_tile_winner(i, j)

    def _check_row_winner(self, row):
        if self._board[row][0].get_winner() == self._board[row][1].get_winner() and self._board[row][1].get_winner() == \
                self._board[row][2].get_winner() and self._board[row][0].get_winner():
            return self._board[row][0].get_winner()
        return None

    def _check_col_winner(self, col):
        if self._board[0][col].get_winner() == self._board[1][col].get_winner() and self._board[1][col].get_winner() == \
                self._board[2][col].get_winner() and self._board[0][col].get_winner():
            return self._board[0][col].get_winner()
        return None

    def _check_diagonal(self):
        if self._board[0][0].get_winner() == self._board[1][1].get_winner() and self._board[1][1].get_winner() == \
                self._board[2][2].get_winner() and self._board[0][0].get_winner():
            return self._board[0][0].get_winner()
        if self._board[2][0].get_winner() == self._board[1][1].get_winner() and self._board[1][1].get_winner() == \
                self._board[0][2].get_winner() and self._board[2][0].get_winner():
            return self._board[2][0].get_winner()
        return None

    def get_winner(self) -> str:
        if self._winner:
            return self._winner

        for i in range(3):
            row = self._check_row_winner(i)
            if row:
                self._winner = row
                return self._winner

        for i in range(3):
            col = self._check_col_winner(i)
            if col:
                self._winner = col
                return self._winner

        if self._check_diagonal():
            self._winner = self._check_diagonal()

        return self._winner

    def find_empty_tiles(self, board):
        if self._winner or self.get_winner():
            return []
        tilesEmpty = []
        tile = 0
        for i in range(3):
            for j in range(3):
                if self.check_tile(i, j):
                    tilesEmpty.append((board, tile))
                tile += 1
        return tilesEmpty

