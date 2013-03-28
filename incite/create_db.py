#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('data/samples.db')
c = conn.cursor()

c.execute('DROP TABLE samples')

c.execute('''CREATE TABLE samples
             (dataset numeric, date text, ch0 real, ch1 real, ch2 real, ch3 real)''')

conn.commit()
conn.close()
