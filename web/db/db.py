from os import path
from flask import g
import sqlite3
from scrapers import *


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


def get_data(db):
    """
    Returns latest `limit` rows from database, all if latest is not given
    """
    cursor = db.cursor()

    rows = cursor.execute(
        """
        SELECT song.name AS "song_name", artist.name AS "artist_name",
               album.name AS "album_name", album.release_date,
               album.poster_img_url, mp3s.url, mp3s.quality
        FROM artist_albums
            INNER JOIN artist ON artist_albums.artist_id = artist.id
            INNER JOIN album ON artist_albums.album_id = album.id
            INNER JOIN song ON album.id = song.album_id
            INNER JOIN mp3s ON song.id = mp3s.song_id;
        """
    ).fetchall()

    return normalize_data(rows)
