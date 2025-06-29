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
from src.board import Board  # update for absolute import if needed


class Player:
    """
    Class representing a player in the Connect Four game.
    """

    def __init__(self, player_num):
        """
        Initialize the player with a player number.

        Args:
            player_num (int): The player number (1 or 2).
        """
        self.player_num = player_num

    def get_move(self, board):
        """
        Get the player's move.

        Args:
            board (Board): The current game board.

        Returns:
            int: The column index where the player wants to drop their piece.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")


class RandomPlayer(Player):
    """
    A class representing a random player in the Connect Four game.
    """

    def __init__(self, player_num):
        """
        Initialize the random player with a player number.
        """
        super().__init__(player_num)
    
    def get_move(self, board):
        """
        Get a random move for the player.

        Args:
            board (Board): The current game board.

        Returns:
            int: The column index where the player wants to drop their piece.
        """
        legal_moves = board.get_move_list()
        return np.random.choice(legal_moves)
