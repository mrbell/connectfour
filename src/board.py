# -*- coding: utf-8 *-*
"""
board.py

The generic connect four board object. Encodes the rules of the connect four
game (i.e. checks for legal moves and for victory conditions). 
"""

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


def infer_current_player_nmoves(board):
    piece_counts = {board.P1: 0, board.P2: 0}

    for row in board.state:
        for col in row:
            if col in piece_counts:
                piece_counts[col] += 1
    
    nmoves = sum(piece_counts.values())
    curr_player = board.P1 if piece_counts[board.P1] == piece_counts[board.P2] else board.P2

    return curr_player, nmoves


class Board(object):
    """
    The class defining a connect four board.
    """
    # Player definitions and board states
    P1 = 1
    P2 = 2
    EMPTY = 0

    # Board dimensions
    NCOL = 7
    NROW = 6

    # A NROWxNCOL numpy array that acts as the board
    state = np.zeros((NROW, NCOL), dtype=int)
    curr_player = P1  # Which player has the next move.
    nmoves = 0  # How many moves have been played on this board instance

    def __init__(self, init_state=None):
        """
        Initialize a Board instance.
        """

        if init_state is not None:
            self.state = init_state
        else:
            self.state = np.zeros((self.NROW, self.NCOL), dtype=int)
        self.curr_player, self.nmoves = infer_current_player_nmoves(self)

    def clone(self):
        state_copy = self.state.copy()
        return Board(state_copy)

    def make_move(self, col):
        """
        Makes a move for the current player, updating the board, changing the
        current player, and checking whether the game is over. If the game ends
        the current player indicates the victor. An EMPTY player is set as the
        current player in case of a draw.

        Args:
            col: The column in which to add a piece.

        Returns:
            result: returns a move state indicating the result of the move
                VICTORY = The current player won with the move
                ILLEGAL_MOVE = The requested move is invalid
                LEGAL_MOVE = The requested move is valid, the board has been
                    updated and the current player changed.
                DRAW = The game has ended in a draw, no legal moves left.
        """

        if not self.is_legal_move(col):
            raise Exception("Illegal move requested!")

        for row in range(self.NROW - 1, -1, -1):
            if self.state[row, col] == self.EMPTY:
                self.state[row, col] = self.curr_player
                break

        self.nmoves += 1

        if self.curr_player == self.P1:
            self.curr_player = self.P2
        else:
            self.curr_player = self.P1

    def get_move_list(self):
        """
        Return the list of valid moves given the current board state.

        Returns:
            moves: A list of ints, each being a column that can be played as
                a valid move by the current player.
        """
        return [i for i in range(self.NCOL) if self.is_legal_move(i)]

    def is_legal_move(self, col):
        """
        Checks whether a move is valid.

        Args:
            col: Column into which a piece should be played.

        Returns:
            result: Bool stating whether the move is valid or not.
        """

        if col >= self.NCOL or col < 0:
            return False

        if self.state[0, col] == self.EMPTY:
            return True
        else:
            return False

    def check_for_victory(self):
        """
        Check whether the current player has won with the given board
        configuration.

        Returns:
            result: Player number for winning player, 0 if draw, or None if there is no winner yet.
        """

        if len(self.get_move_list()) == 0:
            return self.EMPTY

        for cp in [self.P1, self.P2]:

            # check for vertical connections
            for i in range(self.NCOL):
                num = 0
                for j in range(self.NROW):
                    if self.state[j, i] == cp:
                        num += 1
                    else:
                        num = 0

                    if num == 4:
                        return cp

            # check for horizontal connections
            for i in range(self.NROW):
                num = 0
                for j in range(self.NCOL):
                    if self.state[i, j] == cp:
                        num += 1
                    else:
                        num = 0

                    if num == 4:
                        return cp

            # check diagonal connections
            # subtract 1 from col, but add to row to get to next diag entry
            sdiags = [(0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6)]
            # add 1 to row and column to get to next diag entry
            adiags = [(0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0)]

            for i in range(len(sdiags)):
                indx = sdiags[i]
                num = 0
                while indx[0] < self.NROW and indx[1] >= 0:
                    if self.state[indx] == cp:
                        num += 1
                    else:
                        num = 0

                    if num == 4:
                        return cp

                    indx = (indx[0] + 1, indx[1] - 1)

            for i in range(len(adiags)):
                indx = adiags[i]
                num = 0
                while indx[0] < self.NROW and indx[1] < self.NCOL:
                    if self.state[indx] == cp:
                        num += 1
                    else:
                        num = 0

                    if num == 4:
                        return cp

                    indx = (indx[0] + 1, indx[1] + 1)

        return None
