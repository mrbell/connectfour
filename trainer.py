#!/usr/bin/env python

import sqlite3 as sql
import sys

#from scipy import special

import connectfour as c4
import init_db


def trainer(niter):
    """
    A function to "train" the BotA connect four AI player. This will run a
    number of games of connect four where the bot plays against itself and
    populate the games.db database
    """

    con = sql.connect(init_db.db_name)

    cur = con.cursor()

    cur.execute("PRAGMA synchronous=0")
    con.commit()

    counter = 0

    for i in range(niter):
        if counter >= int(niter / 10.):
            sys.stdout.write("*")
            sys.stdout.flush()
            counter = 0

        board = c4.main(c4.BOTA, c4.BOTA, True, False)
        victor = board.curr_player

        # Don't update anything in case of a draw
        if victor == board.EMPTY:
            continue

        cur = con.cursor()

        for j in range(len(board.state_record)):
            sid = str(board.state_record[j])
            cur.execute("SELECT * FROM " + init_db.table_name +
                        " WHERE board_id=? OR " +
                        " mirror_id=?", (sid, sid))

            entry = cur.fetchone()

            if entry is None:
                # Create a new entry because this board config hasn't been
                # seen yet.

                np1wins = 0
                if victor == board.P1:
                    np1wins += 1

                prob1 = (1. + np1wins) / 3.
                prob2 = 1. - prob1

                mid = str(board.get_mirrored_id_from_id(board.state_record[j]))
                cur.execute("INSERT INTO " + init_db.table_name +
                            " VALUES(null, ?, ?, ?, ?, ?, ?)",
                            (sid, mid, 1, np1wins, prob1, prob2))  # ??

            else:
                key = entry[0]
                ngames = entry[3] + 1
                np1wins = entry[4]
                if victor == board.P1:
                    np1wins += 1

                # Compute new probabilities
                # This is the posterior mean assuming a binomial dist. for the
                # likelihood and a flat prior for the prob.
                prob1 = (np1wins + 1.) / (ngames + 2.)
                prob2 = 1. - prob1

                cur.execute("UPDATE " + init_db.table_name +
                            " SET ngames=?, np1wins=?, prob1=?, prob2=? " +
                            " WHERE id=?",
                            (ngames, np1wins, prob1, prob2, key))

            con.commit()
        counter += 1

    sys.stdout.write("\n")
    sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Must give the number of trials to run as an argument!"
    else:
        trainer(int(sys.argv[1]))
