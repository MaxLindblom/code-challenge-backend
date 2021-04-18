"""Database initiation script
Should only be run once
"""

import sqlite3
from datetime import datetime

con = sqlite3.connect('test.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()

# Create our table
cur.execute('''CREATE TABLE clients (
               email TEXT,
               phone TEXT,
               latitude INTEGER,
               longitude INTEGER,
               traffic_area TEXT,
               register_date timestamp,
               PRIMARY KEY (email, phone));''')

# Insert two dummy clients
cur.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?)", ('test@test.com',None,60,18,'Uppland',datetime.now()))
cur.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?)", (None,'123456789',60,18,'Uppland',datetime.now()))

con.commit()
con.close()