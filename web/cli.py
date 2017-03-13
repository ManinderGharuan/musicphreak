from scrapers import run_scrapers
from musicphreak import app
from db import init_db


@app.cli.command('run-scraper')
def run_scrapper_command():
    """Run scrapers"""
    run_scrapers()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db(app)
    print('Initialized the database.')
