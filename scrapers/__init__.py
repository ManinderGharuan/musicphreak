from scrapers.DjpunjabScraper import DjpunjabScraper
from scrapers.JattjugadScraper import JattjugadScraper
from scrapers.MrjattScraper import MrjattScraper
import json
from datetime import date
import os
from db import get_db
from pprint import pprint
from models.Album import Album
from models.Song import Song
from models.Artist import Artist
from models.ArtistAlbums import ArtistAlbums
from models.Mp3s import Mp3s

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__package__)), 'data')
JSON_FILENAME = '{}/{}.json' .format(DATA_DIR, date.today())


def run_scrapers():
    """
    Returns list of songs after running scrapers.

    Returns result of first scraper that finishes without error, otherwise raise an exception.
    """
    songs = []

    try:
        jt = JattjugadScraper()

        songs += jt.parse()
    except Exception as e:
        print("JattjugadScraper failed: ", e)

    try:
        dj = DjpunjabScraper()

        songs += dj.parse()
    except Exception as e:
        print("DjpunjabScraper failed: ", e)

    try:
        mr = MrjattScraper()

        songs += mr.parse()
    except Exception as e:
        print("MrjattScraper failed: ", e)
        raise "None of the scrapers worked. Sorry bru!"

    return songs


def save_songs_to_db(songs):
    """
    Save songs in database
    """
    db = get_db()

    try:
        cursor = db.cursor()

        for song in songs:
            song_name = song['name']
            artist_names = song['artist']
            album_name = song['album']
            source = song['source']
            poster_url = song['image_link']
            mp3_links = song['mp3_links']
            release_date = song['released_date']

            album_id = Album(
                album_name,
                release_date,
                poster_url
            ).insert(cursor).id

            song_id = Song(song_name, album_id).insert(cursor).id

            for name in (artist_names or ['N/A']):
                artist_id = Artist(name).insert(cursor).id
                ArtistAlbums(album_id, artist_id).insert(cursor)

            for quality in mp3_links:
                url = mp3_links.get(quality)
                Mp3s(song_id, url, source, quality).insert(cursor)

    except IOError as error:
        print("Error while inserting new song", error)
    finally:
        db.commit()
        db.close()


def get_data(limit=0):
    """
    Returns latest `limit` rows from database, all if latest is not given
    """


    return data
