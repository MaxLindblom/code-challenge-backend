"""Database connector"""

import sqlite3
from datetime import datetime

DB_PATH = 'test.sqlite'


def add_client(client):
    """Add a client to database, if it doesn't already exist

    Parameters
    ----------
    client : Client
        The client to add

    Returns
    -------
    Client
        The client if it was added, otherwise None
    """

    (con, cur) = _connect()
    try:
        with con:
            cur.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?)",
                        (client.email,
                         client.phone,
                         client.lat,
                         client.lon,
                         client.traffic_area,
                         datetime.now()))
            return_val = client
    except sqlite3.IntegrityError:
        return_val = None
    _disconnect(con)
    return return_val


def get_client(client):
    """Retrieves a client from database, if it exists

    Parameters
    ----------
    client : Client
        The client to get

    Returns
    -------
    Client
        The client if it was found, otherwise None
    """

    (con, cur) = _connect()
    cur.execute("SELECT * FROM clients WHERE (email = ?) OR (phone = ?)",
                (client.email, client.phone))
    db_client = cur.fetchone()
    _disconnect(con)
    return db_client


def get_all_clients():
    """Gets all existing clients from the database

    Returns
    -------
    list
        List of all rows in the clients table
    """

    (con, cur) = _connect()
    cur.execute("SELECT * FROM clients")

    rows = cur.fetchall()
    _disconnect(con)
    return rows


def update_client(client):
    """Updates a client in database, if it exists

    Parameters
    ----------
    client : Client
        The client to update

    Returns
    -------
    Client
        The updated client
    """

    (con, cur) = _connect()
    cur.execute("UPDATE clients SET latitude = ?, longitude = ?, traffic_area = ?" +
                "WHERE (email = ?) OR (phone = ?)",
                (client.lat, client.lon, client.traffic_area, client.email, client.phone))
    _disconnect(con)
    return client


def remove_client(client):
    """Removes a client from database, if it exists

    Parameters
    ----------
    client : Client
        The client to remove

    Returns
    -------
    Client
        The removed client
    """

    (con, cur) = _connect()
    cur.execute("DELETE FROM clients WHERE (email = ?) OR (phone = ?)",
                (client.email, client.phone))
    _disconnect(con)
    return client


def _connect():
    con = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    return (con, cur)


def _disconnect(con):
    con.commit()
    con.close()
