import sqlite3
from os import path


def connect_db(app):
    """
    Connects to the scraper database.
    """
    rv = sqlite3.connect(app.config['SCRAPER_DB'])
    rv.row_factory = sqlite3.Row

    return rv


def get_db(app):
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not path.exists(app.config['SCRAPER_DB']):
        init_db(app)

    return connect_db(app)


def init_db(app):
    db = connect_db(app)
    print("CREATING DATABASE")

    with open('scrapers/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()
