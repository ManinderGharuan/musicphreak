from scrapers import run_scrapers
from web.db import init_db


def add_cli(app):
    @app.cli.command('run-scraper')
    def run_scrapper_command():
        """Run scrapers"""
        run_scrapers(app)

    @app.cli.command('initdb')
    def initdb_command():
        """Initializes the database."""
        init_db(app)
        print('Initialized the database.')
