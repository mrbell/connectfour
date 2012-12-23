#!/usr/bin/env python

import sqlite3 as sql

db_name = "games.db"
table_name = "Knowledge"


def init_db():
    """
    Initializes the games.db database.
    """

    con = sql.connect(db_name)

    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS " + table_name)
        cur.execute("CREATE TABLE " + table_name +
                    "(id INTEGER PRIMARY KEY, " +
                    "board_id TEXT, mirror_id TEXT, ngames INT, " +
                    "np1wins INT, prob1 FLOAT, prob2 FLOAT)")
        cur.execute("CREATE UNIQUE INDEX board_id_index ON " +
                    table_name + "(board_id)")
        cur.execute("CREATE UNIQUE INDEX mirror_id_index ON " +
                    table_name + "(mirror_id)")
        cur.execute("CREATE UNIQUE INDEX entry_id_index ON " +
                    table_name + "(id)")

if __name__ == "__main__":
    init_db()
