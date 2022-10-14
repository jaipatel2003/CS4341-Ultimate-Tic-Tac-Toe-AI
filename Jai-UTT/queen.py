from operator import truediv
import os
from re import X
from tkinter import Y
from Board import Board
from GlobalBoard import GlobalBoard
from AiV2 import *
import time
from copy import deepcopy
import argparse
import sys

player = "queen"
boards = [Board() for i in range(9)]
globalBoard = GlobalBoard(boards)
op = None
time_limit_to_think = 10

def startup():
    global player, op,time_limit_to_think

    parser = argparse.ArgumentParser(description="Grabbing to see if there is a new time limit to think")
    parser.add_argument("--time_limit", type=int, help="Time limit to think (default 10 seconds)", required=False)
    args = parser.parse_args(sys.argv[1:])
    time_limit_to_think = 10 if args.time_limit is None else args.time_limit

    while not os.path.exists("first_four_moves"):
        time.sleep(0.5)
        continue

    board, tile, op = mark_startup()
    lastMove = (board, tile)
    while not os.path.exists("queen.go"):
        time.sleep(0.5)
        continue

    with open('move_file', "r") as f:
        if f.readline():
            lastMove = mark_last_move()

    board = find_next_board(lastMove)
    move = find_next_move(board)

    play_move(move)


def mark_startup():
    lines = []
    op = None
    with open("first_four_moves", "r") as file:
        lines = file.readlines()
    player, board, tile = None, None, None
    for line in lines:
        player, board, tile = line.split(" ")
        if player != "queen":
            op = player
        tile = tile[0]
        #print(tile)
        mark_board(player, board, tile)
    return board, tile, op


def mark_last_move():
    lines = []
    with open("move_file") as file:
        lines = file.readlines()
    line = lines[0]
    player, board, tile = line.split(" ")
    if player == "queen":
        time.sleep(0.5)
        wait_turn()
    tile = tile[0]
    mark_board(op, board, tile)
    boards[int(board)].get_winner()
    #print("king: played tile {} on board {}".format(tile, board))
    return board, tile


def wait_turn():
    if os.path.exists("end_game"):
        exitGame()
    while not os.path.exists("queen.go"):
        time.sleep(0.5)
        continue
    lastMove = mark_last_move()
    board = find_next_board(lastMove)
    move = find_next_move(board)
    play_move(move)


def exitGame():
    #print("Here we goooo: {}".format(globalBoard.get_global_winner()))
    print(my_heuristic_eval(deepcopy(globalBoard),player))
    print("board score finale^\n")
    #print("Found winner to global board - exiting.....")
    time.sleep(1)
    quit()


def find_next_move(board):
    global boards, player, op, globalBoard
    #\print(my_heuristic_eval(deepcopy(boards),player))
    #print("board score^\n")
    board, tile, score = heuristic_strat(
        deepcopy(boards), player, op, board,time.time(),time_limit_to_think)
    if not board or not tile:  # if tiles could not be found
        choices = []
        #print(
            #f"No choices found for board {board} because {boards[board].get_winner()}")
        #print(f"Board Tiles {boards[board].print_board()}")
        if boards[board].get_winner():
            for i in range(9):
                choices.append((i, boards[i].find_empty_tiles(i)))
        else:
            for choice in boards[board].find_empty_tiles(board):
                choices.append((board, choice))
        move = choices[0]
    #print(board, tile, score)
    move = board, tile
    return move


def play_move(move): #assign a move and write to file
    board, tile = move
    x, y = find_tile(tile)
    boards[board].assign_winner_tile_xy(x, y, player)
    boards[board].get_winner()
    # with open("move_file", 'w') as file:
    #     file.write(f'queen {board} {tile}')
    #for i in range(0,9):
        #print("here we goo for local {}: {}".format(i,boards[i].get_winner()))
    #print()
    file = open('move_file', 'r+')
    file.seek(0)
    file.write(f'queen {board} {tile}')
    file.truncate()
    file.close()
    wait_turn()


def find_next_board(lastMove):
    board, tile = lastMove
    row, col = find_tile(tile)
    board = find_board(row, col)
    return board


def find_tile(tile):
    #print(tile)
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


def mark_board(player, board, tile):
    global boards
    board = int(board)
    #print(tile)
    x, y = find_tile(tile)
    boards[board].assign_winner_tile_xy(x, y, player)
    boards[board].get_winner()


if __name__ == "__main__":
    startup()