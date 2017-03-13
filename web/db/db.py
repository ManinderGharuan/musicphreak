from os import path
from flask import g
import sqlite3


def connect_db(app):
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db(app):
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not path.exists(app.config['DATABASE']):
        init_db(app)

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(app)

    return g.sqlite_db


def init_db(app):
    db = connect_db(app)
    print("CREATING DATABASE")

    with app.open_resource('db/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()
