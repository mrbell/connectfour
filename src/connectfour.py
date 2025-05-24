#!/usr/bin/env python

"""
connectfour.py

The connect four gameplay application.
"""

"""
Copyright 2012 Michael Bell

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

import curses

from board import Board
from player import Player, RandomPlayer

# Symbols for players and empty
SYMBOLS = {
    Board.P1: '●',
    Board.P2: '○',
    Board.EMPTY: '.'
}

# Color pair IDs
COLOR_P1 = 1
COLOR_P2 = 2
COLOR_EMPTY = 3


def draw_board(stdscr, board):
    stdscr.clear()
    stdscr.addstr(0, 0, ' Connect Four')
    for row in range(Board.NROW):
        for col in range(Board.NCOL):
            val = board.state[row, col]
            symbol = SYMBOLS[val]
            if val == Board.P1:
                color = curses.color_pair(COLOR_P1)
            elif val == Board.P2:
                color = curses.color_pair(COLOR_P2)
            else:
                color = curses.color_pair(COLOR_EMPTY)
            stdscr.addstr(row + 2, col * 2, symbol, color)
    # Draw column numbers
    col_numbers = ' '.join(str(i) for i in range(Board.NCOL))
    stdscr.addstr(Board.NROW + 2, 0, col_numbers)
    stdscr.refresh()


def get_move(stdscr, board):
    # Show the player's piece symbol in the prompt
    player_symbol = SYMBOLS[board.curr_player]
    if board.curr_player == Board.P1:
        color = curses.color_pair(COLOR_P1)
    else:
        color = curses.color_pair(COLOR_P2)
    prompt_base = f"Player {board.curr_player} "
    stdscr.addstr(Board.NROW + 4, 0, prompt_base)
    stdscr.addstr(Board.NROW + 4, len(prompt_base), player_symbol + " ", color)
    prompt_rest = f"move (0-{Board.NCOL-1}): "
    stdscr.addstr(Board.NROW + 4, len(prompt_base) + 2, prompt_rest)
    stdscr.clrtoeol()
    curses.echo()
    move_str = stdscr.getstr(Board.NROW + 4, len(prompt_base) + 2 + len(prompt_rest), 3).decode('utf-8')
    curses.noecho()
    try:
        move = int(move_str)
        if not board.is_legal_move(move):
            raise ValueError
        return move
    except Exception:
        stdscr.addstr(Board.NROW + 5, 0, "Invalid move. Press any key to continue.")
        stdscr.getch()
        return get_move(stdscr, board)


class HumanPlayer(Player):
    """
    A class representing a human player in the Connect Four game.
    """

    def __init__(self, player_num, stdscr):
        """
        Initialize the human player with a player number and the curses window.
        """
        super().__init__(player_num)
        self.stdscr = stdscr

    def get_move(self, board):
        """
        Get the player's move.

        Args:
            board (Board): The current game board.

        Returns:
            int: The column index where the player wants to drop their piece.
        """
        return get_move(self.stdscr, board)


def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(COLOR_P1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_P2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_EMPTY, curses.COLOR_WHITE, curses.COLOR_BLACK)

    b = Board()

    players = {
        Board.P1: HumanPlayer(Board.P1, stdscr),
        Board.P2: RandomPlayer(Board.P2)
    }

    while True:
        draw_board(stdscr, b)
        winner = b.check_for_victory()
        if winner is not None:
            draw_board(stdscr, b)
            if winner == Board.EMPTY:
                stdscr.addstr(Board.NROW + 4, 0, "It's a draw! Press any key to exit.")
            else:
                stdscr.addstr(Board.NROW + 4, 0, f"Player {winner} wins! Press any key to exit.")
            stdscr.getch()
            break
        player = players[b.curr_player]
        move = player.get_move(b)
        b.make_move(move)


if __name__ == "__main__":
    curses.wrapper(main)
