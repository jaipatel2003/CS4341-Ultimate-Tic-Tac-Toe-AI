from unittest.util import strclass


class Tile():
    def __init__(self) -> None:
        #Object Tile that make up a board
        self._winner = 0

    def assign_winner(self, winner: str) -> None:
        #Assign winner if tile is occupied by symbol
        self._winner = winner

    def get_winner(self) -> str:
        #Grab symbol on tile
        return self._winner

    def __str__(self):
        return f"{self._winner}"
