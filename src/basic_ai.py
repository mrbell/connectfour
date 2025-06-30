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
from src.board import Board
from src.player import Player


WIN = 10000


class Slots:
    '''A struct used in the heuristic function.'''
    PIECE = 1  # A space filled with a piece
    VOID = -1  # An empty space that is not immediately fillable
    GAP = 0    # An empty space that is immediately fillable


def new_counts():
    return {Slots.PIECE: 0, Slots.VOID: 0, Slots.GAP: 0}    


def heuristic(board: Board, player_number: int) -> int:
    """
    Given a board instance and the players position to be evaluated, return an evaluation of the board 
    state, with a positive number meaning the board is better for the given player and a negative number
    meaning it is better for the opponent. Higher absolute values indicate a stronger position.

    The evaluation works as follows:

    Iterate over all sets of 4 spots on the board, any of which could eventually be the winning sequence.
    In a set of 4 contiguous slots, it cannot ever be a winning sequence if one of the opponents pieces 
    occupies a slot. In this case the sequence is not assigned any value. Otherwise the sequence could 
    eventually be a winning sequence. Assign points depending on the number of pices/empty slots in the 
    sequence, 

    - +5 for 2 pieces 
	- +20 for 3 in a row, with the empty spot not yet reachable
	- +50 for 3 in a row, with the empty spot reachable

    For sequences like GPPPG (G being a gap, P being a piece) this would produce 2 sequences of 
    3 in a row with a gap, so would count twice as much as a similar sequence lik GPPPO (where O 
    is an opponents piece).
    """
    value = 0

    other_player_number = board.P2 if player_number == board.P1 else board.P1

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for player in [player_number, other_player_number]:
        other_player = player_number if player == other_player_number else other_player_number
        modifier = 1 if player == player_number else -1
        for row in range(board.NROW):
            for col in range(board.NCOL):
                for direction in directions:
                    counts = new_counts()
                    is_invalid = False
                    for i in range(4):
                        r = row + direction[0] * i
                        c = col + direction[1] * i
                        if r < 0 or c < 0 or r >= board.NROW or c >= board.NCOL:
                            is_invalid = True
                            break
                        if board.state[r, c] == other_player:
                            is_invalid = True
                            break 
                        if board.state[r, c] == player:
                            counts[Slots.PIECE] += 1
                        elif r == 0 or board.state[r - 1, c] != board.EMPTY:
                            counts[Slots.GAP] += 1
                        else:
                            counts[Slots.VOID] += 1
                        
                    if is_invalid:
                        continue

                    if counts[Slots.PIECE] == 2:
                        value += modifier * 5
                    elif counts[Slots.PIECE] == 3 and counts[Slots.VOID] == 1:
                        value += modifier * 20
                    elif counts[Slots.PIECE] == 3 and counts[Slots.GAP] == 1:
                        value += modifier * 50

    return value 


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
    '''A node in the tree of board states explored with minimax'''
    def __init__(self, board: Board):
        self.board = board
    def is_terminal(self):
        '''A winning board state has no children.'''
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


def minimax(node, depth, is_maximizing_player, maximizing_player):
    '''
    Recursively explore all board states to a given depth.
    '''
    if depth == 0 or node.is_terminal():
        return evaluate(node.board, maximizing_player)

    ext_val = float('-inf') if is_maximizing_player else float('inf')
    ext_fn = max if is_maximizing_player else min

    for child in node.children():
        val = minimax(child, depth - 1, not is_maximizing_player, maximizing_player)
        ext_val = ext_fn(ext_val, val)

    return ext_val


def alpha_beta(node, depth, alpha, beta, is_maximizing_player, maximizing_player):
    """
    Recursively explore all board states to a given depth, pruning using the alpha-beta
    pruning algorithm.
    """
    if depth == 0 or node.is_terminal():
        return evaluate(node.board, maximizing_player)
    
    if is_maximizing_player:
        max_eval = float('-inf')
        for child in node.children():
            eval = alpha_beta(child, depth - 1, alpha, beta, False, maximizing_player)
            max_eval = max(eval, max_eval)
            alpha = max(eval, alpha)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child in node.children():
            eval = alpha_beta(child, depth - 1, alpha, beta, True, maximizing_player)
            min_eval = min(eval, min_eval)
            beta = min(eval, beta)
            if beta <= alpha:
                break
        return min_eval


class AIPlayer(Player):

    def __init__(self, player_num: int, max_depth: int):
        super().__init__(player_num)
        self.max_depth = max_depth

    def get_move(self, board: Board):
        
        moves = board.get_move_list()
        best_move_val = -100000000
        best_move = None

        def inherent_move_val(move):
            # Add points for moves that are closer to the center 
            # of the board 
            return min(move, board.NCOL - move - 1)

        for move in moves:
            temp = board.clone()
            temp.make_move(move)
            node = Node(temp)
            # move_val = minimax(node, self.max_depth - 1, False, self.player_num)
            move_val = alpha_beta(
                node, 
                self.max_depth - 1, 
                float('-inf'), 
                float('inf'),
                False,
                self.player_num
            )
            move_val += inherent_move_val(move)
            if move_val > best_move_val:
                best_move_val = move_val
                best_move = move
        
        return best_move
