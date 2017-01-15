#!/usr/bin/env python

import sqlite3 as sql

import trainer as T
import fight as F
import connectfour as c4
import init_db

# initialize the database
init_db.init_db()

# Number of training steps to go between fight tests
step = 10000
ntrials = 10000
num_runs = 100

fn = "RAND_training_log_5.dat"

con = sql.connect(init_db.db_name)

for i in range(1, num_runs + 1):

    # Train botA against itself
    T.trainer(step, c4.RANDOM, c4.RANDOM)

    # BotA vs. Random fight test
    [p1wins, draws] = F.fight(c4.BOTA, c4.RANDOM, ntrials)

    cur = con.cursor()
    cur.execute("SELECT Count(*) FROM " + init_db.table_name)

    ntrain = i * step
    p1winfrac = p1wins / float(ntrials - draws)
    nrows = cur.fetchone()[0]

    f = open(fn, 'a')
    f.write("{0:7d} {1:.5f} {2:12d}\n".format(ntrain, p1winfrac, nrows))
    f.close()

    print "Finished " + str(ntrain) + " trials."
