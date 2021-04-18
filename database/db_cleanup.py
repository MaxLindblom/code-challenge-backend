"""Cleanup script for use during development"""

import sqlite3

con = sqlite3.connect('test.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS clients")

con.commit()
con.close()