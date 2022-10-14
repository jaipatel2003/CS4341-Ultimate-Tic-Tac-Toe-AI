from os import popen
from tkinter.tix import INTEGER
from scipy import rand
from GlobalBoard import GlobalBoard
import time
from copy import deepcopy
import random


def find_board(row, col):
    # Converts row and col to board -> Returns board number
    if (row, col) == (0, 0):
        return 0
    if (row, col) == (0, 1):
        return 1
    if (row, col) == (0, 2):
        return 2
    if (row, col) == (1, 0):
        return 3
    if (row, col) == (1, 1):
        return 4
    if (row, col) == (1, 2):
        return 5
    if (row, col) == (2, 0):
        return 6
    if (row, col) == (2, 1):
        return 7
    if (row, col) == (2, 2):
        return 8


def _calc_adj_points(points, i, j, k):
    # Helper function for eval function to check for blocks and adj tiles
    if points[i] > 0 and points[j] > 0 and points[k] >= 0:
        return 5
    if points[i] < 0 and points[j] < 0 and points[k] <= 0:
        return -5
    if points[i] < 0 and points[j] < 0 and points[k] >= 0:
        return -2
    if points[i] > 0 and points[j] > 0 and points[k] <= 0:
        return 2
    else:
        return 0


def _check_in_2_adj(points):
    # Helper function to evaluvate all legal combinations of the board
    score = 0

    score += _calc_adj_points(points, 0, 1, 2)
    score += _calc_adj_points(points, 0, 2, 1)
    score += _calc_adj_points(points, 0, 4, 8)
    score += _calc_adj_points(points, 0, 8, 4)
    score += _calc_adj_points(points, 0, 3, 6)
    score += _calc_adj_points(points, 0, 6, 3)

    score += _calc_adj_points(points, 1, 0, 2)
    score += _calc_adj_points(points, 1, 2, 0)
    score += _calc_adj_points(points, 1, 4, 7)
    score += _calc_adj_points(points, 1, 7, 4)

    score += _calc_adj_points(points, 2, 1, 0)
    score += _calc_adj_points(points, 2, 0, 1)
    score += _calc_adj_points(points, 2, 4, 6)
    score += _calc_adj_points(points, 2, 6, 4)
    score += _calc_adj_points(points, 2, 5, 8)
    score += _calc_adj_points(points, 2, 8, 5)

    score += _calc_adj_points(points, 3, 4, 5)
    score += _calc_adj_points(points, 3, 5, 4)
    score += _calc_adj_points(points, 3, 0, 6)
    score += _calc_adj_points(points, 3, 6, 0)

    score += _calc_adj_points(points, 4, 1, 7)
    score += _calc_adj_points(points, 4, 7, 1)
    score += _calc_adj_points(points, 4, 3, 5)
    score += _calc_adj_points(points, 4, 5, 3)
    score += _calc_adj_points(points, 4, 0, 8)
    score += _calc_adj_points(points, 4, 8, 0)
    score += _calc_adj_points(points, 4, 2, 6)
    score += _calc_adj_points(points, 4, 6, 2)

    score += _calc_adj_points(points, 5, 4, 3)
    score += _calc_adj_points(points, 5, 3, 4)
    score += _calc_adj_points(points, 5, 2, 8)
    score += _calc_adj_points(points, 5, 8, 2)

    score += _calc_adj_points(points, 6, 3, 0)
    score += _calc_adj_points(points, 6, 0, 3)
    score += _calc_adj_points(points, 6, 4, 2)
    score += _calc_adj_points(points, 6, 2, 4)
    score += _calc_adj_points(points, 6, 7, 8)
    score += _calc_adj_points(points, 6, 8, 7)

    score += _calc_adj_points(points, 7, 4, 1)
    score += _calc_adj_points(points, 7, 1, 4)
    score += _calc_adj_points(points, 7, 8, 6)
    score += _calc_adj_points(points, 7, 6, 8)

    score += _calc_adj_points(points, 8, 5, 2)
    score += _calc_adj_points(points, 8, 2, 5)
    score += _calc_adj_points(points, 8, 7, 6)
    score += _calc_adj_points(points, 8, 6, 7)
    score += _calc_adj_points(points, 8, 4, 0)
    score += _calc_adj_points(points, 8, 0, 4)

    return score


def _global_calc_adj_points(points, i, j, k):
    # Helper function for eval function to check for blocks and adj tiles
    if points[i] > 75 and points[j] > 75 and points[k] >= 0:
        # print("a)In here because i: {}, j:{}, k: {}".format(i,j,k))
        return 100
    if points[i] < -75 and points[j] < -75 and points[k] <= 0:
        # print("b)In here because i: {}, j:{}, k: {}".format(i,j,k))
        return -100
    if points[i] < -75 and points[j] < -75 and points[k] >= 75:
        # print("c)In here because i: {}, j:{}, k: {}".format(i,j,k))
        return -75
    if points[i] > 75 and points[j] > 75 and points[k] <= -75:
        # print("d)In here because i: {}, j:{}, k: {}".format(i,j,k))
        return 75
    else:
        # print("e)In here because i: {}, j:{}, k: {}".format(i,j,k))
        return 0


def _global_check_in_2_adj(points):
    # Helper function to evaluvate all legal combinations of the board
    score = 0

    score += _global_calc_adj_points(points, 0, 1, 2)
    score += _global_calc_adj_points(points, 0, 2, 1)
    score += _global_calc_adj_points(points, 0, 4, 8)
    score += _global_calc_adj_points(points, 0, 8, 4)
    score += _global_calc_adj_points(points, 0, 3, 6)
    score += _global_calc_adj_points(points, 0, 6, 3)

    score += _global_calc_adj_points(points, 1, 0, 2)
    score += _global_calc_adj_points(points, 1, 2, 0)
    score += _global_calc_adj_points(points, 1, 4, 7)
    score += _global_calc_adj_points(points, 1, 7, 4)

    score += _global_calc_adj_points(points, 2, 1, 0)
    score += _global_calc_adj_points(points, 2, 0, 1)
    score += _global_calc_adj_points(points, 2, 4, 6)
    score += _global_calc_adj_points(points, 2, 6, 4)
    score += _global_calc_adj_points(points, 2, 5, 8)
    score += _global_calc_adj_points(points, 2, 8, 5)

    score += _global_calc_adj_points(points, 3, 4, 5)
    score += _global_calc_adj_points(points, 3, 5, 4)
    score += _global_calc_adj_points(points, 3, 0, 6)
    score += _global_calc_adj_points(points, 3, 6, 0)

    score += _global_calc_adj_points(points, 4, 1, 7)
    score += _global_calc_adj_points(points, 4, 7, 1)
    score += _global_calc_adj_points(points, 4, 3, 5)
    score += _global_calc_adj_points(points, 4, 5, 3)
    score += _global_calc_adj_points(points, 4, 0, 8)
    score += _global_calc_adj_points(points, 4, 8, 0)
    score += _global_calc_adj_points(points, 4, 2, 6)
    score += _global_calc_adj_points(points, 4, 6, 2)

    score += _global_calc_adj_points(points, 5, 4, 3)
    score += _global_calc_adj_points(points, 5, 3, 4)
    score += _global_calc_adj_points(points, 5, 2, 8)
    score += _global_calc_adj_points(points, 5, 8, 2)

    score += _global_calc_adj_points(points, 6, 3, 0)
    score += _global_calc_adj_points(points, 6, 0, 3)
    score += _global_calc_adj_points(points, 6, 4, 2)
    score += _global_calc_adj_points(points, 6, 2, 4)
    score += _global_calc_adj_points(points, 6, 7, 8)
    score += _global_calc_adj_points(points, 6, 8, 7)

    score += _global_calc_adj_points(points, 7, 4, 1)
    score += _global_calc_adj_points(points, 7, 1, 4)
    score += _global_calc_adj_points(points, 7, 8, 6)
    score += _global_calc_adj_points(points, 7, 6, 8)

    score += _global_calc_adj_points(points, 8, 5, 2)
    score += _global_calc_adj_points(points, 8, 2, 5)
    score += _global_calc_adj_points(points, 8, 7, 6)
    score += _global_calc_adj_points(points, 8, 6, 7)
    score += _global_calc_adj_points(points, 8, 4, 0)
    score += _global_calc_adj_points(points, 8, 0, 4)

    return score


def _global_check_for_winner_points(points, i, j, k):
    # Helper function for eval function to check for blocks and adj tiles
    if points[i] > 100 and points[j] > 100 and points[k] > 100:
        # print("In here as Queen won as because i: {}, j:{}, k: {}".format(i,j,k))
        return 1000
    if points[i] < -100 and points[j] < -100 and points[k] < -100:
        # print("In here king won because i: {}, j:{}, k: {}".format(i,j,k))
        return -1000
    else:
        # print("e)In here because i: {}, j:{}, k: {}".format(i,j,k))
        return 0


def _global_winner_points_score(points):
    # Helper function to evaluvate all legal combinations of the board
    score = 0

    score += _global_check_for_winner_points(points, 0, 1, 2)
    score += _global_check_for_winner_points(points, 0, 2, 1)
    score += _global_check_for_winner_points(points, 0, 4, 8)
    score += _global_check_for_winner_points(points, 0, 8, 4)
    score += _global_check_for_winner_points(points, 0, 3, 6)
    score += _global_check_for_winner_points(points, 0, 6, 3)

    score += _global_check_for_winner_points(points, 1, 0, 2)
    score += _global_check_for_winner_points(points, 1, 2, 0)
    score += _global_check_for_winner_points(points, 1, 4, 7)
    score += _global_check_for_winner_points(points, 1, 7, 4)

    score += _global_check_for_winner_points(points, 2, 1, 0)
    score += _global_check_for_winner_points(points, 2, 0, 1)
    score += _global_check_for_winner_points(points, 2, 4, 6)
    score += _global_check_for_winner_points(points, 2, 6, 4)
    score += _global_check_for_winner_points(points, 2, 5, 8)
    score += _global_check_for_winner_points(points, 2, 8, 5)

    score += _global_check_for_winner_points(points, 3, 4, 5)
    score += _global_check_for_winner_points(points, 3, 5, 4)
    score += _global_check_for_winner_points(points, 3, 0, 6)
    score += _global_check_for_winner_points(points, 3, 6, 0)

    score += _global_check_for_winner_points(points, 4, 1, 7)
    score += _global_check_for_winner_points(points, 4, 7, 1)
    score += _global_check_for_winner_points(points, 4, 3, 5)
    score += _global_check_for_winner_points(points, 4, 5, 3)
    score += _global_check_for_winner_points(points, 4, 0, 8)
    score += _global_check_for_winner_points(points, 4, 8, 0)
    score += _global_check_for_winner_points(points, 4, 2, 6)
    score += _global_check_for_winner_points(points, 4, 6, 2)

    score += _global_check_for_winner_points(points, 5, 4, 3)
    score += _global_check_for_winner_points(points, 5, 3, 4)
    score += _global_check_for_winner_points(points, 5, 2, 8)
    score += _global_check_for_winner_points(points, 5, 8, 2)

    score += _global_check_for_winner_points(points, 6, 3, 0)
    score += _global_check_for_winner_points(points, 6, 0, 3)
    score += _global_check_for_winner_points(points, 6, 4, 2)
    score += _global_check_for_winner_points(points, 6, 2, 4)
    score += _global_check_for_winner_points(points, 6, 7, 8)
    score += _global_check_for_winner_points(points, 6, 8, 7)

    score += _global_check_for_winner_points(points, 7, 4, 1)
    score += _global_check_for_winner_points(points, 7, 1, 4)
    score += _global_check_for_winner_points(points, 7, 8, 6)
    score += _global_check_for_winner_points(points, 7, 6, 8)

    score += _global_check_for_winner_points(points, 8, 5, 2)
    score += _global_check_for_winner_points(points, 8, 2, 5)
    score += _global_check_for_winner_points(points, 8, 7, 6)
    score += _global_check_for_winner_points(points, 8, 6, 7)
    score += _global_check_for_winner_points(points, 8, 4, 0)
    score += _global_check_for_winner_points(points, 8, 0, 4)

    return score


def _calc_points_for_local(board, boards, player):
    # Helper function to calc the points of a local board
    local_board_points = [0 for i in range(9)]
    board_num = 0
    score = 0
    for r in range(0, 3):
        for c in range(0, 3):
            winner = boards[board].get_tile_winner(r, c)
            if winner and winner == player:
                if boards[board].get_tile_winner(1, 1) == player:
                    score += 2
                if boards[board].get_tile_winner(1, 0) == player:
                    score += 1
                if boards[board].get_tile_winner(0, 1) == player:
                    score += 1
                if boards[board].get_tile_winner(1, 2) == player:
                    score += 1
                if boards[board].get_tile_winner(2, 1) == player:
                    score += 1
                local_board_points[board_num] = 1
                score += 1
            elif winner:
                if boards[board].get_tile_winner(1, 1) != player:
                    score -= 2
                if boards[board].get_tile_winner(1, 0) != player:
                    score -= 1
                if boards[board].get_tile_winner(0, 1) != player:
                    score -= 1
                if boards[board].get_tile_winner(1, 2) != player:
                    score -= 1
                if boards[board].get_tile_winner(2, 1) != player:
                    score -= 1
                local_board_points[board_num] = -1
                score -= 1
            else:
                local_board_points[board_num] = 0
            board_num += 1

    score += _check_in_2_adj(local_board_points)
    return score


def my_heuristic_eval(boards, player):
    # Eval function to give every board a point valye
    all_board_points = [0 for i in range(9)]
    globalboard = GlobalBoard(boards)
    score = 0
    for i in range(9):
        all_board_points[i] += _calc_points_for_local(i, boards, player)  # first calc a local board

    for i in range(9):
        temp = boards[i].get_winner()
        if temp and temp == player:
            if boards[4].get_winner() == player:
                all_board_points[4] += 300
            if boards[1].get_winner() == player:
                all_board_points[1] += 150
            if boards[3].get_winner() == player:
                all_board_points[3] += 150
            if boards[5].get_winner() == player:
                all_board_points[5] += 150
            if boards[7].get_winner() == player:
                all_board_points[7] += 150
            if boards[2].get_winner() == player:
                all_board_points[2] += 75
            if boards[6].get_winner() == player:
                all_board_points[6] += 75
            if boards[8].get_winner() == player:
                all_board_points[8] += 75

            # all_board_points[i] += 100 #give points for a local board win
        elif temp:
            if boards[4].get_winner() == player:
                all_board_points[4] -= 300
            if boards[1].get_winner() == player:
                all_board_points[1] -= 150
            if boards[3].get_winner() == player:
                all_board_points[3] -= 150
            if boards[5].get_winner() == player:
                all_board_points[5] -= 150
            if boards[7].get_winner() == player:
                all_board_points[7] -= 150
            if boards[2].get_winner() == player:
                all_board_points[2] -= 75
            if boards[6].get_winner() == player:
                all_board_points[6] -= 75
            if boards[8].get_winner() == player:
                all_board_points[8] -= 75
            # all_board_points[i] -= 500
        else:
            all_board_points[i] += 0
    # print("-=============================================-")
    # print(all_board_points)
    score = sum(all_board_points)
    # print("Score before: {}".format(score))
    score += _global_check_in_2_adj(all_board_points)  # calc global boards adjs
    # print("Score After adj check: {}".format(score))
    # print("-=============================================-")
    gameWinnerScore = _global_winner_points_score(all_board_points)
    # print("This is game winner score: {} score: {}".format(all_board_points,gameWinnerScore))
    overallScore = score + gameWinnerScore
    # print("Combined scores are adj check:{} | game winner: {} --> overall: {}".format(score,gameWinnerScore,overallScore))
    # print("-=============================================-")

    return overallScore


def heuristic_eval(boards, player):
    # Eval function to give every board a point valye
    all_board_points = [0 for i in range(9)]
    globalboard = GlobalBoard(boards)
    score = 0
    for i in range(9):
        all_board_points[i] += _calc_points_for_local(i, boards, player)  # first calc a local board

    for i in range(9):
        temp = boards[i].get_winner()
        if temp and temp == player:
            if boards[4].get_winner() == player:
                all_board_points[4] += 300
            if boards[1].get_winner() == player:
                all_board_points[1] += 150
            if boards[3].get_winner() == player:
                all_board_points[3] += 150
            if boards[5].get_winner() == player:
                all_board_points[5] += 150
            if boards[7].get_winner() == player:
                all_board_points[7] += 150
            if boards[2].get_winner() == player:
                all_board_points[2] += 75
            if boards[6].get_winner() == player:
                all_board_points[6] += 75
            if boards[8].get_winner() == player:
                all_board_points[8] += 75

            # all_board_points[i] += 100 #give points for a local board win
        elif temp:
            if boards[4].get_winner() == player:
                all_board_points[4] -= 300
            if boards[1].get_winner() == player:
                all_board_points[1] -= 150
            if boards[3].get_winner() == player:
                all_board_points[3] -= 150
            if boards[5].get_winner() == player:
                all_board_points[5] -= 150
            if boards[7].get_winner() == player:
                all_board_points[7] -= 150
            if boards[2].get_winner() == player:
                all_board_points[2] -= 75
            if boards[6].get_winner() == player:
                all_board_points[6] -= 75
            if boards[8].get_winner() == player:
                all_board_points[8] -= 75
            # all_board_points[i] -= 500
        else:
            all_board_points[i] += 0
    # print("-=============================================-")
    # print(all_board_points)
    score = sum(all_board_points)
    # print("Score before: {}".format(score))
    score += _global_check_in_2_adj(all_board_points)  # calc global boards adjs
    # print("Score After adj check: {}".format(score))
    # print("-=============================================-")
    gameWinnerScore = _global_winner_points_score(all_board_points)
    # print("This is game winner score: {} score: {}".format(all_board_points,gameWinnerScore))
    overallScore = score + gameWinnerScore
    # print("Combined scores are adj check:{} | game winner: {} --> overall: {}".format(score,gameWinnerScore,overallScore))
    # print("-=============================================-")

    return overallScore


def heuristic_strat(boards, player, op, currentBoard, startTime, timeLimit, lastTile=None, maximizing=False,
                    debug=False, alpha=float("-inf"),
                    beta=float("inf")):
    global_board = GlobalBoard(boards)  # create a global boards object with the current boards
    winner = global_board.get_global_winner()
    if winner:
        return (currentBoard, lastTile, heuristic_eval(boards, player))  # check if there is a winner (Utilty Function)

    if time.time() - startTime > (timeLimit - 1):
        # print("ran out of time")
        return (currentBoard, lastTile, heuristic_eval(boards, player))  # check if we ran out of time (Eval Function)

    choices = []

    if global_board.get_board_winnner(
            currentBoard):  # if theres a winner on the current board we must play eval all tiles in the global board
        for i in range(9):
            temp = global_board.get_board(i)
            tempChoices = temp.find_empty_tiles(i)
            for t in tempChoices:
                choices.append((t[0], t[1]))

    else:
        temp = global_board.get_board(currentBoard).find_empty_tiles(
            currentBoard)  # else only find tiles in the local board
        for t in temp:
            choices.append((t[0], t[1]))

    random.shuffle(
        choices)  # shuffle choices to ensure a little bit of randomness occurs due to time contraits, if no time constraints this would be the same as not shuffling
    globalValue = float("inf") if not maximizing else float("-inf")
    bestMove = None

    for choice in choices:  # go through each choice
        if choice == (currentBoard, lastTile):
            continue
        board, tile = choice
        copy = deepcopy(boards)  # create a copy of the board
        global_board_copy = GlobalBoard(copy)
        if maximizing:
            global_board_copy.get_board(board).assign_winner_tile(tile, player)  # assing a tile in the copy
        else:
            global_board_copy.get_board(board).assign_winner_tile(tile, op)  # assing a tile in the copy
        x, y, value = heuristic_strat(copy, player, op, tile, startTime, timeLimit, tile, not maximizing, debug=False,
                                      alpha=alpha, beta=beta)  # recursivly call minmax search
        global_board_copy.get_board(board).unassign_winner_tile(tile)
        if maximizing:
            if value >= beta:
                break

            if value and value > globalValue:
                globalValue = value
                bestMove = choice

            alpha = max(alpha, value)
        else:
            if value <= alpha:
                break

            if value and value < globalValue:
                globalValue = value
                bestMove = choice

            beta = min(beta, value)

        if time.time() - startTime > (timeLimit - 1):  # check for time after eval
            # print("ran out of time")
            break

    if not choices:
        return currentBoard, lastTile, globalValue  # if no choices found, or ran out of time return last evaluvated move
    if not bestMove:
        return choices[0][0], choices[0][1], 0  # return first choice if ran out of time
    return (bestMove[0], bestMove[1], globalValue)
