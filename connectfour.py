#!/usr/bin/env python

import sys

from board import Board
from c4bot import BotA as Computer1
from c4bot import Random as Computer2
from c4bot import Human

HUMAN = 1
COMPUTER = 0


def main(p1, p2, record=False, verbose=True):
    """
    The main game loop.

    Args:
        p1: An int indicating what kind of player 1 is.
        p2: Same as p1, but for player 2.
        record: A boolean indicating whether moves should be recorded and
            returned. [False]

    Returns:
        board: The game board instance.
    """

    b = Board(record)
    players = []
    if p1 == HUMAN:
        players.append(Human(1))
    else:
        players.append(Computer1(1))

    if p2 == HUMAN:
        players.append(Human(2))
    else:
        players.append(Computer2(2))

    while True:
        if verbose:
            print b
        move = players[b.curr_player - 1].move(b)
        if move < 0:
            if verbose:
                print "Thanks for playing!"
            break

        result = b.make_move(move)

        if result == b.VICTORY:
            if verbose:
                print ""
                print "-----------------------------------------"
                print ""
                print b
                print "Player " + str(b.curr_player) + " wins!"
                print ""
            break
        elif result == b.DRAW:
            if verbose:
                print "The game has ended in a draw."
            break
        elif result == b.ILLEGAL_MOVE:
            print "Illegal move, try again."

        if verbose:
            print ""
            print "-----------------------------------------"
            print ""

    return b


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Please indicate the number of human players that will play."
        sys.exit(0)
    nplayers = int(sys.argv[1])
    if nplayers == 1:
        ans = int(raw_input("Is the human player 1 or 2? "))
        if ans == 1:
            main(HUMAN, COMPUTER)
        elif ans == 2:
            main(COMPUTER, HUMAN)
        else:
            print "Invalid entry!"
            sys.exit(0)
    elif nplayers == 2:
        main(HUMAN, HUMAN)
    else:
        main(COMPUTER, COMPUTER)
