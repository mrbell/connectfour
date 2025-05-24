import numpy as np


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
