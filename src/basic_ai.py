# -*- coding: utf-8 *-*
"""
Copyright 2025 Michael Bell

This file is part of connectfour.

connectfour is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

connectfour is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with connectfour.  If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from board import Board
from player import Player


WIN = 1000


def heuristic(board: Board, player_number: int) -> int:
    """
    This logic isn't quite right. I should consider which player is next. If the next player
    has 3 in a row on a board, and is able to make a move to connect four, that should count 
    much more strongly than if you have 3 in a row but don't have the next move. However, 
    depending on recursion depth this evaluation function would still get to the right answer
    I think. So maybe it's fine. The minimax recursion should handle looking into the future.
    This function just provides a snapshot evaluation.
    """
    value = 0

    other_player_number = board.P2 if player_number == board.P1 else board.P1

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for player in [player_number, other_player_number]:
        other_player = player_number if player == other_player_number else other_player_number
        for row in range(board.NROW):
            for col in range(board.NCOL):
                for direction in directions:
                    n = 0
                    for i in range(4):
                        r = row + direction[0] * i
                        c = col + direction[1] * i
                        if r < 0 or c < 0 or r >= board.NROW or c >= board.NCOL:
                            n = 0
                            break
                        if board.state[r, c] == other_player:
                            n = 0
                            break 
                        if board.state[r, c] == player:
                            n += 1
                    if n == 3:
                        value += 1 if player == player_number else -1

    return value  # Because we count each 3 in a row twice


def evaluate(board: Board, player_number: int) -> int:
    victor = board.check_for_victory()
    if victor == board.EMPTY:
        return 0
    elif victor == player_number:
        return WIN
    elif victor is not None:
        return -WIN 
    else:
        return heuristic(board, player_number)


class Node:
    def __init__(self, board: Board):
        self.board = board
    def is_terminal(self):
        return self.board.check_for_victory() is not None
    def children(self):
        children_nodes = []
        next_moves = self.board.get_move_list()
        for next_move in next_moves:
            new_board = self.board.clone()
            new_board.make_move(next_move)
            children_nodes.append(Node(new_board))
        return children_nodes


def other_player(player_num: int) -> int:
    if player_num == Board.P1:
        return Board.P2
    else:
        return Board.P1


def minimax(node, depth, is_maximizing_player, player_to_move):
    if depth == 0 or node.is_terminal():
        return evaluate(node.board, player_to_move)

    if is_maximizing_player:
        maxEval = float('-inf')
        for child in node.children():
            eval = minimax(child, depth - 1, False, player_to_move)
            maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = float('inf')
        for child in node.children():
            eval = minimax(child, depth - 1, True, player_to_move)
            minEval = min(minEval, eval)
        return minEval


class AIPlayer(Player):

    def __init__(self, player_num: int, max_depth: int):
        super().__init__(player_num)
        self.max_depth = max_depth

    def get_move(self, board: Board):
        
        moves = board.get_move_list()
        best_move_val = -100000000
        best_move = None

        for move in moves:
            temp = board.clone()
            temp.make_move(move)
            node = Node(temp)
            move_val = minimax(node, self.max_depth - 1, False, self.player_num)
            if move_val > best_move_val:
                best_move_val = move_val
                best_move = move
        
        return best_move
