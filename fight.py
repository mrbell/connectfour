#!/usr/bin/env python

import sys

import connectfour as c4
import board as B


def fight(ntrials):
    """
    A simple function for having the computer play itself a number of times and
    to record who wins.
    """
    # FIXME: There is some kind of bug that makes random v. random matches hang
    #     sometimes.

    p1wins = 0
    draws = 0
    counter = 0

    for i in range(ntrials):

        if counter >= int(ntrials / 10.):
                sys.stdout.write("*")
                sys.stdout.flush()
                counter = 0

        result = c4.main(c4.COMPUTER, c4.COMPUTER, False, False)

        if result.curr_player == B.Board.P1:
            p1wins += 1
        elif result.curr_player == B.Board.EMPTY:
            draws += 1

        counter += 1

    sys.stdout.write("\n")
    sys.stdout.flush()

    print "Player 1 won " + str(p1wins) + " games of out of " + \
        str(ntrials - draws) + " decisions."


if __name__ == "__main__":
    ntrials = int(sys.argv[1])
    fight(ntrials)
