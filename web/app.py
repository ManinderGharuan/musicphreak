from os import path
from flask import Flask, render_template, g
from scrapers import get_data
from .db import get_db

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=path.join(path.dirname(app.root_path), 'musicphreak.db')
))


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_top20():
    data = get_data(get_db(app))

    for song in data:
        song['smallest_bitrate'] = min(song.get('mp3_links').keys())

    return render_template('top20.html', songs=data)
