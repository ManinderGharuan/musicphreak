from flask_script import Manager
from . import app
from scrapers import run_scrapers, run_ranking_scrapers, download_song_posters
from .db import init_db

cli = Manager(app)


@cli.command
def run_scrapper():
    """Run scrapers"""
    run_scrapers(app)


@cli.command
def run_ranking_scraper():
    """Run ranking scrapers"""
    run_ranking_scrapers(app)


@cli.command
def initdb():
    """Initializes the database."""
    init_db(app)
    print('Initialized the database.')


@cli.command
def download_poster_images():
    """Run download poster images function"""
    download_song_posters(app)


@cli.command
def web():
    """Run the web server"""
    app.run(debug=True)
