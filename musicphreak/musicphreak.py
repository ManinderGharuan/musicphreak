from os import path
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from scrapers import run_scrapers, get_data


app = Flask(__name__)


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=path.join(app.root_path, 'musicphreak.db')
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    print(app.config.get('DATABASE'))
    # if not path.exists(app.config.get('DATABASE')):
    #     init_db()

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()

    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.cli.command('run-scraper')
def run_scrapper_command():
    """Run scrapers"""
    run_scrapers()


@app.route('/')
def show_top20():
    data = get_data(get_db())

    for song in data:
        song['smallest_bitrate'] = min(song.get('mp3_links').keys())

    return render_template('top20.html', songs=data)
