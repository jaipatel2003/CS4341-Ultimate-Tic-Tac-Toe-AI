from operator import truediv
import os
from re import X
from tkinter import Y
from Board import Board
from GlobalBoard import GlobalBoard
from Ai import *
import time
from copy import deepcopy
import argparse
import sys

player = "king"
boards = [Board() for i in range(9)]
globalBoard = GlobalBoard(boards)
op = None
time_limit = 10


def startup():
    global player, op, time_limit

    parser = argparse.ArgumentParser(description="Grabbing to see if there is a new time limit to think")
    parser.add_argument("--time_limit", type=int, help="Time limit to think (default 10 seconds)", required=False)
    args = parser.parse_args(sys.argv[1:])
    time_limit = 10 if args.time_limit is None else args.time_limit

    while not os.path.exists("first_four_moves"):  # wait for first four moves
        time.sleep(0.5)
        continue

    board, tile, op = mark_startup()
    lastMove = (board, tile)
    while not os.path.exists("king.go"):  # wait till its tunr
        time.sleep(0.5)
        continue

    with open('move_file', "r") as f:
        if f.readline():
            lastMove = mark_last_move()  # mark opponets last move

    board = find_next_board(lastMove)  # find next board to play on
    move = find_next_move(board)  # find next move using strat

    play_move(move)


def mark_startup():  # mark first four moves
    lines = []
    op = None
    with open("first_four_moves", "r") as file:
        lines = file.readlines()
    player, board, tile = None, None, None
    for line in lines:
        player, board, tile = line.split(" ")
        if player != "king":
            op = player
        tile = tile[0]
        mark_board(player, board, tile)
    return board, tile, op


def mark_last_move():  # mark ops move
    lines = []
    with open("move_file") as file:
        lines = file.readlines()
    line = lines[0]
    player, board, tile = line.split(" ")
    if player == "king":
        time.sleep(0.5)
        wait_turn()
    tile = tile[0]
    mark_board(op, board, tile)
    boards[int(board)].get_winner()
    return board, tile


def wait_turn():
    if os.path.exists("end_game"):  # if refree said game over
        exitGame()
    while not os.path.exists("king.go"):  # wait till its turn
        time.sleep(0.5)
        continue
    lastMove = mark_last_move()
    board = find_next_board(lastMove)
    move = find_next_move(board)

    play_move(move)


def exitGame():
    print("Found winner to global board - exiting.....")
    time.sleep(1)
    quit()


def find_next_move(board):
    global boards, player, op, globalBoard
    print(heuristic_eval(deepcopy(boards), player))
    print("check this config^")
    board, tile, score = heuristic_strat(
        deepcopy(boards), player, op, board, time.time(), time_limit)  # min max, with current time
    if not board or not tile:  # if tiles could not be found, should be unnesarry but just in case for error handling
        choices = []
        if boards[board].get_winner():
            for i in range(9):
                choices.append((i, boards[i].find_empty_tiles(i)))
        else:
            for choice in boards[board].find_empty_tiles(board):
                choices.append((board, choice))
        move = choices[0]
    move = board, tile
    return move


def play_move(move):  # assign a move and write to file
    board, tile = move
    x, y = find_tile(tile)
    boards[board].assign_winner_tile_xy(x, y, player)
    boards[board].get_winner()
    # with open("move_file", 'w') as file:
    #     file.write(f'king {board} {tile}')
    file = open('move_file', 'r+')
    file.seek(0)
    file.write(f'king {board} {tile}')
    file.truncate()
    file.close()
    wait_turn()


def find_next_board(lastMove):
    board, tile = lastMove
    row, col = find_tile(tile)
    board = find_board(row, col)
    return board


def find_tile(tile):  # find tile and convert to row col
    tile = int(tile)
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


def mark_board(player, board, tile):  # mark the board with desired move
    global boards
    board = int(board)
    x, y = find_tile(tile)
    # print(board)
    boards[board].assign_winner_tile_xy(x, y, player)
    for r in range(0, 3):
        for c in range(0, 3):
            winner = boards[0].get_tile_winner(r, c)
            # print("on {} {} we had winner {}".format(r,c,winner))
    # print("This is board {}".format(board))
    boards[board].get_winner()


if __name__ == "__main__":
    startup()