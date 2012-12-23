# -*- coding: utf-8 *-*

import numpy as np
import sqlite3 as sql
import init_db


class C4Bot(object):
    """
    The generic connect 4 player class.
    """

    pnum = 1  # the player number

    def __init__(self, pnum):
        """
        Sets the player number for the current class instance.
        """

        if pnum > 2 or pnum < 1:
            raise Exception("Illegal player number!")

        self.pnum = pnum

    def move(self, board):
        """
        Given the current board setup, make a move. Children must implement
        this method.
        """
        raise Exception("C4Bot does not have a default move. Children must" +
                        " implement this method!")
        return None


class Human(C4Bot):
    """
    A human controlled player. Moves are made using the standard input.
    """

    def __init__(self, pnum):
        """
        """
        super(Human, self).__init__(pnum)

    def move(self, board):
        """
        Given the current board setup, make a move.
        """
        move = int(raw_input('Enter move (0 to quit): ')) - 1

        return move


class Random(C4Bot):
    """
    A computer controlled player that chooses moves at random from the
    available options.
    """

    def __init__(self, pnum):
        """
        """
        super(Random, self).__init__(pnum)

    def move(self, board):
        """
        Given the current board setup, make a move.
        """
        ml = board.get_move_list()

        if len(ml) == 0:
            return None
        else:
            return ml[np.random.randint(0, len(ml))]


class BotA(C4Bot):
    """
    A computer controlled player that chooses that move that has the highest
    probability of leading to victory, as determined using a simple learning
    algorithm.
    """

    db_name = init_db.db_name
    table_name = init_db.table_name

    def __init__(self, pnum):
        """
        Initialize the class. Sets the player number.
        """
        super(BotA, self).__init__(pnum)
        self.con = sql.connect(self.db_name)

        # Don't care about synchronization. Runs WAY faster without
        cur = self.con.cursor()
        cur.execute("PRAGMA synchronous=0")
        self.con.commit()

        if self.pnum == 1:
            self.prob_key = "prob1"
        else:
            self.prob_key = "prob2"

    def move(self, board):
        """
        Given the current board setup, make a move.
        """

        ml = board.get_move_list()

        max_prob = 0.
        # The move(s) having the highest probability of winning.
        selected_moves = []

        cur = self.con.cursor()

        for i in range(len(ml)):
            testboard = board.get_new_board(ml[i])
            tbid = board.get_board_id(testboard)

            cur.execute("SELECT " + self.prob_key +
                        " FROM " + self.table_name +
                        " WHERE board_id=? " +
                        "OR mirror_id=?",
                        (str(tbid), str(tbid)))

            # returns None if there is no matching entry
            # returns a tuple with one entry otherwise.
            test_prob = cur.fetchone()

            if test_prob is None:
                # the board config is not in the data base, in which case we
                # say that there is a 50% chance of winning with it.
                test_prob = 0.5
            else:
                test_prob = test_prob[0]

            if test_prob > max_prob:
                max_prob = test_prob
                selected_moves = [ml[i]]
            elif test_prob == max_prob:
                selected_moves.append(ml[i])

        if len(selected_moves) == 0:
            return None
        else:
            selected_move = selected_moves[np.random.randint(0,
                                                         len(selected_moves))]
            return selected_move
